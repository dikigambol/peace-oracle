import os
import time

try:
    import pymysql
    import pymysql.cursors

    HAS_PYMYSQL = True
except ImportError:
    HAS_PYMYSQL = False


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
