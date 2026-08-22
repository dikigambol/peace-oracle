import os
import json
from datetime import date
from flask import request

QUOTA_FILE = os.path.join(os.path.dirname(__file__), 'ai_quota_store.json')
DAILY_AI_LIMIT = 2

def get_client_id():
    try:
        # Prioritaskan X-Forwarded-For jika di belakang reverse proxy, fallback ke remote_addr
        forwarded = request.headers.get('X-Forwarded-For')
        if forwarded:
            ip = forwarded.split(',')[0].strip()
        else:
            ip = request.remote_addr
        return ip or '127.0.0.1'
    except Exception:
        return '127.0.0.1'

def _load_store():
    if os.path.exists(QUOTA_FILE):
        try:
            with open(QUOTA_FILE, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception:
            return {}
    return {}

def _save_store(store):
    try:
        with open(QUOTA_FILE, 'w', encoding='utf-8') as f:
            json.dump(store, f, indent=2)
    except Exception:
        pass

def check_ai_quota(client_id=None):
    """
    Memeriksa kuota AI harian pengguna (Maksimal 2x / hari).
    Kembalikan (is_allowed, count, limit, notice_message)
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    store = _load_store()

    client_data = store.get(client_id, {})
    saved_date = client_data.get('date')
    count = client_data.get('count', 0)

    # Reset kuota jika hari berganti
    if saved_date != today_str:
        count = 0

    if count >= DAILY_AI_LIMIT:
        notice = f"🔒 Quota Mode AI Gratis (2x/hari) Anda telah habis untuk hari ini ({count}/{DAILY_AI_LIMIT}). Beralih otomatis ke Mode Data Statis Default."
        return False, count, DAILY_AI_LIMIT, notice

    return True, count, DAILY_AI_LIMIT, None

def increment_ai_quota(client_id=None):
    """
    Menambah hitungan penggunaan AI harian pengguna.
    """
    if not client_id:
        client_id = get_client_id()

    today_str = date.today().isoformat()
    store = _load_store()

    client_data = store.get(client_id, {})
    saved_date = client_data.get('date')
    count = client_data.get('count', 0)

    if saved_date != today_str:
        count = 0

    count += 1
    store[client_id] = {
        'date': today_str,
        'count': count
    }
    _save_store(store)
    return count
