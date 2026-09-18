import os
import time
import hashlib
from datetime import date
from flask import request

try:
    import pymysql
    import pymysql.cursors

    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False
def _env_int(name, fallback):
    try:
        return int(os.environ.get(name, fallback))
    except (TypeError, ValueError):
        return fallback


DAILY_AI_LIMIT = _env_int("DAILY_AI_LIMIT", 10)
FINGERPRINT_AI_LIMIT = _env_int(
    "FINGERPRINT_AI_LIMIT", max(DAILY_AI_LIMIT * 3, DAILY_AI_LIMIT)
)
MEMORY_STORE_MAX = _env_int("MEMORY_STORE_MAX", 5000)
DB_OFFLINE_COOLDOWN = _env_int("DB_OFFLINE_COOLDOWN", 60)
MYSQL_HOST = os.environ.get("MYSQL_HOST")
MYSQL_PORT = _env_int("MYSQL_PORT", 3306)
MYSQL_DB = os.environ.get("MYSQL_DB")
MYSQL_USER = os.environ.get("MYSQL_USER")
MYSQL_PASSWORD = os.environ.get("MYSQL_PASSWORD")
_MEMORY_STORE = {}
_DB_OFFLINE_UNTIL = 0.0


def _db_available():
    return bool(HAS_PYMYSQL and MYSQL_HOST and MYSQL_DB and MYSQL_USER)


def _mark_db_offline():
    global _DB_OFFLINE_UNTIL
    _DB_OFFLINE_UNTIL = time.monotonic() + DB_OFFLINE_COOLDOWN


def _get_mysql_connection():
    if not _db_available():
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
        _mark_db_offline()
        return None


def init_db():
    if not _db_available():
        return
    try:
        conn = _get_mysql_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS ai_quota (
                        client_id VARCHAR(191) PRIMARY KEY,
                        quota_date VARCHAR(20) NOT NULL,
                        used_count INT NOT NULL DEFAULT 0,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_quota_date (quota_date)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS quiz_rooms (
                        room_code VARCHAR(32) PRIMARY KEY,
                        host_name VARCHAR(100) NOT NULL,
                        host_sign VARCHAR(30) NOT NULL,
                        host_answers TEXT DEFAULT NULL,
                        partner_name VARCHAR(100) DEFAULT NULL,
                        partner_sign VARCHAR(30) DEFAULT NULL,
                        partner_answers TEXT DEFAULT NULL,
                        status VARCHAR(20) NOT NULL DEFAULT 'waiting',
                        match_score INT DEFAULT 0,
                        breakdown_json LONGTEXT DEFAULT NULL,
                        ai_result_json LONGTEXT DEFAULT NULL,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
                        INDEX idx_status (status)
                    ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
                """)
            conn.close()
    except Exception:
        pass


init_db()


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


get_client_id = get_device_id


def _prune_memory(today_str):
    global _MEMORY_STORE
    if len(_MEMORY_STORE) <= MEMORY_STORE_MAX:
        return
    _MEMORY_STORE = {
        k: v for k, v in _MEMORY_STORE.items() if v.get("date") == today_str
    }
    if len(_MEMORY_STORE) > MEMORY_STORE_MAX:
        _MEMORY_STORE = dict(list(_MEMORY_STORE.items())[-MEMORY_STORE_MAX:])


def _db_get_count(device_id, today_str):
    global _MEMORY_STORE
    if not device_id:
        return 0
    count = 0
    try:
        conn = _get_mysql_connection()
        if conn:
            with conn.cursor() as cursor:
                query = "SELECT used_count FROM ai_quota WHERE client_id = %s AND quota_date = %s"
                cursor.execute(query, (device_id, today_str))
                row = cursor.fetchone()
                if row:
                    count = row["used_count"]
            conn.close()
    except Exception:
        pass
    mem_val = _MEMORY_STORE.get(device_id, {})
    if mem_val.get("date") == today_str:
        count = max(count, mem_val.get("count", 0))
    return count


def _db_set_count(device_id, today_str, count):
    global _MEMORY_STORE
    if not device_id:
        return
    _MEMORY_STORE[device_id] = {"date": today_str, "count": count}
    _prune_memory(today_str)
    try:
        conn = _get_mysql_connection()
        if conn:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO ai_quota (client_id, quota_date, used_count)
                    VALUES (%s, %s, %s)
                    ON DUPLICATE KEY UPDATE
                        quota_date = VALUES(quota_date),
                        used_count = VALUES(used_count)
                """,
                    (device_id, today_str, count),
                )
            conn.close()
    except Exception:
        pass


def _quota_buckets(device_id):
    fingerprint_id = get_fingerprint_id()
    buckets = [(device_id, DAILY_AI_LIMIT)]
    if fingerprint_id != device_id:
        buckets.append((fingerprint_id, FINGERPRINT_AI_LIMIT))
    return buckets


def check_ai_quota(device_id=None):
    try:
        if not device_id:
            device_id = get_device_id()
        today_str = date.today().isoformat()
        used_count = 0
        for bucket_id, bucket_limit in _quota_buckets(device_id):
            bucket_count = _db_get_count(bucket_id, today_str)
            if bucket_id == device_id:
                used_count = bucket_count
            if bucket_count >= bucket_limit:
                notice = "AI Mode Limited. Switching to Standard Prediction."
                return False, used_count, DAILY_AI_LIMIT, notice
        return True, used_count, DAILY_AI_LIMIT, None
    except Exception:
        return True, 0, DAILY_AI_LIMIT, None


def increment_ai_quota(device_id=None):
    try:
        if not device_id:
            device_id = get_device_id()
        today_str = date.today().isoformat()
        new_count = 1
        for bucket_id, bucket_limit in _quota_buckets(device_id):
            bucket_count = _db_get_count(bucket_id, today_str) + 1
            _db_set_count(bucket_id, today_str, bucket_count)
            if bucket_id == device_id:
                new_count = bucket_count
        return new_count
    except Exception:
        return 1
