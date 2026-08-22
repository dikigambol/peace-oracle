import os
import json
import hashlib
from datetime import date
from flask import request

DAILY_AI_LIMIT = 2

# Path penyimpanan file kuota
PRIMARY_QUOTA_FILE = os.path.join(os.path.dirname(__file__), 'ai_quota_store.json')
TMP_QUOTA_FILE = '/tmp/ai_quota_store.json' if os.name != 'nt' else os.path.join(os.environ.get('TEMP', '.'), 'ai_quota_store_tmp.json')

# Memory cache fallback untuk serverless (seperti Vercel)
_MEMORY_STORE = {}

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
    """
    try:
        # 1. Cek Header X-Device-Id
        device_id = request.headers.get('X-Device-Id')
        if device_id and len(device_id) >= 8:
            return f"dev_{device_id}"

        # 2. Cek Cookie _z_device_id
        cookie_id = request.cookies.get('_z_device_id')
        if cookie_id and len(cookie_id) >= 8:
            return f"cookie_{cookie_id}"

        # 3. Cek POST JSON body
        if request.is_json:
            json_data = request.get_json(silent=True) or {}
            json_dev_id = json_data.get('device_id')
            if json_dev_id and len(json_dev_id) >= 8:
                return f"json_{json_dev_id}"

        # 4. Fallback ke IP + User-Agent Fingerprint
        return get_fp_id()
    except Exception:
        return get_fp_id()

def _get_active_file_path():
    try:
        if os.path.exists(PRIMARY_QUOTA_FILE):
            return PRIMARY_QUOTA_FILE
        # Test writeability
        with open(PRIMARY_QUOTA_FILE, 'a', encoding='utf-8') as f:
            pass
        return PRIMARY_QUOTA_FILE
    except Exception:
        return TMP_QUOTA_FILE

def _load_store():
    global _MEMORY_STORE
    target_file = _get_active_file_path()
    if os.path.exists(target_file):
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                _MEMORY_STORE.update(data)
                return _MEMORY_STORE
        except Exception:
            pass
    return _MEMORY_STORE

def _save_store(store):
    global _MEMORY_STORE
    _MEMORY_STORE = store
    target_file = _get_active_file_path()
    try:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2)
    except Exception:
        pass

def check_ai_quota(client_id=None):
    """
    Memeriksa kuota AI harian pengguna (Maksimal 2x / hari).
    Strict Check: Memeriksa Device ID DAN IP+UserAgent Fingerprint.
    Kembalikan (is_allowed, count, limit, notice_message)
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    store = _load_store()

    # Hitungan dari Device ID / Client ID
    client_data = store.get(client_id, {})
    saved_date = client_data.get('date')
    count = client_data.get('count', 0) if saved_date == today_str else 0

    # Hitungan dari IP + UserAgent Fingerprint (Proteksi anti-clear localstorage/cookies)
    fp_id = get_fp_id()
    fp_data = store.get(fp_id, {}) if (fp_id and fp_id != client_id) else {}
    fp_saved_date = fp_data.get('date')
    fp_count = fp_data.get('count', 0) if fp_saved_date == today_str else 0

    effective_count = max(count, fp_count)

    if effective_count >= DAILY_AI_LIMIT:
        notice = f"AI quota mode limited. Switching to Static Data Prediction."
        return False, effective_count, DAILY_AI_LIMIT, notice

    return True, effective_count, DAILY_AI_LIMIT, None

def increment_ai_quota(client_id=None):
    """
    Menambah hitungan penggunaan AI harian pengguna secara strict pada Device ID & IP Fingerprint.
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    store = _load_store()

    # Increment Client ID
    client_data = store.get(client_id, {})
    saved_date = client_data.get('date')
    count = client_data.get('count', 0) if saved_date == today_str else 0
    count += 1
    store[client_id] = {
        'date': today_str,
        'count': count
    }

    # Increment FP ID (IP + UserAgent Fingerprint)
    fp_id = get_fp_id()
    if fp_id and fp_id != client_id:
        fp_data = store.get(fp_id, {})
        fp_saved_date = fp_data.get('date')
        fp_count = fp_data.get('count', 0) if fp_saved_date == today_str else 0
        fp_count += 1
        store[fp_id] = {
            'date': today_str,
            'count': fp_count
        }

    _save_store(store)
    return count

