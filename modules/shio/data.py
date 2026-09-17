import random
import datetime
import math
import zlib
import ephem
from .bank import (
    DAY_OFFICER_BANK,
    ELEMENT_RELATION_BANK,
    DAILY_CHONG_MESSAGES,
    DAILY_SAN_HE_MESSAGES,
    DAILY_LIU_HE_MESSAGES,
    DAILY_XIANG_XING_MESSAGES,
    DAILY_PO_MESSAGES,
    DAILY_HAI_MESSAGES,
    DAILY_ZI_XING_MESSAGES,
    DAILY_BEN_MING_MESSAGES,
    DAILY_PING_MESSAGES,
    SHIO_DAILY_TIPS,
    SHIO_GUARDIAN_BANK,
    SHIO_COMPATIBILITY_BANK,
    SHIO_YEARLY_BANK,
    SHIO_ROASTING_BANK,
    SHIO_FORTUNE_COOKIE_BANK,
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

LIU_HE_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]
)

LIU_PO_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10)]
)

LIU_HAI_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)]
)

XIANG_XING_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(2, 5), (5, 8), (2, 8), (1, 10), (10, 7), (1, 7), (0, 3)]
)

ZI_XING_BRANCHES = frozenset([4, 6, 9, 11])

BRANCH_RELATION_META = {
    "liu_he": {"label": "Liu He (Jodoh Kosmik Sejati)", "code": "good", "band": (95, 99)},
    "san_he": {"label": "San He (Tiga Harmoni)", "code": "good", "band": (85, 90)},
    "ben_ming": {"label": "Ben Ming (Kembar Kosmik)", "code": "neutral", "band": (72, 78)},
    "netral": {"label": "Ping (Netral & Stabil)", "code": "neutral", "band": (58, 68)},
    "liu_po": {"label": "Liu Po (Perusakan)", "code": "bad", "band": (50, 57)},
    "zi_xing": {"label": "Zi Xing (Hukuman Diri)", "code": "bad", "band": (44, 49)},
    "liu_hai": {"label": "Liu Hai (Saling Menyakiti)", "code": "bad", "band": (37, 43)},
    "xiang_xing": {"label": "Xiang Xing (Hukuman)", "code": "bad", "band": (30, 36)},
    "chong": {"label": "Chong (Bentrokan Ekstrem)", "code": "bad", "band": (23, 29)},
}

def get_branch_relation(idx_a, idx_b):
    dist = abs(idx_a - idx_b)

    if dist > 6:
        dist = 12 - dist

    pair = frozenset((idx_a, idx_b))

    if idx_a != idx_b:
        if dist == 6:
            return "chong"
        if dist == 4:
            return "san_he"
        if pair in LIU_HE_PAIRS:
            return "liu_he"
    else:
        return "zi_xing" if idx_a in ZI_XING_BRANCHES else "ben_ming"

    if pair in XIANG_XING_PAIRS:
        return "xiang_xing"
    if pair in LIU_HAI_PAIRS:
        return "liu_hai"
    if pair in LIU_PO_PAIRS:
        return "liu_po"
    return "netral"

ALMANAC_TZ = datetime.timezone(datetime.timedelta(hours=7), "WIB")

HEAVENLY_STEMS = [
    ("Jia", "甲"), ("Yi", "乙"), ("Bing", "丙"), ("Ding", "丁"), ("Wu", "戊"),
    ("Ji", "己"), ("Geng", "庚"), ("Xin", "辛"), ("Ren", "壬"), ("Gui", "癸"),
]

EARTHLY_BRANCHES = [
    ("Zi", "子"), ("Chou", "丑"), ("Yin", "寅"), ("Mao", "卯"),
    ("Chen", "辰"), ("Si", "巳"), ("Wu", "午"), ("Wei", "未"),
    ("Shen", "申"), ("You", "酉"), ("Xu", "戌"), ("Hai", "亥"),
]

STEM_ELEMENTS = [
    "kayu", "kayu", "api", "api", "tanah",
    "tanah", "logam", "logam", "air", "air",
]

BRANCH_ELEMENTS = [
    "air", "tanah", "kayu", "kayu", "tanah", "api",
    "api", "tanah", "logam", "logam", "tanah", "air",
]

ELEMENT_LABELS = {
    "kayu": ("Kayu", "木"),
    "api": ("Api", "火"),
    "tanah": ("Tanah", "土"),
    "logam": ("Logam", "金"),
    "air": ("Air", "水"),
}

ELEMENT_GENERATES = {
    "kayu": "api",
    "api": "tanah",
    "tanah": "logam",
    "logam": "air",
    "air": "kayu",
}

ELEMENT_CONTROLS = {
    "kayu": "tanah",
    "tanah": "air",
    "air": "api",
    "api": "logam",
    "logam": "kayu",
}

JULIAN_DAY_OFFSET = 1721425

DAILY_RELATION_VIEW = {
    "chong": ("Chong (Bentrokan)", DAILY_CHONG_MESSAGES),
    "san_he": ("San He (Sangat Hoki)", DAILY_SAN_HE_MESSAGES),
    "liu_he": ("Liu He (Hoki Ekstra)", DAILY_LIU_HE_MESSAGES),
    "zi_xing": ("Zi Xing (Hukuman Diri)", DAILY_ZI_XING_MESSAGES),
    "ben_ming": ("Ben Ming (Hari Kembar)", DAILY_BEN_MING_MESSAGES),
    "xiang_xing": ("Xiang Xing (Hukuman)", DAILY_XIANG_XING_MESSAGES),
    "liu_hai": ("Liu Hai (Bahaya Tersembunyi)", DAILY_HAI_MESSAGES),
    "liu_po": ("Liu Po (Perusakan)", DAILY_PO_MESSAGES),
    "netral": ("Ping (Netral & Stabil)", DAILY_PING_MESSAGES),
}

def build_stable_seed(*parts):
    raw = "|".join(str(p) for p in parts).encode("utf-8")
    return zlib.crc32(raw)

def get_day_pillar(target_date):
    jdn = target_date.toordinal() + JULIAN_DAY_OFFSET
    return (jdn + 9) % 10, (jdn + 1) % 12

def get_solar_longitude(target_date):
    noon = datetime.datetime(
        target_date.year, target_date.month, target_date.day, 12, 0
    )
    sun = ephem.Sun()
    sun.compute(ephem.Date(noon))
    return math.degrees(float(ephem.Ecliptic(sun).lon)) % 360

def get_month_branch(target_date):
    longitude = get_solar_longitude(target_date)
    return (int((longitude - 315) % 360 // 30) + 2) % 12

def get_day_officer(day_branch, month_branch):
    return DAY_OFFICER_BANK[(day_branch - month_branch) % 12]

def get_element_relation(day_element, shio_element):
    if day_element == shio_element:
        key = "bi_he"
    elif ELEMENT_GENERATES[day_element] == shio_element:
        key = "sheng_wo"
    elif ELEMENT_GENERATES[shio_element] == day_element:
        key = "wo_sheng"
    elif ELEMENT_CONTROLS[day_element] == shio_element:
        key = "ke_wo"
    else:
        key = "wo_ke"
    return key, ELEMENT_RELATION_BANK[key]

def resolve_almanac_date(client_date_str=None):
    if client_date_str:
        try:
            year, month, day = map(int, client_date_str.split("-"))
            return datetime.date(year, month, day)
        except (ValueError, AttributeError):
            pass

    now = datetime.datetime.now(ALMANAC_TZ)
    target = now.date()

    if now.hour >= 23:
        target += datetime.timedelta(days=1)
    return target

def get_all_daily_fortunes(client_date_str=None):
    target_date = resolve_almanac_date(client_date_str)

    stem_idx, shio_index = get_day_pillar(target_date)
    month_branch = get_month_branch(target_date)
    officer = get_day_officer(shio_index, month_branch)
    day_element = STEM_ELEMENTS[stem_idx]
    today_shio_key = SHIOS_LIST[shio_index]
    today_shio_data = SHIO_DATA.get(today_shio_key)
    today_idx = SHIOS_LIST.index(today_shio_key)
    results = []
    
    for shio_key in SHIOS_LIST:
        idx = SHIOS_LIST.index(shio_key)
        shio_data = SHIO_DATA.get(shio_key)

        msg_seed = build_stable_seed("daily", target_date.toordinal(), shio_key)
        msg_rng = random.Random(msg_seed)

        relation_key = get_branch_relation(today_idx, idx)
        status, pool = DAILY_RELATION_VIEW[relation_key]
        status_code = BRANCH_RELATION_META[relation_key]["code"]
        message = msg_rng.choice(pool)

        tips_list = SHIO_DAILY_TIPS.get(shio_key, [])
        daily_tip = msg_rng.choice(tips_list) if tips_list else ""

        shio_element = BRANCH_ELEMENTS[idx]
        relation_key, relation = get_element_relation(day_element, shio_element)
        element_name, element_hanzi = ELEMENT_LABELS[shio_element]

        results.append(
            {
                "shio_key": shio_key,
                "name": shio_data["name"],
                "hanzi": shio_data["hanzi"],
                "status": status,
                "status_code": status_code,
                "message": message,
                "daily_tip": daily_tip,
                "element": element_name,
                "element_hanzi": element_hanzi,
                "element_relation": relation["name"],
                "element_relation_key": relation_key,
                "element_relation_code": relation["code"],
                "element_symbol": relation["symbol"],
                "element_desc": relation["desc"],
                "element_advice": relation["advice"],
            }
        )

    formatted_date = target_date.strftime("%d %B %Y")
    stem_name, stem_hanzi = HEAVENLY_STEMS[stem_idx]
    branch_name, branch_hanzi = EARTHLY_BRANCHES[shio_index]
    month_branch_name, month_branch_hanzi = EARTHLY_BRANCHES[month_branch]
    day_element_name, day_element_hanzi = ELEMENT_LABELS[day_element]

    return {
        "date_str": formatted_date,
        "today_shio_name": today_shio_data["name"],
        "today_shio_hanzi": today_shio_data["hanzi"],
        "day_pillar": f"{stem_name} {branch_name}",
        "day_pillar_hanzi": f"{stem_hanzi}{branch_hanzi}",
        "day_element": day_element_name,
        "day_element_hanzi": day_element_hanzi,
        "month_branch": month_branch_name,
        "month_branch_hanzi": month_branch_hanzi,
        "officer_name": officer["name"],
        "officer_hanzi": officer["hanzi"],
        "officer_code": officer["code"],
        "officer_meaning": officer["meaning"],
        "officer_yi": officer["yi"],
        "officer_ji": officer["ji"],
        "fortunes": results,
    }

def get_shio_guardian(shio_key):
    return SHIO_GUARDIAN_BANK.get(shio_key, {})

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

    relation_key = get_branch_relation(
        SHIOS_LIST.index(shio1_key), SHIOS_LIST.index(shio2_key)
    )
    meta = BRANCH_RELATION_META[relation_key]

    return {
        "shio1": {"name": s1_data["name"], "hanzi": s1_data["hanzi"]},
        "shio2": {"name": s2_data["name"], "hanzi": s2_data["hanzi"]},
        "relationship": meta["label"],
        "relation_key": relation_key,
        "relation_code": meta["code"],
        "score": compat.get("score", 50),
        "asmara": compat.get("asmara", ""),
        "bisnis": compat.get("bisnis", ""),
        "drama": compat.get("drama", ""),
        "tips": compat.get("tips", ""),
    }

def get_shio_yearly(user_shio_key, year):
    user_data = SHIO_DATA.get(user_shio_key)
    if not user_data:
        return {"error": f"Shio '{user_shio_key}' tidak ditemukan."}

    try:
        year = int(year)
    except (ValueError, TypeError):
        return {"error": "Tahun tidak valid."}

    year_idx = (year - 4) % 12
    year_shio_key = SHIOS_LIST[year_idx]
    year_data = SHIO_DATA.get(year_shio_key)
    pair_key = (user_shio_key, year_shio_key)
    yearly = SHIO_YEARLY_BANK.get(pair_key)

    if not yearly:
        return {
            "error": "Data ramalan tahunan belum tersedia untuk kombinasi ini.",
            "user_shio": {"name": user_data["name"], "hanzi": user_data["hanzi"]},
            "year_shio": {"name": year_data["name"], "hanzi": year_data["hanzi"]},
            "year": year,
        }

    return {
        "user_shio": {"name": user_data["name"], "hanzi": user_data["hanzi"]},
        "year_shio": {"name": year_data["name"], "hanzi": year_data["hanzi"]},
        "year": year,
        "karir": yearly.get("karir", ""),
        "keuangan": yearly.get("keuangan", ""),
        "asmara": yearly.get("asmara", ""),
        "kesehatan": yearly.get("kesehatan", ""),
        "saran_utama": yearly.get("saran_utama", ""),
    }

def get_shio_roasting(shio_key):
    roast = SHIO_ROASTING_BANK.get(shio_key)
    if not roast:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}
    return roast

def get_fortune_cookie(shio_key):
    cookies = SHIO_FORTUNE_COOKIE_BANK.get(shio_key)
    if not cookies:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}

    today = datetime.date.today()
    cycle, position = divmod(today.toordinal(), len(cookies))
    order = list(range(len(cookies)))
    random.Random(build_stable_seed("cookie", shio_key, cycle)).shuffle(order)

    if len(order) > 2:
        previous = list(range(len(cookies)))
        random.Random(build_stable_seed("cookie", shio_key, cycle - 1)).shuffle(
            previous
        )
        if order[0] == previous[-1]:
            order[0], order[1] = order[1], order[0]

    cookie = cookies[order[position]]
    return {
        "shio_key": shio_key,
        "message": cookie.get("message", ""),
        "lucky_item": cookie.get("lucky_item", ""),
    }
