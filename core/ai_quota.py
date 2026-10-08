import datetime

from core.core import db_available, env_int, get_mysql_connection

WIB = datetime.timezone(datetime.timedelta(hours=7))
QUOTA_MEMORY_MAX = env_int("MEMORY_STORE_MAX", 5000)
QUOTA_TOTAL_BUCKET = "__total__"
QUOTA_MEMORY = {}
QUOTA_TABLE_STATE = {"ready": False}


def quota_day():
    return datetime.datetime.now(WIB).date().isoformat()


def run_quota_sql(sql, params=()):
    conn = get_mysql_connection()
    if not conn:
        return False, None
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            return True, cursor.fetchone()
    except Exception:
        return False, None
    finally:
        conn.close()


def ensure_quota_table():
    if QUOTA_TABLE_STATE["ready"] or not db_available():
        return QUOTA_TABLE_STATE["ready"]
    created, _ = run_quota_sql("""
        CREATE TABLE IF NOT EXISTS ai_usage (
            namespace VARCHAR(32) NOT NULL,
            client_id VARCHAR(191) NOT NULL,
            quota_date VARCHAR(10) NOT NULL,
            used_count INT NOT NULL DEFAULT 0,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            PRIMARY KEY (namespace, client_id)
        ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
    """)
    QUOTA_TABLE_STATE["ready"] = created
    return QUOTA_TABLE_STATE["ready"]


def stored_quota_count(namespace, client_id, day):
    if not ensure_quota_table():
        return None
    ok, row = run_quota_sql(
        "SELECT used_count, quota_date FROM ai_usage WHERE namespace = %s AND client_id = %s",
        (namespace, client_id),
    )
    if not ok:
        return None
    return row["used_count"] if row and row["quota_date"] == day else 0


def store_quota_increment(namespace, client_id, day):
    if not ensure_quota_table():
        return False
    ok, _ = run_quota_sql(
        """
        INSERT INTO ai_usage (namespace, client_id, quota_date, used_count)
        VALUES (%s, %s, %s, 1)
        ON DUPLICATE KEY UPDATE
            used_count = IF(quota_date = VALUES(quota_date), used_count + 1, 1),
            quota_date = VALUES(quota_date)
        """,
        (namespace, client_id, day),
    )
    return ok


def memory_quota_count(namespace, client_id, day):
    entry = QUOTA_MEMORY.get((namespace, client_id))
    return entry["count"] if entry and entry["date"] == day else 0


def prune_quota_memory(day):
    if len(QUOTA_MEMORY) <= QUOTA_MEMORY_MAX:
        return
    for key in [key for key, entry in QUOTA_MEMORY.items() if entry["date"] != day]:
        del QUOTA_MEMORY[key]
    removable = [key for key in QUOTA_MEMORY if key[1] != QUOTA_TOTAL_BUCKET]
    for key in removable[: max(0, len(QUOTA_MEMORY) - QUOTA_MEMORY_MAX)]:
        del QUOTA_MEMORY[key]


def memory_quota_increment(namespace, client_id, day):
    key = (namespace, client_id)
    count = memory_quota_count(namespace, client_id, day) + 1
    QUOTA_MEMORY.pop(key, None)
    QUOTA_MEMORY[key] = {"date": day, "count": count}
    prune_quota_memory(day)


class AiQuota:
    def __init__(self, namespace, device_limit, fingerprint_limit, daily_budget):
        self.namespace = namespace
        self.device_limit = device_limit
        self.fingerprint_limit = fingerprint_limit
        self.daily_budget = daily_budget

    def buckets(self, device_id=None, fingerprint_id=None):
        found = []
        if device_id:
            found.append((device_id, self.device_limit))
        if fingerprint_id and fingerprint_id != device_id:
            found.append((fingerprint_id, self.fingerprint_limit))
        found.append((QUOTA_TOTAL_BUCKET, self.daily_budget))
        return found

    def used(self, client_id, day):
        stored = stored_quota_count(self.namespace, client_id, day)
        return max(stored or 0, memory_quota_count(self.namespace, client_id, day))

    def allows(self, device_id=None, fingerprint_id=None):
        day = quota_day()
        return all(self.used(client_id, day) < limit for client_id, limit in self.buckets(device_id, fingerprint_id))

    def record(self, device_id=None, fingerprint_id=None):
        day = quota_day()
        for client_id, _ in self.buckets(device_id, fingerprint_id):
            memory_quota_increment(self.namespace, client_id, day)
            store_quota_increment(self.namespace, client_id, day)
