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


DB_OFFLINE_COOLDOWN = env_int("DB_OFFLINE_COOLDOWN", 60)
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = env_int("MYSQL_PORT", 3306)
MYSQL_DB = os.environ.get("MYSQL_DB")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
_DB_OFFLINE_UNTIL = 0.0


def db_available():
    return bool(HAS_PYMYSQL and MYSQL_HOST and MYSQL_DB and MYSQL_USER)


def mark_db_offline():
    global _DB_OFFLINE_UNTIL
    _DB_OFFLINE_UNTIL = time.monotonic() + DB_OFFLINE_COOLDOWN


def get_mysql_connection():
    if not db_available():
        return None
    if time.monotonic() < _DB_OFFLINE_UNTIL:
        return None
    try:
        return pymysql.connect(
            host=MYSQL_HOST,
            port=MYSQL_PORT,
            user=MYSQL_USER,
            password=MYSQL_PASSWORD,
            database=MYSQL_DB,
            cursorclass=pymysql.cursors.DictCursor,
            connect_timeout=2,
            read_timeout=3,
            write_timeout=3,
            autocommit=True,
        )
    except (pymysql.MySQLError, OSError):
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
