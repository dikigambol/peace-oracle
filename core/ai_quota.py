import datetime

from core.core import env_int, get_firestore_client, transact

WIB = datetime.timezone(datetime.timedelta(hours=7))
QUOTA_MEMORY_MAX = env_int("MEMORY_STORE_MAX", 5000)
QUOTA_TOTAL_BUCKET = "__total__"
QUOTA_MEMORY = {}


def quota_day():
    return datetime.datetime.now(WIB).date().isoformat()


def _quota_doc_id(namespace, client_id):
    raw = f"{namespace}_{client_id}".replace("/", "_").replace(".", "_")
    return raw[:200]


def stored_quota_count(namespace, client_id, day):
    db = get_firestore_client()
    if not db:
        return None
    try:
        doc = db.collection("ai_usage").document(_quota_doc_id(namespace, client_id)).get()
        if doc.exists:
            data = doc.to_dict() or {}
            if data.get("quota_date") == day:
                return data.get("used_count", 0)
        return 0
    except Exception as e:
        print(f"[FIREBASE QUOTA ERROR] Gagal baca quota: {e}", flush=True)
        return None


def store_quota_increment(namespace, client_id, day):
    db = get_firestore_client()
    if not db:
        return False

    def change(current):
        same_day = bool(current) and current.get("quota_date") == day
        count = int(current.get("used_count", 0)) + 1 if same_day else 1
        fields = {
            "namespace": namespace,
            "client_id": client_id,
            "quota_date": day,
            "used_count": count,
        }
        return fields, True

    try:
        return transact(db.collection("ai_usage").document(_quota_doc_id(namespace, client_id)), change)
    except Exception as e:
        print(f"[FIREBASE QUOTA ERROR] Gagal update quota: {e}", flush=True)
        return False


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
