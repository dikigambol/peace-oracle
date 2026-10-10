import hashlib
import os

from flask import request

import base64
import json

try:
    import firebase_admin
    from firebase_admin import credentials, firestore

    HAS_FIREBASE = True
except ImportError:
    HAS_FIREBASE = False

def init_app(app):
    @app.context_processor
    def inject_installed_modes():
        return {"installed_modes": frozenset(app.blueprints)}


def env_int(name, fallback):
    try:
        return int(os.environ.get(name, fallback))
    except (TypeError, ValueError):
        return fallback


_FIRESTORE_CLIENT = None
_FIREBASE_INIT_ATTEMPTED = False


def get_service_account_dict():
    raw_env_key = os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY")
    if raw_env_key:
        raw_env_key = raw_env_key.strip()
        try:
            return json.loads(raw_env_key)
        except Exception:
            try:
                decoded = base64.b64decode(raw_env_key).decode("utf-8")
                return json.loads(decoded)
            except Exception as e:
                print(f"[FIREBASE ERROR] Gagal parse FIREBASE_SERVICE_ACCOUNT_KEY: {e}", flush=True)

    custom_path = os.environ.get("FIREBASE_SERVICE_ACCOUNT_PATH")
    root_file = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "serviceAccountKey.json")
    for path in (custom_path, root_file, "serviceAccountKey.json"):
        if path and os.path.isfile(path):
            try:
                with open(path, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception as e:
                print(f"[FIREBASE ERROR] Gagal membaca service account dari file {path}: {e}", flush=True)

    return None


def get_firestore_client():
    global _FIRESTORE_CLIENT, _FIREBASE_INIT_ATTEMPTED
    if not HAS_FIREBASE:
        return None
    if _FIRESTORE_CLIENT is not None:
        return _FIRESTORE_CLIENT
    if _FIREBASE_INIT_ATTEMPTED and _FIRESTORE_CLIENT is None:
        return None

    _FIREBASE_INIT_ATTEMPTED = True
    key_dict = get_service_account_dict()
    if not key_dict:
        print("[FIREBASE WARN] Kredensial Firebase tidak ditemukan (tidak ada env FIREBASE_SERVICE_ACCOUNT_KEY maupun file serviceAccountKey.json).", flush=True)
        return None

    try:
        cred = credentials.Certificate(key_dict)
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)
        _FIRESTORE_CLIENT = firestore.client()
        return _FIRESTORE_CLIENT
    except Exception as e:
        print(f"[FIREBASE ERROR] Gagal inisialisasi Firebase Admin / Firestore: {e}", flush=True)
        return None


def db_available():
    return get_firestore_client() is not None


class TransactionFailed(Exception):
    pass


def transact(doc_ref, change):
    client = get_firestore_client()
    if client is None:
        raise RuntimeError("Firestore is not configured")

    @firestore.transactional
    def run(transaction):
        snapshot = doc_ref.get(transaction=transaction)
        fields, result = change(snapshot.to_dict() if snapshot.exists else None)
        if fields:
            if snapshot.exists:
                transaction.update(doc_ref, fields)
            else:
                transaction.set(doc_ref, fields)
        return result

    try:
        return run(client.transaction())
    except ValueError as error:
        if str(error).startswith("Failed to commit transaction"):
            raise TransactionFailed() from error
        raise


def _hash(value):
    return hashlib.sha256(value.encode("utf-8")).hexdigest()[:40]


def get_fingerprint_id():
    try:
        forwarded = request.headers.get("X-Forwarded-For")
        ip = (
            forwarded.split(",")[0].strip()
            if forwarded
            else (request.remote_addr or "127.0.0.1")
        )
        user_agent = request.headers.get("User-Agent", "unknown_ua")
        accept_lang = request.headers.get("Accept-Language", "")
        sec_ua = request.headers.get("Sec-Ch-Ua", "")
        return "fp_" + _hash(f"{ip}_{user_agent}_{accept_lang}_{sec_ua}")
    except Exception:
        return "fp_default"


def get_device_id():
    try:
        raw_id = None
        dev_header = request.headers.get("X-Device-Id")
        if dev_header and len(dev_header.strip()) >= 8:
            raw_id = dev_header.strip()
        if not raw_id:
            cookie_id = request.cookies.get("_z_device_id")
            if cookie_id and len(cookie_id.strip()) >= 8:
                raw_id = cookie_id.strip()
        if not raw_id:
            if request.is_json:
                json_data = request.get_json(silent=True) or {}
                json_dev_id = json_data.get("device_id")
                if json_dev_id and len(str(json_dev_id).strip()) >= 8:
                    raw_id = str(json_dev_id).strip()
            if not raw_id:
                url_dev_id = request.args.get("device_id")
                if url_dev_id and len(url_dev_id.strip()) >= 8:
                    raw_id = url_dev_id.strip()
        if raw_id:
            for prefix in ("device_", "dev_", "cookie_", "json_"):
                if raw_id.startswith(prefix):
                    raw_id = raw_id[len(prefix) :]
                    break
            return "device_" + _hash(raw_id)
        return get_fingerprint_id()
    except Exception:
        return "device_default"
