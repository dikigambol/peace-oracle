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

    Catatan: Menggunakan format konsisten 'device_<raw_id>' untuk mencegah bypass kuota saat berpindah antar menu/endpoint.
    """
    try:
        raw_id = None
        # 1. Cek Header X-Device-Id
        dev_header = request.headers.get('X-Device-Id')
        if dev_header and len(dev_header) >= 8:
            raw_id = dev_header

        # 2. Cek Cookie _z_device_id
        if not raw_id:
            cookie_id = request.cookies.get('_z_device_id')
            if cookie_id and len(cookie_id) >= 8:
                raw_id = cookie_id

        # 3. Cek POST JSON body
        if not raw_id and request.is_json:
            json_data = request.get_json(silent=True) or {}
            json_dev_id = json_data.get('device_id')
            if json_dev_id and len(json_dev_id) >= 8:
                raw_id = json_dev_id

        if raw_id:
            # Normalisasi: Bersihkan prefix lama jika ada
            for prefix in ('dev_', 'cookie_', 'json_', 'device_'):
                if raw_id.startswith(prefix):
                    raw_id = raw_id[len(prefix):]
                    break
            return f"device_{raw_id}"

        # 4. Fallback ke IP + User-Agent Fingerprint
        return get_fp_id()
    except Exception:
        return get_fp_id()

def _get_active_file_path():
    """
    Menguji kemampuan tulis file secara eksplisit untuk mendukung lingkungan serverless / read-only (seperti Vercel).
    """
    try:
        with open(PRIMARY_QUOTA_FILE, 'a', encoding='utf-8') as f:
            pass
        return PRIMARY_QUOTA_FILE
    except Exception:
        return TMP_QUOTA_FILE

def _load_store():
    global _MEMORY_STORE
    today_str = date.today().isoformat()
    target_file = _get_active_file_path()
    disk_data = {}
    if os.path.exists(target_file):
        try:
            with open(target_file, 'r', encoding='utf-8') as f:
                disk_data = json.load(f)
        except Exception:
            disk_data = {}

    # Gabungkan data disk dengan _MEMORY_STORE (pertahankan count tertinggi untuk hari ini)
    for key, val in disk_data.items():
        if isinstance(val, dict) and val.get('date') == today_str:
            mem_val = _MEMORY_STORE.get(key, {})
            mem_count = mem_val.get('count', 0) if mem_val.get('date') == today_str else 0
            disk_count = val.get('count', 0)
            _MEMORY_STORE[key] = {
                'date': today_str,
                'count': max(mem_count, disk_count)
            }
        elif key not in _MEMORY_STORE:
            _MEMORY_STORE[key] = val

    return _MEMORY_STORE

def _save_store(store):
    global _MEMORY_STORE
    _MEMORY_STORE = store
    target_file = _get_active_file_path()
    try:
        with open(target_file, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2)
    except Exception:
        try:
            with open(TMP_QUOTA_FILE, 'w', encoding='utf-8') as f:
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

    # Cek variasi prefix legacy jika client_id adalah device_
    legacy_max = 0
    if client_id.startswith('device_'):
        raw = client_id[7:]
        for pfx in ('dev_', 'cookie_', 'json_'):
            leg_data = store.get(f"{pfx}{raw}", {})
            if leg_data.get('date') == today_str:
                legacy_max = max(legacy_max, leg_data.get('count', 0))

    # Hitungan dari IP + UserAgent Fingerprint (Proteksi anti-clear localstorage/cookies)
    fp_id = get_fp_id()
    fp_data = store.get(fp_id, {}) if (fp_id and fp_id != client_id) else {}
    fp_saved_date = fp_data.get('date')
    fp_count = fp_data.get('count', 0) if fp_saved_date == today_str else 0

    effective_count = max(count, legacy_max, fp_count)

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

    # Hitung hitungan efektif saat ini
    is_allowed, current_count, limit, notice = check_ai_quota(client_id)
    new_count = current_count + 1

    # Increment Client ID
    store[client_id] = {
        'date': today_str,
        'count': new_count
    }

    # Sinkronkan variasi prefix legacy jika client_id adalah device_
    if client_id.startswith('device_'):
        raw = client_id[7:]
        for pfx in ('dev_', 'cookie_', 'json_'):
            store[f"{pfx}{raw}"] = {
                'date': today_str,
                'count': new_count
            }

    # Increment FP ID (IP + UserAgent Fingerprint)
    fp_id = get_fp_id()
    if fp_id and fp_id != client_id:
        store[fp_id] = {
            'date': today_str,
            'count': new_count
        }

    _save_store(store)
    return new_count


