import hashlib
import os
import time

from flask import request

try:
    import pymysql
    import pymysql.cursors

    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False


def init_app(app):
    @app.context_processor
    def inject_installed_modes():
        return {"installed_modes": frozenset(app.blueprints)}


def env_int(name, fallback):
    try:
        return int(os.environ.get(name, fallback))
    except (TypeError, ValueError):
        return fallback


DB_OFFLINE_COOLDOWN = env_int("DB_OFFLINE_COOLDOWN", 5)
_DB_OFFLINE_UNTIL = 0.0


def _clean_env(val):
    if not val:
        return None
    s = str(val).strip()
    if (s.startswith('"') and s.endswith('"')) or (s.startswith("'") and s.endswith("'")):
        s = s[1:-1].strip()
    return s or None


def get_mysql_config():
    return {
        "host": _clean_env(os.environ.get("MYSQL_HOST")),
        "port": env_int("MYSQL_PORT", 3306),
        "database": _clean_env(os.environ.get("MYSQL_DB")),
        "user": _clean_env(os.environ.get("MYSQL_USER")),
        "password": _clean_env(os.environ.get("MYSQL_PASSWORD")),
    }


MYSQL_HOST = _clean_env(os.environ.get("MYSQL_HOST"))
MYSQL_PORT = env_int("MYSQL_PORT", 3306)
MYSQL_DB = _clean_env(os.environ.get("MYSQL_DB"))
MYSQL_USER = _clean_env(os.environ.get("MYSQL_USER"))
MYSQL_PASSWORD = _clean_env(os.environ.get("MYSQL_PASSWORD"))


def db_available():
    cfg = get_mysql_config()
    return bool(HAS_PYMYSQL and cfg["host"] and cfg["database"] and cfg["user"])


def mark_db_offline():
    global _DB_OFFLINE_UNTIL
    _DB_OFFLINE_UNTIL = time.monotonic() + DB_OFFLINE_COOLDOWN


def get_mysql_connection():
    if not db_available():
        return None
    if time.monotonic() < _DB_OFFLINE_UNTIL:
        return None
    cfg = get_mysql_config()
    try:
        return pymysql.connect(
            host=cfg["host"],
            port=cfg["port"],
            user=cfg["user"],
            password=cfg["password"],
            database=cfg["database"],
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=8,
            read_timeout=10,
            write_timeout=10,
            autocommit=True,
        )
    except (pymysql.MySQLError, OSError) as e:
        print(f"[DB ERROR] Gagal koneksi MySQL ({cfg['host']}:{cfg['port']}, db={cfg['database']}, user={cfg['user']}): {e}", flush=True)
        mark_db_offline()
        return None


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
