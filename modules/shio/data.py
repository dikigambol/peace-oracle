import random
import datetime
import math
import zlib
import ephem
from .bank import (
    HEAVENLY_STEMS,
    EARTHLY_BRANCHES,
    STEM_ELEMENTS,
    STEM_POLARITY,
    BRANCH_ELEMENTS,
    ELEMENT_LABELS,
    ELEMENT_GENERATES,
    ELEMENT_CONTROLS,
    HIDDEN_STEMS,
    HIDDEN_STEM_WEIGHTS,
    TEN_GODS_TABLE,
    LIU_HE_PAIRS,
    LIU_PO_PAIRS,
    LIU_HAI_PAIRS,
    XIANG_XING_PAIRS,
    ZI_XING_BRANCHES,
    BRANCH_RELATION_META,
    JULIAN_DAY_OFFSET,
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
    PAIR_ELEMENT_DYNAMIC_BANK,
    PAIR_RELATION_BANK,
    DAY_PILLAR_RELATION_BANK,
    DAY_STEM_CONTEXT,
    USEFUL_GOD_MATCH_BANK,
    COUPLE_STAR_BANK,
    NAYIN_BANK,
    STEM_RELATION_BANK,
    STEM_NEUTRAL,
    NAYIN_RELATION_BANK,
    SHIO_YEARLY_BANK,
    YEARLY_RELATION_BANK,
    YEAR_STEM_LAYER_BANK,
    SHIO_ROASTING_BANK,
    SHIO_FORTUNE_COOKIE_BANK,
    DAY_MASTER_BANK,
    CHART_STRENGTH_BANK,
    TEN_GODS_BANK,
    WUXING_ANALYSIS_BANK,
    WUXING_ROLE_BANK,
    DESTINY_CAREER_BANK,
    DESTINY_WEALTH_BANK,
    DESTINY_LOVE_BANK,
    DESTINY_HEALTH_DAYMASTER,
    DESTINY_HEALTH_ELEMENT,
    SHEN_SHA_BANK,
    ELEMENT_REMEDY_BANK,
    LIFE_PHASE_BANK,
    PILLAR_POSITION_BANK,
    NO_BIRTH_TIME_BANK,
    IDENTITY_BANK,
)
from .bazi import (
    BIRTH_CITIES,
    get_year_pillar,
    get_month_branch,
    get_solar_longitude,
    get_day_pillar,
    build_four_pillars,
    classify_element_status,
    normalise_gender,
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

GUARDIAN_TRADITION = (
    "Buddhisme Esoterik Tionghoa (漢傳密教), sistem 八大本命佛 — delapan penjaga "
    "untuk dua belas shio, sehingga empat di antaranya dibagi oleh dua shio."
)

GUARDIAN_FENGSHUI_NOTE = (
    "Saran feng shui berikut adalah pelengkap budaya Tionghoa, bukan ajaran Buddhis. "
    "Keduanya sistem yang berbeda dan sengaja tidak dicampur."
)

GUARDIAN_PRAY_TIME_NOTE = (
    "Jam ini selaras dengan 時辰 shio-mu. Ini konvensi penanggalan Tionghoa, "
    "bukan ketentuan dalam praktik 本命佛."
)


def get_shio_guardian(shio_key):
    guardian = SHIO_GUARDIAN_BANK.get(shio_key)
    if not guardian:
        return {}
    element = BRANCH_ELEMENTS[SHIOS_LIST.index(shio_key)]
    return {
        **guardian,
        "shio_element": ELEMENT_LABELS[element][0],
        "shio_element_hanzi": ELEMENT_LABELS[element][1],
        "tradition": GUARDIAN_TRADITION,
        "feng_shui_note": GUARDIAN_FENGSHUI_NOTE,
        "pray_time_note": GUARDIAN_PRAY_TIME_NOTE,
    }

def get_element_role_pair(element_a, element_b):
    if element_a == element_b:
        return "setara"
    if ELEMENT_GENERATES[element_a] == element_b:
        return "memberi"
    if ELEMENT_GENERATES[element_b] == element_a:
        return "menerima"
    if ELEMENT_CONTROLS[element_a] == element_b:
        return "menekan"
    return "ditekan"


def describe_element_side(self_key, other_key):
    self_element = BRANCH_ELEMENTS[SHIOS_LIST.index(self_key)]
    other_element = BRANCH_ELEMENTS[SHIOS_LIST.index(other_key)]
    role = get_element_role_pair(self_element, other_element)
    entry = PAIR_ELEMENT_DYNAMIC_BANK[role]
    fields = {
        "self": SHIO_DATA[self_key]["name"],
        "other": SHIO_DATA[other_key]["name"],
        "self_element": ELEMENT_LABELS[self_element][0],
        "other_element": ELEMENT_LABELS[other_element][0],
    }
    return {
        "shio": fields["self"],
        "hanzi": SHIO_DATA[self_key]["hanzi"],
        "element": fields["self_element"],
        "element_hanzi": ELEMENT_LABELS[self_element][1],
        "role": role,
        "label": entry["label"],
        "arrow": entry["arrow"],
        "icon": entry["icon"],
        "summary": entry["summary"].format(**fields),
        "advice": entry["advice"].format(**fields),
    }


def get_pair_element_dynamic(key_a, key_b):
    if key_a not in SHIO_DATA or key_b not in SHIO_DATA:
        return None
    return {
        "for_shio1": describe_element_side(key_a, key_b),
        "for_shio2": describe_element_side(key_b, key_a),
        "symmetric": BRANCH_ELEMENTS[SHIOS_LIST.index(key_a)]
        == BRANCH_ELEMENTS[SHIOS_LIST.index(key_b)],
    }


def get_sexagenary_index(stem, branch):
    if (branch - stem) % 2:
        return None
    step = (5 * ((branch - stem) // 2)) % 6
    return (stem + 10 * step) % 60


def describe_year_pillar(birth_date):
    stem, branch = get_year_pillar(birth_date)
    index = get_sexagenary_index(stem, branch)
    nayin = NAYIN_BANK[index // 2]
    return {
        "date": birth_date.isoformat(),
        "stem_index": stem,
        "branch_index": branch,
        "pillar_hanzi": HEAVENLY_STEMS[stem][1] + EARTHLY_BRANCHES[branch][1],
        "stem_hanzi": HEAVENLY_STEMS[stem][1],
        "shio_key": SHIOS_LIST[branch],
        "shio_name": SHIO_DATA[SHIOS_LIST[branch]]["name"],
        "nayin": dict(nayin),
    }


def describe_nayin_side(self_pillar, other_pillar):
    role = get_element_role_pair(
        self_pillar["nayin"]["element"], other_pillar["nayin"]["element"]
    )
    text = NAYIN_RELATION_BANK[role].format(
        element=ELEMENT_LABELS[self_pillar["nayin"]["element"]][0],
        self_name=self_pillar["nayin"]["name"],
        other_name=other_pillar["nayin"]["name"],
    )
    return {"role": role, "text": text}


def get_year_layer(date1, date2, picked1, picked2):
    if date1 is None or date2 is None:
        return None

    pillar1 = describe_year_pillar(date1)
    pillar2 = describe_year_pillar(date2)

    stem_pair = tuple(sorted((pillar1["stem_index"], pillar2["stem_index"])))
    stem_relation = dict(STEM_RELATION_BANK.get(stem_pair, STEM_NEUTRAL))

    corrections = [
        {
            "picked": SHIO_DATA[picked]["name"],
            "actual": pillar["shio_name"],
            "pillar": pillar["pillar_hanzi"],
            "date": pillar["date"],
        }
        for picked, pillar in ((picked1, pillar1), (picked2, pillar2))
        if picked != pillar["shio_key"]
    ]

    return {
        "shio1": {**pillar1, "nayin_relation": describe_nayin_side(pillar1, pillar2)},
        "shio2": {**pillar2, "nayin_relation": describe_nayin_side(pillar2, pillar1)},
        "stem_relation": stem_relation,
        "corrections": corrections,
        "lichun_note": (
            "Tahun Imlek berganti di 立春 (sekitar 4 Februari), bukan 1 Januari. "
            "Kelahiran Januari sampai awal Februari masuk pilar tahun sebelumnya."
        ),
    }


SOLITUDE_STARS = ("gu_chen", "gua_su")

BAZI_LAYER_NOTE = (
    "Lapisan ini dihitung dari pilar hari (日柱) kedua tanggal, bukan dari "
    "shionya. Di 合婚 klasik justru pilar hari inilah yang dibaca lebih dulu, "
    "karena cabang hari adalah istana pasangan (夫妻宮). Halaman ini cuma "
    "meminta tanggal, jadi hitungannya memakai tiga pilar — sah dibaca, tapi "
    "lapisan jam tidak ikut."
)


def pair_side_labels(name1, name2):
    if name1 != name2:
        return name1, name2
    return name1 + " (pertama)", name2 + " (kedua)"


def describe_day_pillar_match(chart1, chart2):
    day1 = chart1["day"]
    day2 = chart2["day"]
    relation_key = get_branch_relation(day1["branch_index"], day2["branch_index"])
    meta = PAIR_RELATION_BANK[relation_key]
    stem_meta = STEM_RELATION_BANK.get(
        tuple(sorted((day1["stem_index"], day2["stem_index"]))), STEM_NEUTRAL
    )
    return {
        "pillar1": day1["pillar_hanzi"],
        "pillar2": day2["pillar_hanzi"],
        "branch1": day1["branch_hanzi"],
        "branch2": day2["branch_hanzi"],
        "relation_key": relation_key,
        "label": meta["label"],
        "hanzi": meta["hanzi"],
        "title": meta["title"],
        "code": meta["code"],
        "text": DAY_PILLAR_RELATION_BANK[relation_key],
        "stem_kind": stem_meta["kind"],
        "stem_hanzi": stem_meta["hanzi"],
        "stem_text": DAY_STEM_CONTEXT[stem_meta["kind"]].format(
            hanzi=stem_meta["hanzi"]
        ),
    }


def describe_useful_god_side(label, chart, own_element, other_element,
                             other_gods):
    return {
        "label": label,
        "pillar": chart["day"]["pillar_hanzi"],
        "element": ELEMENT_LABELS[own_element][0],
        "element_hanzi": ELEMENT_LABELS[own_element][1],
        "strength": chart["strength"]["key"],
        "needs": list(chart["useful_gods"]["favourable"]),
        "avoids": list(chart["useful_gods"]["unfavourable"]),
        "supplies": own_element in other_gods["favourable_keys"],
        "burdens": own_element in other_gods["unfavourable_keys"],
    }


def describe_useful_god_match(chart1, chart2, label1, label2):
    element1 = STEM_ELEMENTS[chart1["day"]["stem_index"]]
    element2 = STEM_ELEMENTS[chart2["day"]["stem_index"]]
    gods1 = chart1["useful_gods"]
    gods2 = chart2["useful_gods"]

    supplies_to2 = element1 in gods2["favourable_keys"]
    supplies_to1 = element2 in gods1["favourable_keys"]
    burdens_to2 = element1 in gods2["unfavourable_keys"]
    burdens_to1 = element2 in gods1["unfavourable_keys"]

    if supplies_to1 and supplies_to2:
        key = "saling_memasok"
    elif burdens_to1 and burdens_to2:
        key = "saling_menguras"
    elif (supplies_to2 and burdens_to1) or (supplies_to1 and burdens_to2):
        key = "timpang"
    elif supplies_to1 or supplies_to2:
        key = "sepihak"
    else:
        key = "netral"

    giver, receiver = (label1, label2) if supplies_to2 else (label2, label1)
    entry = USEFUL_GOD_MATCH_BANK[key]

    return {
        "key": key,
        "title": entry["title"],
        "code": entry["code"],
        "note": entry["note"].format(
            a=label1, b=label2, giver=giver, receiver=receiver
        ),
        "advice": entry["advice"],
        "side1": describe_useful_god_side(
            label1, chart1, element1, element2, gods2
        ),
        "side2": describe_useful_god_side(
            label2, chart2, element2, element1, gods1
        ),
    }


def collect_shen_sha_keys(chart):
    return {item["key"] for item in chart["shen_sha"]}


def describe_couple_stars(chart1, chart2, label1, label2):
    keys1 = collect_shen_sha_keys(chart1)
    keys2 = collect_shen_sha_keys(chart2)
    stars = []

    def push(bank_key, who):
        entry = COUPLE_STAR_BANK[bank_key]
        stars.append({
            "key": bank_key,
            "icon": entry["icon"],
            "title": entry["title"],
            "code": entry["code"],
            "note": entry["note"],
            "who": who,
        })

    def resolve(flag1, flag2, both_key, one_key):
        if flag1 and flag2:
            push(both_key, label1 + " & " + label2)
        elif flag1 or flag2:
            push(one_key, label1 if flag1 else label2)

    resolve("tao_hua" in keys1, "tao_hua" in keys2,
            "tao_hua_both", "tao_hua_one")
    resolve(bool(keys1.intersection(SOLITUDE_STARS)),
            bool(keys2.intersection(SOLITUDE_STARS)),
            "solitude_both", "solitude_one")

    tian_yi1 = "tian_yi" in keys1
    tian_yi2 = "tian_yi" in keys2
    if tian_yi1 and tian_yi2:
        push("tian_yi", label1 + " & " + label2)
    elif tian_yi1 or tian_yi2:
        push("tian_yi", label1 if tian_yi1 else label2)

    return stars


def get_bazi_layer(date1, date2, name1, name2):
    if date1 is None or date2 is None:
        return None

    chart1 = build_four_pillars(date1)
    chart2 = build_four_pillars(date2)
    label1, label2 = pair_side_labels(name1, name2)

    return {
        "note": BAZI_LAYER_NOTE,
        "day_pillar": describe_day_pillar_match(chart1, chart2),
        "useful_god": describe_useful_god_match(chart1, chart2, label1, label2),
        "couple_stars": describe_couple_stars(chart1, chart2, label1, label2),
    }


def get_shio_compatibility(shio1_key, shio2_key,
                           birth1=None, birth2=None):
    date1 = parse_birth_date(birth1) if birth1 else None
    date2 = parse_birth_date(birth2) if birth2 else None
    if birth1 and date1 is None:
        return {"error": "Tanggal lahir pertama tidak valid."}
    if birth2 and date2 is None:
        return {"error": "Tanggal lahir kedua tidak valid."}

    picked1, picked2 = shio1_key, shio2_key
    if date1 is not None and date2 is not None:
        shio1_key = SHIOS_LIST[get_year_pillar(date1)[1]]
        shio2_key = SHIOS_LIST[get_year_pillar(date2)[1]]

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
        "pair_relation": dict(PAIR_RELATION_BANK[relation_key]),
        "element_dynamic": get_pair_element_dynamic(shio1_key, shio2_key),
        "year_layer": get_year_layer(date1, date2, picked1, picked2),
        "bazi_layer": get_bazi_layer(
            date1, date2, s1_data["name"], s2_data["name"]
        ),
    }

YEARLY_LICHUN_NOTE = (
    "Tahun Imlek berganti di 立春, sekitar 4 Februari — bukan 1 Januari. "
    "Kelahiran maupun peristiwa di awal Januari masih masuk hitungan tahun sebelumnya."
)


def get_current_imlek_year(today=None):
    moment = today or datetime.datetime.now(ALMANAC_TZ).date()
    branch = get_month_branch(moment)
    year = moment.year
    if moment.month <= 2 and branch in (0, 1):
        year -= 1
    return year


def describe_year_stem_layer(user_shio_key, year):
    stem = (year - 4) % 10
    branch = (year - 4) % 12
    year_element = STEM_ELEMENTS[stem]
    shio_element = BRANCH_ELEMENTS[SHIOS_LIST.index(user_shio_key)]
    role = get_element_role_pair(shio_element, year_element)
    entry = YEAR_STEM_LAYER_BANK[role]
    fields = {
        "shio": SHIO_DATA[user_shio_key]["name"],
        "shio_element": ELEMENT_LABELS[shio_element][0],
        "year_element": ELEMENT_LABELS[year_element][0],
        "year_pillar": HEAVENLY_STEMS[stem][1] + EARTHLY_BRANCHES[branch][1],
    }
    return {
        "role": role,
        "title": entry["title"],
        "year_pillar": fields["year_pillar"],
        "year_element": fields["year_element"],
        "shio_element": fields["shio_element"],
        "summary": entry["summary"].format(**fields),
        "advice": entry["advice"].format(**fields),
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

    relation_key = get_branch_relation(
        SHIOS_LIST.index(user_shio_key), year_idx
    )
    relation = YEARLY_RELATION_BANK[relation_key]

    return {
        "user_shio": {"name": user_data["name"], "hanzi": user_data["hanzi"]},
        "year_shio": {"name": year_data["name"], "hanzi": year_data["hanzi"]},
        "year": year,
        "relation": {"key": relation_key, **relation},
        "stem_layer": describe_year_stem_layer(user_shio_key, year),
        "lichun_note": YEARLY_LICHUN_NOTE,
        "karir": yearly.get("karir", ""),
        "keuangan": yearly.get("keuangan", ""),
        "asmara": yearly.get("asmara", ""),
        "kesehatan": yearly.get("kesehatan", ""),
        "saran_utama": yearly.get("saran_utama", ""),
    }

ROAST_TRAITS_PER_DRAW = 8


def get_shio_roasting(shio_key):
    roast = SHIO_ROASTING_BANK.get(shio_key)
    if not roast:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}
    return {
        **roast,
        "traits_per_draw": ROAST_TRAITS_PER_DRAW,
    }

COOKIE_ELEMENT_RULE = {
    "bi_he": "wo_sheng",
    "sheng_wo": "day",
    "wo_sheng": "resource",
    "ke_wo": "resource",
    "wo_ke": "self",
}

COOKIE_ELEMENT_REASON = {
    "bi_he": "Elemen hari sama dengan elemenmu, jadi kelebihannya perlu disalurkan keluar.",
    "sheng_wo": "Elemen hari sedang menghidupimu, jadi ikut arusnya saja.",
    "wo_sheng": "Kamu yang menghidupi hari ini, jadi isi ulang dari sumbermu sendiri.",
    "ke_wo": "Hari ini menekanmu, dan elemen inilah yang menjembatani tekanannya jadi dukungan.",
    "wo_ke": "Kamu yang memegang kendali hari ini, jadi perkuat saja elemenmu sendiri.",
}


def pick_cookie_element(relation_key, day_element, shio_element):
    rule = COOKIE_ELEMENT_RULE[relation_key]
    if rule == "day":
        return day_element
    if rule == "self":
        return shio_element
    if rule == "wo_sheng":
        return ELEMENT_GENERATES[shio_element]
    return next(e for e in ELEMENT_GENERATES if ELEMENT_GENERATES[e] == shio_element)


def describe_cookie_day(shio_key, target_date):
    stem_index, day_branch = get_day_pillar(target_date)
    shio_index = SHIOS_LIST.index(shio_key)

    branch_key = get_branch_relation(day_branch, shio_index)
    branch_label, _messages = DAILY_RELATION_VIEW[branch_key]
    branch_code = BRANCH_RELATION_META[branch_key]["code"]

    day_element = STEM_ELEMENTS[stem_index]
    shio_element = BRANCH_ELEMENTS[shio_index]
    element_key, element_meta = get_element_relation(day_element, shio_element)

    lucky_element = pick_cookie_element(element_key, day_element, shio_element)
    remedy = ELEMENT_REMEDY_BANK[lucky_element]

    return {
        "date": target_date.isoformat(),
        "pillar_hanzi": HEAVENLY_STEMS[stem_index][1] + EARTHLY_BRANCHES[day_branch][1],
        "day_element": ELEMENT_LABELS[day_element][0],
        "shio_element": ELEMENT_LABELS[shio_element][0],
        "branch": {
            "key": branch_key,
            "label": branch_label,
            "code": branch_code,
        },
        "element": {
            "key": element_key,
            "name": element_meta["name"],
            "code": element_meta["code"],
            "symbol": element_meta["symbol"],
            "desc": element_meta["desc"],
            "advice": element_meta["advice"],
        },
        "lucky": {
            "element": ELEMENT_LABELS[lucky_element][0],
            "reason": COOKIE_ELEMENT_REASON[element_key],
            "colors": remedy["colors"],
            "directions": remedy["directions"],
            "numbers": remedy["numbers"],
        },
    }


def pick_day_tone(energy):
    branch_code = energy["branch"]["code"]
    if branch_code != "neutral":
        return branch_code
    return energy["element"]["code"]


def rotate_pool(pool, shio_key, tone, ordinal):
    cycle, position = divmod(ordinal, len(pool))
    order = list(range(len(pool)))
    random.Random(build_stable_seed("cookie-" + tone, shio_key, cycle)).shuffle(order)

    if len(order) > 2:
        previous = list(range(len(pool)))
        random.Random(
            build_stable_seed("cookie-" + tone, shio_key, cycle - 1)
        ).shuffle(previous)
        if order[0] == previous[-1]:
            order[0], order[1] = order[1], order[0]

    return pool[order[position]]


def get_fortune_cookie(shio_key, client_date_str=None):
    cookies = SHIO_FORTUNE_COOKIE_BANK.get(shio_key)
    if not cookies:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}

    today = resolve_almanac_date(client_date_str)
    energy = describe_cookie_day(shio_key, today)
    tone = pick_day_tone(energy)

    pool = [c for c in cookies if c.get("tone") == tone] or cookies
    cookie = rotate_pool(pool, shio_key, tone, today.toordinal())

    return {
        "shio_key": shio_key,
        "message": cookie.get("message", ""),
        "lucky_item": cookie.get("lucky_item", ""),
        "tone": tone,
        "day_energy": energy,
    }


DESTINY_SCHOOL = "子平 (Zi Ping)"

DESTINY_EARLIEST_YEAR = 1900

DESTINY_CITIES = [
    {"key": key, "name": name}
    for key, (name, _longitude) in sorted(
        BIRTH_CITIES.items(), key=lambda item: item[1][0]
    )
]

DESTINY_DISCLAIMER = (
    "Bacaan ini disusun dari kalkulasi Ba Zi dan ditujukan untuk hiburan serta "
    "bahan refleksi. Bagian kesehatan bukan diagnosis dan tidak menggantikan "
    "pemeriksaan tenaga medis."
)

LUNAR_MONTH_LABELS = [
    "Imlek 1 (寅)", "Imlek 2 (卯)", "Imlek 3 (辰)", "Imlek 4 (巳)",
    "Imlek 5 (午)", "Imlek 6 (未)", "Imlek 7 (申)", "Imlek 8 (酉)",
    "Imlek 9 (戌)", "Imlek 10 (亥)", "Imlek 11 (子)", "Imlek 12 (丑)",
]


def parse_birth_date(value):
    if not isinstance(value, str):
        return None
    try:
        parsed = datetime.date.fromisoformat(value.strip())
    except (ValueError, AttributeError):
        return None
    if parsed.year < DESTINY_EARLIEST_YEAR:
        return None
    if parsed > datetime.datetime.now(ALMANAC_TZ).date():
        return None
    return parsed


DESTINY_UNSET = object()


def parse_clock_part(value, ceiling):
    if value is None or value == "":
        return None
    try:
        number = int(value)
    except (TypeError, ValueError):
        return DESTINY_UNSET
    return number if 0 <= number <= ceiling else DESTINY_UNSET


def describe_pillar_row(chart, slot):
    pillar = chart[slot]
    position = PILLAR_POSITION_BANK[slot]
    if pillar is None:
        return {
            "slot": slot,
            "available": False,
            "hanzi": position["hanzi"],
            "label": position["label"],
            "domain": position["domain"],
            "age_range": position["age_range"],
            "reading_note": position["reading_note"],
        }

    gods = chart["ten_gods"][slot]
    hidden = [
        {"hanzi": HEAVENLY_STEMS[stem][1], "name": HEAVENLY_STEMS[stem][0],
         "element": ELEMENT_LABELS[STEM_ELEMENTS[stem]][0],
         "god": gods["hidden"][index]}
        for index, stem in enumerate(HIDDEN_STEMS[pillar["branch_index"]])
    ]
    return {
        "slot": slot,
        "available": True,
        "hanzi": position["hanzi"],
        "label": position["label"],
        "domain": position["domain"],
        "age_range": position["age_range"],
        "reading_note": position["reading_note"],
        "pillar_hanzi": pillar["pillar_hanzi"],
        "stem_hanzi": pillar["stem_hanzi"],
        "stem": pillar["stem"],
        "stem_element": pillar["stem_element"],
        "stem_polarity": pillar["stem_polarity"],
        "branch_hanzi": pillar["branch_hanzi"],
        "branch": pillar["branch"],
        "branch_element": pillar["branch_element"],
        "stem_god": gods["stem"],
        "hidden_stems": hidden,
    }


def describe_elements(chart):
    tally = chart["element_tally"]
    total = sum(tally.values())
    favourable = set(chart["useful_gods"]["favourable_keys"])
    unfavourable = set(chart["useful_gods"]["unfavourable_keys"])

    rows = []
    for key, score in tally.items():
        status = classify_element_status(score, total)
        if key in favourable:
            role = "menguntungkan"
        elif key in unfavourable:
            role = "merugikan"
        else:
            role = "netral"

        analysis = WUXING_ANALYSIS_BANK.get((key, status))
        verdict = WUXING_ROLE_BANK.get((status, role))
        rows.append(
            {
                "key": key,
                "label": ELEMENT_LABELS[key][0],
                "hanzi": ELEMENT_LABELS[key][1],
                "score": round(score, 2),
                "share": round(score / total, 3) if total else 0.0,
                "status": status,
                "role": role,
                "status_label": analysis["status_label"] if analysis else "",
                "impact": analysis["impact"] if analysis else "",
                "remedy": analysis["remedy"] if analysis else "",
                "verdict": verdict["verdict"] if verdict else "",
                "action": verdict["action"] if verdict else "",
            }
        )
    rows.sort(key=lambda row: -row["score"])
    return rows


def describe_shen_sha(chart):
    return [
        {
            **SHEN_SHA_BANK[star["key"]],
            "key": star["key"],
            "slots": [PILLAR_POSITION_BANK[slot]["label"] for slot in star["slots"]],
        }
        for star in chart["shen_sha"]
    ]


def describe_luck(chart):
    luck = chart["luck"]
    if not luck:
        return None
    pillars = []
    for pillar in luck["pillars"]:
        phase = LIFE_PHASE_BANK[pillar["dominant_god"]["key"]]
        pillars.append(
            {
                "order": pillar["order"],
                "age_from": pillar["age_from"],
                "age_to": pillar["age_to"],
                "year_from": pillar["year_from"],
                "year_to": pillar["year_to"],
                "pillar_hanzi": pillar["pillar_hanzi"],
                "stem_god": pillar["stem_god"],
                "dominant_god": pillar["dominant_god"],
                "phase_name": phase["phase_name"],
                "description": phase["description"],
                "advice": phase["advice"],
            }
        )
    return {
        "direction": luck["direction"],
        "start_age_years": luck["start_age_years"],
        "start_age_months": luck["start_age_months"],
        "pillars": pillars,
    }


def describe_heritage(chart):
    shio_key = SHIOS_LIST[chart["year"]["branch_index"]]
    identity = IDENTITY_BANK[shio_key]
    relation = chart["year_branch_relation"]
    return {
        "shio_key": shio_key,
        "shio_name": SHIO_DATA[shio_key]["name"],
        "shio_hanzi": SHIO_DATA[shio_key]["hanzi"],
        "icon": identity["icon"],
        "branch_hanzi": chart["year"]["branch_hanzi"],
        "branch_element": chart["year"]["branch_element"],
        "persona": identity["personality_long"],
        "traits_positive": identity["traits_positive"],
        "traits_negative": identity["traits_negative"],
        "green_flags": identity["green_flags"],
        "red_flags": identity["red_flags"],
        "alter_ego": identity["alter_ego"][STEM_ELEMENTS[chart["year"]["stem_index"]]],
        "famous_people": identity["famous_people"],
        "lucky_flowers": identity["lucky_flowers"],
        "unlucky_colors": identity["unlucky_colors"],
        "unlucky_numbers": identity["unlucky_numbers"],
        "best_months": [LUNAR_MONTH_LABELS[m - 1] for m in identity["best_months"]],
        "worst_months": [LUNAR_MONTH_LABELS[m - 1] for m in identity["worst_months"]],
        "relation_key": relation["key"],
        "relation_text": identity["relation_to_day_master"][relation["key"]],
        "spirit_advice": identity["spirit_advice"],
    }


def describe_remedy(chart):
    return [
        {"element": ELEMENT_LABELS[key][0], **ELEMENT_REMEDY_BANK[key]}
        for key in chart["useful_gods"]["favourable_keys"]
    ]


def get_shio_destiny(birth_date_str, birth_hour=None, birth_minute=None,
                    city_key=None, gender=None):
    birth_date = parse_birth_date(birth_date_str)
    if birth_date is None:
        return {"error": "Tanggal lahir tidak valid."}

    hour = parse_clock_part(birth_hour, 23)
    if hour is DESTINY_UNSET:
        return {"error": "Jam lahir harus angka 0 sampai 23."}

    minute = parse_clock_part(birth_minute, 59)
    if minute is DESTINY_UNSET:
        return {"error": "Menit lahir harus angka 0 sampai 59."}
    minute = minute or 0

    resolved_gender = normalise_gender(gender)
    if gender not in (None, "") and resolved_gender is None:
        return {"error": "Jenis kelamin harus 'pria' atau 'wanita'."}

    chart = build_four_pillars(birth_date, hour, minute, city_key, gender)

    stem_key = HEAVENLY_STEMS[chart["day"]["stem_index"]][0].lower()
    day_master = DAY_MASTER_BANK[stem_key]
    strength = chart["strength"]
    strength_bank = CHART_STRENGTH_BANK[strength["key"]]
    dominant = chart["dominant_ten_god"]
    god_bank = TEN_GODS_BANK[dominant["key"]]

    is_strong = strength["key"] in ("shen_qiang", "cong_qiang")

    return {
        "meta": {
            "school": DESTINY_SCHOOL,
            "birth_date": birth_date.isoformat(),
            "birth_hour": hour,
            "birth_minute": minute if hour is not None else None,
            "gender": resolved_gender,
            "pillar_count": chart["pillar_count"],
            "has_hour": chart["has_hour"],
            "city": chart["city"],
            "true_solar_offset_minutes": chart["true_solar_offset_minutes"],
            "disclaimer": DESTINY_DISCLAIMER,
        },
        "pillars": [describe_pillar_row(chart, slot)
                    for slot in ("year", "month", "day", "hour")],
        "day_master": {
            "hanzi": chart["day_master"]["hanzi"],
            "name": chart["day_master"]["name"],
            "element": day_master["element"],
            "polarity": day_master["polarity"],
            "title": day_master["title"],
            "personality": day_master["personality"],
            "strengths": day_master["strengths"],
            "weaknesses": day_master["weaknesses"],
            "variant": day_master["when_strong"] if is_strong else day_master["when_weak"],
            "nuance": day_master["nuance"],
        },
        "strength": {
            "key": strength["key"],
            "label": strength_bank["label"],
            "hanzi": strength_bank["hanzi"],
            "title": strength_bank["title"],
            "summary": strength_bank["summary"],
            "advice": strength_bank["advice"],
            "caution": strength_bank["caution"],
            "support_ratio": strength["support_ratio"],
            "day_element": strength["day_element"],
            "resource_element": strength["resource_element"],
        },
        "useful_gods": {
            "favourable": chart["useful_gods"]["favourable"],
            "unfavourable": chart["useful_gods"]["unfavourable"],
        },
        "elements": describe_elements(chart),
        "dominant_god": {
            **god_bank,
            "key": dominant["key"],
            "share": dominant["share"],
            "decisive": dominant["decisive"],
            "variant": god_bank["when_strong"] if is_strong else god_bank["when_weak"],
        },
        "destiny": {
            "career": DESTINY_CAREER_BANK[dominant["key"]],
            "wealth": DESTINY_WEALTH_BANK[dominant["key"]],
            "love": DESTINY_LOVE_BANK[dominant["key"]],
            "health": {
                **DESTINY_HEALTH_DAYMASTER[stem_key],
                "organs": [
                    {"element": ELEMENT_LABELS[row["key"]][0],
                     **DESTINY_HEALTH_ELEMENT[row["key"]]}
                    for row in describe_elements(chart)
                    if row["status"] in ("lemah", "kosong")
                ],
            },
        },
        "remedy": describe_remedy(chart),
        "shen_sha": describe_shen_sha(chart),
        "luck": describe_luck(chart),
        "heritage": describe_heritage(chart),
        "no_birth_time": None if chart["has_hour"] else NO_BIRTH_TIME_BANK,
    }
