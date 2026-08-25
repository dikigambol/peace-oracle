import random
import datetime
from .bank import (
    DAILY_CIONG_MESSAGES,
    DAILY_SAN_HE_MESSAGES,
    DAILY_LIU_HE_MESSAGES,
    DAILY_WARNING_MESSAGES,
    DAILY_TAI_SUI_MESSAGES,
    DAILY_NEUTRAL_MESSAGES,
    SHIO_DAILY_TIPS,
    SHIO_GUARDIAN_BANK,
    SHIO_PROFILE_BANK,
    SHIO_COMPATIBILITY_BANK,
    SHIO_FORTUNE_BANK,
)

SHIO_DATA = {
    "tikus": {"name": "Tikus", "hanzi": "鼠"},
    "kerbau": {"name": "Kerbau", "hanzi": "牛"},
    "macan": {"name": "Macan", "hanzi": "虎"},
    "kelinci": {"name": "Kelinci", "hanzi": "兔"},
    "naga": {"name": "Naga", "hanzi": "龍"},
    "ular": {"name": "Ular", "hanzi": "蛇"},
    "kuda": {"name": "Kuda", "hanzi": "馬"},
    "kambing": {"name": "Kambing", "hanzi": "羊"},
    "monyet": {"name": "Monyet", "hanzi": "猴"},
    "ayam": {"name": "Ayam", "hanzi": "雞"},
    "anjing": {"name": "Anjing", "hanzi": "狗"},
    "babi": {"name": "Babi", "hanzi": "豬"},
}
SHIOS_LIST = [
    "tikus",
    "kerbau",
    "macan",
    "kelinci",
    "naga",
    "ular",
    "kuda",
    "kambing",
    "monyet",
    "ayam",
    "anjing",
    "babi",
]
LIU_HE_PAIRS = [
    (0, 1),
    (1, 0),
    (2, 11),
    (11, 2),
    (3, 10),
    (10, 3),
    (4, 9),
    (9, 4),
    (5, 8),
    (8, 5),
    (6, 7),
    (7, 6),
]


def get_all_daily_fortunes(client_date_str=None):
    anchor_date = datetime.date(2024, 1, 1)
    if client_date_str:
        try:
            year, month, day = map(int, client_date_str.split("-"))
            target_date = datetime.date(year, month, day)
        except:
            target_date = datetime.date.today()
    else:
        target_date = datetime.date.today()
    days_diff = (target_date - anchor_date).days
    shio_index = days_diff % 12
    today_shio_key = SHIOS_LIST[shio_index]
    today_shio_data = SHIO_DATA.get(today_shio_key)
    today_idx = SHIOS_LIST.index(today_shio_key)
    daily_seed = sum(ord(c) for c in str(target_date))
    results = []
    for shio_key in SHIOS_LIST:
        idx = SHIOS_LIST.index(shio_key)
        shio_data = SHIO_DATA.get(shio_key)
        dist = abs(today_idx - idx)
        if dist > 6:
            dist = 12 - dist
        msg_seed = daily_seed + idx
        msg_rng = random.Random(msg_seed)
        if dist == 6:
            status = "Ciong (Bentrokan)"
            status_code = "bad"
            message = msg_rng.choice(DAILY_CIONG_MESSAGES)
        elif dist == 4:
            status = "San He (Sangat Hoki)"
            status_code = "good"
            message = msg_rng.choice(DAILY_SAN_HE_MESSAGES)
        elif (today_idx, idx) in LIU_HE_PAIRS:
            status = "Liu He (Hoki Ekstra)"
            status_code = "good"
            message = msg_rng.choice(DAILY_LIU_HE_MESSAGES)
        elif dist == 3:
            status = "Waspada (Ketegangan)"
            status_code = "bad"
            message = msg_rng.choice(DAILY_WARNING_MESSAGES)
        elif dist == 0:
            status = "Hari Kembar (Tai Sui)"
            status_code = "neutral"
            message = msg_rng.choice(DAILY_TAI_SUI_MESSAGES)
        else:
            status = "Netral & Stabil"
            status_code = "neutral"
            message = msg_rng.choice(DAILY_NEUTRAL_MESSAGES)
        tips_list = SHIO_DAILY_TIPS.get(shio_key, [])
        daily_tip = msg_rng.choice(tips_list) if tips_list else ""
        results.append(
            {
                "shio_key": shio_key,
                "name": shio_data["name"],
                "hanzi": shio_data["hanzi"],
                "status": status,
                "status_code": status_code,
                "message": message,
                "daily_tip": daily_tip,
            }
        )
    formatted_date = target_date.strftime("%d %B %Y")
    return {
        "date_str": formatted_date,
        "today_shio_name": today_shio_data["name"],
        "today_shio_hanzi": today_shio_data["hanzi"],
        "fortunes": results,
    }


def get_shio_guardian(shio_key):
    return SHIO_GUARDIAN_BANK.get(shio_key, {})


def get_shio_profile(shio_key):
    profile = SHIO_PROFILE_BANK.get(shio_key)
    if not profile:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}
    return profile


def get_shio_compatibility(shio1_key, shio2_key):
    s1_data = SHIO_DATA.get(shio1_key)
    s2_data = SHIO_DATA.get(shio2_key)
    if not s1_data or not s2_data:
        return {"error": "Shio tidak ditemukan."}
    pair_key = tuple(sorted([shio1_key, shio2_key]))
    compat = SHIO_COMPATIBILITY_BANK.get(pair_key)
    if not compat:
        compat = SHIO_COMPATIBILITY_BANK.get((shio1_key, shio2_key))
    if not compat:
        compat = SHIO_COMPATIBILITY_BANK.get((shio2_key, shio1_key))
    if not compat:
        return {
            "error": "Data kompatibilitas belum tersedia untuk pasangan ini.",
            "shio1": {"name": s1_data["name"], "hanzi": s1_data["hanzi"]},
            "shio2": {"name": s2_data["name"], "hanzi": s2_data["hanzi"]},
        }
    return {
        "shio1": {"name": s1_data["name"], "hanzi": s1_data["hanzi"]},
        "shio2": {"name": s2_data["name"], "hanzi": s2_data["hanzi"]},
        "relationship": compat.get("relationship", ""),
        "score": compat.get("score", 50),
        "asmara": compat.get("asmara", ""),
        "bisnis": compat.get("bisnis", ""),
        "drama": compat.get("drama", ""),
        "tips": compat.get("tips", ""),
    }


def get_shio_fortune(shio_key):
    shio_data = SHIO_DATA.get(shio_key)
    if not shio_data:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}
    fortune_data = SHIO_FORTUNE_BANK.get(shio_key)
    if not fortune_data:
        return {"error": f"Data ramalan untuk Shio '{shio_key}' belum tersedia."}
    today = datetime.date.today()
    seed_val = sum(ord(c) for c in (shio_key + str(today)))
    rng = random.Random(seed_val)
    result = {
        "shio_key": shio_key,
        "name": shio_data["name"],
        "hanzi": shio_data["hanzi"],
        "date": today.strftime("%d %B %Y"),
    }
    for category in ["karir", "keuangan", "asmara", "kesehatan"]:
        pool = fortune_data.get(category, [])
        if pool:
            result[category] = rng.choice(pool)
        else:
            result[category] = "Ramalan sedang disiapkan oleh alam semesta..."
    return result
