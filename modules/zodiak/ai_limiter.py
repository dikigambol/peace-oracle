import os
import json
import sqlite3
import hashlib
from datetime import date
from flask import request

DAILY_AI_LIMIT = 2

# Database path with tmp fallback for serverless
PRIMARY_DB_FILE = os.path.join(os.path.dirname(__file__), 'ai_quota.db')
TMP_DB_FILE = '/tmp/ai_quota.db' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'ai_quota_tmp.db')

_MEMORY_STORE = {}

def _get_db_path():
    try:
        conn = sqlite3.connect(PRIMARY_DB_FILE)
        conn.close()
        return PRIMARY_DB_FILE
    except Exception:
        return TMP_DB_FILE

def _get_db_connection():
    db_path = _get_db_path()
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ai_quota (
                client_id TEXT PRIMARY KEY,
                quota_date TEXT NOT NULL,
                used_count INTEGER NOT NULL DEFAULT 0
            )
        ''')
        conn.commit()
        conn.close()
    except Exception:
        pass

# Initialize DB table on import
init_db()

def get_fp_id():
    """
    Menghasilkan Fingerprint Hash berbasis IP + User-Agent.
    Dipakai sebagai fallback & proteksi ganda jika cookie/localstorage dibersihkan.
    """
    try:
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            ip = forwarded.split(',')[0].strip()
        else:
            ip = request.remote_addr or '127.0.0.1'

        user_agent = request.headers.get('User-Agent', 'unknown_ua')
        fp_raw = f"{ip}_{user_agent}"
        return f"fp_{hashlib.md5(fp_raw.encode('utf-8')).hexdigest()}"
    except Exception:
        return "fp_default"

def get_client_id():
    """
    Identifikasi perangkat secara strict & multi-layer:
    1. Header X-Device-Id (dikirim otomatis oleh JS via LocalStorage)
    2. Cookie _z_device_id
    3. Parameter JSON device_id
    4. Fallback: Hash IP + User-Agent

    Catatan: Menggunakan format konsisten 'device_<raw_id>' untuk mencegah bypass kuota saat berpindah antar menu/endpoint.
    """
    try:
        raw_id = None
        dev_header = request.headers.get('X-Device-Id')
        if dev_header and len(dev_header) >= 8:
            raw_id = dev_header

        if not raw_id:
            cookie_id = request.cookies.get('_z_device_id')
            if cookie_id and len(cookie_id) >= 8:
                raw_id = cookie_id

        if not raw_id and request.is_json:
            json_data = request.get_json(silent=True) or {}
            json_dev_id = json_data.get('device_id')
            if json_dev_id and len(json_dev_id) >= 8:
                raw_id = json_dev_id

        if raw_id:
            for prefix in ('dev_', 'cookie_', 'json_', 'device_'):
                if raw_id.startswith(prefix):
                    raw_id = raw_id[len(prefix):]
                    break
            return f"device_{raw_id}"

        return get_fp_id()
    except Exception:
        return get_fp_id()

def _db_get_count(client_id, today_str):
    global _MEMORY_STORE
    db_count = 0
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute(
            "SELECT used_count FROM ai_quota WHERE client_id = ? AND quota_date = ?",
            (client_id, today_str)
        )
        row = cursor.fetchone()
        if row:
            db_count = row['used_count']
        conn.close()
    except Exception:
        pass

    mem_val = _MEMORY_STORE.get(client_id, {})
    mem_count = mem_val.get('count', 0) if mem_val.get('date') == today_str else 0

    return max(db_count, mem_count)

def _db_set_count(client_id, today_str, count):
    global _MEMORY_STORE
    _MEMORY_STORE[client_id] = {'date': today_str, 'count': count}
    try:
        conn = _get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO ai_quota (client_id, quota_date, used_count)
            VALUES (?, ?, ?)
            ON CONFLICT(client_id) DO UPDATE SET
                quota_date = excluded.quota_date,
                used_count = excluded.used_count
        ''', (client_id, today_str, count))
        conn.commit()
        conn.close()
    except Exception:
        pass

def check_ai_quota(client_id=None):
    """
    Memeriksa kuota AI harian pengguna (Maksimal 2x / hari) via SQLite DB.
    Strict Check: Memeriksa Device ID DAN IP+UserAgent Fingerprint.
    Kembalikan (is_allowed, count, limit, notice_message)
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    init_db()

    count = _db_get_count(client_id, today_str)

    legacy_max = 0
    if client_id.startswith('device_'):
        raw = client_id[7:]
        for pfx in ('dev_', 'cookie_', 'json_'):
            leg_count = _db_get_count(f"{pfx}{raw}", today_str)
            legacy_max = max(legacy_max, leg_count)

    fp_id = get_fp_id()
    fp_count = 0
    if fp_id and fp_id != client_id:
        fp_count = _db_get_count(fp_id, today_str)

    effective_count = max(count, legacy_max, fp_count)

    if effective_count >= DAILY_AI_LIMIT:
        notice = "AI quota mode limited. Switching to Static Data Prediction."
        return False, effective_count, DAILY_AI_LIMIT, notice

    return True, effective_count, DAILY_AI_LIMIT, None

def increment_ai_quota(client_id=None):
    """
    Menambah hitungan penggunaan AI harian pengguna secara strict pada Device ID & IP Fingerprint via SQLite DB.
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    init_db()

    is_allowed, current_count, limit, notice = check_ai_quota(client_id)
    new_count = current_count + 1

    _db_set_count(client_id, today_str, new_count)

    if client_id.startswith('device_'):
        raw = client_id[7:]
        for pfx in ('dev_', 'cookie_', 'json_'):
            _db_set_count(f"{pfx}{raw}", today_str, new_count)

    fp_id = get_fp_id()
    if fp_id and fp_id != client_id:
        _db_set_count(fp_id, today_str, new_count)

    return new_count



