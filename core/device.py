import hashlib

from flask import request


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
