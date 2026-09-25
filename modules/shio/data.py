import collections
import datetime
import hashlib
import json
import math
import random
import re
import secrets
import sqlite3
import unicodedata
import zlib
from contextlib import contextmanager
from itertools import combinations

import ephem
from .bank import (
    BIRTH_CITIES,
    TIME_ZONE_MERIDIANS,
    DEFAULT_CITY,
    CITY_ALIASES,
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
    JULIAN_DAY_OFFSET,
    SHEN_SHA_BANK,
    TIAN_YI_BY_STEM,
    WEN_CHANG_BY_STEM,
    LU_SHEN_BY_STEM,
    YANG_REN_BY_STEM,
    JIN_YU_BY_STEM,
    SAN_HE_GROUP,
    LIU_HE_PAIRS,
    LIU_PO_PAIRS,
    LIU_HAI_PAIRS,
    XIANG_XING_PAIRS,
    ZI_XING_BRANCHES,
    TAO_HUA_BY_GROUP,
    YI_MA_BY_GROUP,
    HUA_GAI_BY_GROUP,
    YUE_DE_BY_GROUP,
    TIAN_DE_BY_MONTH,
    GU_GUA_BY_YEAR,
    BRANCH_RELATION_META,
    DAY_OFFICER_BANK,
    ELEMENT_RELATION_BANK,
    DAILY_RANK_STATUS_WEIGHT,
    DAILY_RANK_ELEMENT_WEIGHT,
    DAILY_RANK_TIERS,
    DAILY_RANK_NOTE,
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
    ROAST_PAIR_BANK,
    ROAST_DAY_MASTER_BANK,
    ROAST_DIRECTION_BANK,
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
    ELEMENT_REMEDY_BANK,
    LIFE_PHASE_BANK,
    PILLAR_POSITION_BANK,
    CHART_RELATION_BANK,
    CHART_RELATION_REACH,
    CHART_RELATION_CLASH_NOTE,
    SAN_HE_ELEMENT,
    NO_BIRTH_TIME_BANK,
    IDENTITY_BANK,
    RELATION_LENS,
    NEUTRAL_RELATION_LABELS,
    NEUTRAL_BAZI_LAYER_NOTE,
    NEUTRAL_DAY_PILLAR_RELATION_BANK,
    NEUTRAL_USEFUL_GOD_NOTES,
    NEUTRAL_COUPLE_STARS,
    GROUP_ROLE_BANK,
    GROUP_VERDICT_BANK,
    PAIR_QUIZ_QUESTIONS,
    PAIR_VERDICT_BANK,
    GUESS_VERDICT_BANK,
    QUIZ_MODE_BANK,
    GUESS_FLAVOR_BANK,
    PAIR_LENS_QUESTION_IDS,
    LEGACY_PAIR_QUESTION_IDS,
    GUESS_STOPWORDS,
    GUESS_SIGNATURE_TRAITS,
    GUESS_EXTRA_TRAITS,
)

TEN_GOD_LABELS = {
    "bi_jian": ("Bi Jian", "比肩", "Saudara Sebaya"),
    "jie_cai": ("Jie Cai", "劫財", "Perampas Harta"),
    "shi_shen": ("Shi Shen", "食神", "Dewa Penikmat"),
    "shang_guan": ("Shang Guan", "傷官", "Pelukai Pejabat"),
    "pian_cai": ("Pian Cai", "偏財", "Harta Tak Terduga"),
    "zheng_cai": ("Zheng Cai", "正財", "Harta Sah"),
    "qi_sha": ("Qi Sha", "七殺", "Tujuh Pembunuh"),
    "zheng_guan": ("Zheng Guan", "正官", "Pejabat Sah"),
    "pian_yin": ("Pian Yin", "偏印", "Penopang Miring"),
    "zheng_yin": ("Zheng Yin", "正印", "Penopang Sah"),
}

TEN_GOD_ORDER = {key: index for index, key in enumerate(TEN_GOD_LABELS)}

YEAR_BRANCH_RELATION_KEYS = {
    "sama": "sama",
    "menghidupi_dm": "sheng",
    "mengekang_dm": "ke",
    "dm_menghidupi": "diserap",
    "dm_mengekang": "dikuasai",
}

DOMINANT_GOD_MARGIN = 0.3

MONTH_COMMAND_BONUS = 1.5

STRENGTH_THRESHOLDS = [
    (0.167, "cong_ruo"),
    (0.389, "shen_ruo"),
    (0.571, "zhong_he"),
    (0.817, "shen_qiang"),
]

WIB = datetime.timezone(datetime.timedelta(hours=7), "WIB")

LICHUN_LONGITUDE = 315.0

MONTH_BRANCH_YIN = 2


WIB_OFFSET_HOURS = 7

DEFAULT_ZONE = "WIB"

ZONE_OFFSET_HOURS = {"WIB": 7, "WITA": 8, "WIT": 9}


def get_zone_offset_hours(zone):
    return ZONE_OFFSET_HOURS.get(zone, WIB_OFFSET_HOURS)


def get_solar_longitude(moment):
    epoch = ephem.Date(moment)
    sun = ephem.Sun()
    sun.compute(epoch)
    apparent = ephem.Equatorial(sun.ra, sun.dec, epoch=epoch)
    return math.degrees(float(ephem.Ecliptic(apparent, epoch=epoch).lon)) % 360


def as_local_moment(target):
    if isinstance(target, datetime.datetime):
        return target
    return datetime.datetime(target.year, target.month, target.day, 12, 0)


def get_month_branch(target, zone=DEFAULT_ZONE):
    local = as_local_moment(target)
    utc = local - datetime.timedelta(hours=get_zone_offset_hours(zone))
    longitude = get_solar_longitude(utc)
    return (int((longitude - LICHUN_LONGITUDE) % 360 // 30) + MONTH_BRANCH_YIN) % 12


def get_day_pillar(target_date):
    jdn = target_date.toordinal() + JULIAN_DAY_OFFSET
    return (jdn + 9) % 10, (jdn + 1) % 12


def get_year_pillar(target, zone=DEFAULT_ZONE):
    month_branch = get_month_branch(target, zone)
    local = as_local_moment(target)
    year = local.year

    if local.month <= 2 and month_branch in (0, 1):
        year -= 1

    return (year - 4) % 10, (year - 4) % 12


def get_month_pillar(target, year_stem, zone=DEFAULT_ZONE):
    branch = get_month_branch(target, zone)
    first_stem = ((year_stem % 5) * 2 + 2) % 10
    offset = (branch - MONTH_BRANCH_YIN) % 12
    return (first_stem + offset) % 10, branch


def get_equation_of_time(moment):
    day_of_year = moment.timetuple().tm_yday
    angle = 2 * math.pi * (day_of_year - 81) / 365.2422
    return (
        9.87 * math.sin(2 * angle)
        - 7.53 * math.cos(angle)
        - 1.5 * math.sin(angle)
    )


def normalise_city_text(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


BARE_NAME_COUNT = collections.Counter(
    normalise_city_text(_row[0].split(",")[0]) for _row in BIRTH_CITIES.values()
)

CITY_LOOKUP = {}
for _key, _row in BIRTH_CITIES.items():
    CITY_LOOKUP[normalise_city_text(_key)] = _key
    CITY_LOOKUP.setdefault(normalise_city_text(_row[0]), _key)
    _bare = normalise_city_text(_row[0].split(",")[0])
    if BARE_NAME_COUNT[_bare] == 1:
        CITY_LOOKUP.setdefault(_bare, _key)

for _alias, _target in CITY_ALIASES.items():
    CITY_LOOKUP[normalise_city_text(_alias)] = _target


def resolve_city(value):
    if not value:
        return None
    return CITY_LOOKUP.get(normalise_city_text(value))


def get_true_solar_offset(moment, city_longitude, zone_meridian):
    longitude_minutes = (city_longitude - zone_meridian) * 4
    return longitude_minutes + get_equation_of_time(moment)


def get_hour_branch(hour):
    return ((hour + 1) // 2) % 12


def get_hour_pillar(day_stem, hour_branch):
    first_stem = ((day_stem % 5) * 2) % 10
    return (first_stem + hour_branch) % 10, hour_branch


def describe_pillar(stem, branch):
    stem_name, stem_hanzi = HEAVENLY_STEMS[stem]
    branch_name, branch_hanzi = EARTHLY_BRANCHES[branch]
    element_name, element_hanzi = ELEMENT_LABELS[STEM_ELEMENTS[stem]]
    branch_element_name, branch_element_hanzi = ELEMENT_LABELS[BRANCH_ELEMENTS[branch]]
    return {
        "stem_index": stem,
        "branch_index": branch,
        "stem": stem_name,
        "stem_hanzi": stem_hanzi,
        "branch": branch_name,
        "branch_hanzi": branch_hanzi,
        "pillar": f"{stem_name} {branch_name}",
        "pillar_hanzi": f"{stem_hanzi}{branch_hanzi}",
        "stem_element": element_name,
        "stem_element_hanzi": element_hanzi,
        "stem_polarity": STEM_POLARITY[stem],
        "branch_element": branch_element_name,
        "branch_element_hanzi": branch_element_hanzi,
        "hidden_stems": [
            {
                "index": s,
                "name": HEAVENLY_STEMS[s][0],
                "hanzi": HEAVENLY_STEMS[s][1],
                "element": ELEMENT_LABELS[STEM_ELEMENTS[s]][0],
            }
            for s in HIDDEN_STEMS[branch]
        ],
    }


def get_element_role(day_element, other_element):
    if day_element == other_element:
        return "sama"
    if ELEMENT_GENERATES[day_element] == other_element:
        return "dm_menghidupi"
    if ELEMENT_GENERATES[other_element] == day_element:
        return "menghidupi_dm"
    if ELEMENT_CONTROLS[day_element] == other_element:
        return "dm_mengekang"
    return "mengekang_dm"


def get_ten_god(day_stem, other_stem):
    role = get_element_role(STEM_ELEMENTS[day_stem], STEM_ELEMENTS[other_stem])
    same_polarity = STEM_POLARITY[day_stem] == STEM_POLARITY[other_stem]
    return TEN_GODS_TABLE[(role, same_polarity)]


def describe_ten_god(day_stem, other_stem):
    key = get_ten_god(day_stem, other_stem)
    name, hanzi, meaning = TEN_GOD_LABELS[key]
    return {"key": key, "name": name, "hanzi": hanzi, "meaning": meaning}


ELEMENT_DOMINANT_SHARE = 0.30

ELEMENT_WEAK_SHARE = 0.10


def classify_element_status(score, total):
    if score <= 0:
        return "kosong"
    share = score / total if total else 0.0
    if share >= ELEMENT_DOMINANT_SHARE:
        return "dominan"
    if share <= ELEMENT_WEAK_SHARE:
        return "lemah"
    return "seimbang"


PILLAR_SLOTS = ("year", "month", "day", "hour")

ADJACENT_SLOT_PAIRS = (("year", "month"), ("month", "day"), ("day", "hour"))

ALL_SLOT_PAIRS = (
    ("year", "month"),
    ("year", "day"),
    ("year", "hour"),
    ("month", "day"),
    ("month", "hour"),
    ("day", "hour"),
)

ADJACENT_CLASH_FACTOR = 0.5


def get_hidden_stem_weights(branch):
    stems = HIDDEN_STEMS[branch]
    raw = [
        HIDDEN_STEM_WEIGHTS[min(position, len(HIDDEN_STEM_WEIGHTS) - 1)]
        for position in range(len(stems))
    ]
    total = sum(raw)
    return [(stem, weight / total) for stem, weight in zip(stems, raw)]


def get_branch_distance(first, second):
    distance = abs(first - second)
    return 12 - distance if distance > 6 else distance


def list_branch_relations(first, second):
    if first == second:
        return ["zi_xing"] if first in ZI_XING_BRANCHES else []
    pair = frozenset((first, second))
    found = []
    if get_branch_distance(first, second) == 6:
        found.append("chong")
    if pair in LIU_HE_PAIRS:
        found.append("liu_he")
    if SAN_HE_GROUP[first] == SAN_HE_GROUP[second]:
        found.append("san_he")
    if pair in XIANG_XING_PAIRS:
        found.append("xiang_xing")
    if pair in LIU_HAI_PAIRS:
        found.append("liu_hai")
    if pair in LIU_PO_PAIRS:
        found.append("liu_po")
    return found


def detect_chart_relations(chart):
    present = [slot for slot in PILLAR_SLOTS if chart[slot] is not None]

    pairs = []
    for first, second in ALL_SLOT_PAIRS:
        if first not in present or second not in present:
            continue
        branches = [chart[first]["branch_index"], chart[second]["branch_index"]]
        relations = list_branch_relations(*branches)
        if relations:
            pairs.append(
                {
                    "slots": [first, second],
                    "branches": branches,
                    "adjacent": (first, second) in ADJACENT_SLOT_PAIRS,
                    "relations": relations,
                }
            )

    members = {}
    for slot in present:
        branch = chart[slot]["branch_index"]
        members.setdefault(SAN_HE_GROUP[branch], {}).setdefault(branch, slot)

    triads = [
        {
            "group": group,
            "branches": sorted(found),
            "slots": [found[branch] for branch in sorted(found)],
        }
        for group, found in members.items()
        if len(found) == 3
    ]

    return {"pairs": pairs, "triads": triads}


def get_branch_weight_factors(chart):
    factors = {slot: 1.0 for slot in PILLAR_SLOTS}
    for first, second in ADJACENT_SLOT_PAIRS:
        if chart[first] is None or chart[second] is None:
            continue
        distance = get_branch_distance(
            chart[first]["branch_index"], chart[second]["branch_index"]
        )
        if distance == 6:
            factors[first] = ADJACENT_CLASH_FACTOR
            factors[second] = ADJACENT_CLASH_FACTOR
    return factors


def tally_elements(chart):
    tally = {element: 0.0 for element in ELEMENT_LABELS}
    factors = get_branch_weight_factors(chart)

    for slot in PILLAR_SLOTS:
        pillar = chart[slot]
        if pillar is None:
            continue
        bonus = MONTH_COMMAND_BONUS if slot == "month" else 1.0
        tally[STEM_ELEMENTS[pillar["stem_index"]]] += 1.0 * bonus
        for stem, weight in get_hidden_stem_weights(pillar["branch_index"]):
            tally[STEM_ELEMENTS[stem]] += weight * bonus * factors[slot]

    return {element: round(value, 2) for element, value in tally.items()}


def judge_day_master_strength(chart, tally):
    day_element = STEM_ELEMENTS[chart["day"]["stem_index"]]
    resource = next(e for e in ELEMENT_GENERATES if ELEMENT_GENERATES[e] == day_element)

    support = tally[day_element] + tally[resource]
    total = sum(tally.values())
    ratio = support / total if total else 0.0

    key = "cong_qiang"
    for limit, candidate in STRENGTH_THRESHOLDS:
        if ratio < limit:
            key = candidate
            break

    return {
        "key": key,
        "support_ratio": round(ratio, 3),
        "support_score": round(support, 2),
        "total_score": round(total, 2),
        "day_element": ELEMENT_LABELS[day_element][0],
        "resource_element": ELEMENT_LABELS[resource][0],
    }


def get_useful_gods(chart, strength_key):
    day_element = STEM_ELEMENTS[chart["day"]["stem_index"]]
    resource = next(e for e in ELEMENT_GENERATES if ELEMENT_GENERATES[e] == day_element)
    output = ELEMENT_GENERATES[day_element]
    wealth = ELEMENT_CONTROLS[day_element]
    officer = next(e for e in ELEMENT_CONTROLS if ELEMENT_CONTROLS[e] == day_element)

    strengthening = [day_element, resource]
    draining = [output, wealth, officer]

    if strength_key in ("shen_qiang", "cong_ruo"):
        favourable, unfavourable = draining, strengthening
    elif strength_key in ("shen_ruo", "cong_qiang"):
        favourable, unfavourable = strengthening, draining
    else:
        favourable, unfavourable = [output, wealth], [officer]

    return {
        "favourable": [ELEMENT_LABELS[e][0] for e in favourable],
        "favourable_keys": favourable,
        "unfavourable": [ELEMENT_LABELS[e][0] for e in unfavourable],
        "unfavourable_keys": unfavourable,
    }


def map_ten_gods(chart):
    day_stem = chart["day"]["stem_index"]
    mapped = {}

    for slot in ("year", "month", "day", "hour"):
        pillar = chart[slot]
        if pillar is None:
            mapped[slot] = None
            continue
        mapped[slot] = {
            "stem": describe_ten_god(day_stem, pillar["stem_index"]),
            "hidden": [
                describe_ten_god(day_stem, stem)
                for stem in HIDDEN_STEMS[pillar["branch_index"]]
            ],
        }

    mapped["day"]["stem"] = {
        "key": "ri_yuan",
        "name": "Ri Yuan",
        "hanzi": "日元",
        "meaning": "Diri Sendiri",
    }
    return mapped


def tally_ten_gods(chart):
    day_stem = chart["day"]["stem_index"]
    tally = {key: 0.0 for key in TEN_GOD_LABELS}
    factors = get_branch_weight_factors(chart)

    for slot in PILLAR_SLOTS:
        pillar = chart[slot]
        if pillar is None:
            continue
        bonus = MONTH_COMMAND_BONUS if slot == "month" else 1.0
        if slot != "day":
            tally[get_ten_god(day_stem, pillar["stem_index"])] += 1.0 * bonus
        for stem, weight in get_hidden_stem_weights(pillar["branch_index"]):
            tally[get_ten_god(day_stem, stem)] += weight * bonus * factors[slot]

    return {key: round(value, 2) for key, value in tally.items()}


def get_dominant_ten_god(chart, tally):
    ranked = sorted(tally.items(), key=lambda item: (-item[1], TEN_GOD_ORDER[item[0]]))
    key, score = ranked[0]
    runner_up = ranked[1][1]
    total = sum(tally.values())

    return {
        "key": key,
        "name": TEN_GOD_LABELS[key][0],
        "hanzi": TEN_GOD_LABELS[key][1],
        "meaning": TEN_GOD_LABELS[key][2],
        "score": score,
        "share": round(score / total, 3) if total else 0.0,
        "decisive": score - runner_up >= DOMINANT_GOD_MARGIN,
    }


def get_year_branch_relation(chart):
    day_element = STEM_ELEMENTS[chart["day"]["stem_index"]]
    year_element = BRANCH_ELEMENTS[chart["year"]["branch_index"]]
    return {
        "key": YEAR_BRANCH_RELATION_KEYS[get_element_role(day_element, year_element)],
        "day_element": ELEMENT_LABELS[day_element][0],
        "year_element": ELEMENT_LABELS[year_element][0],
    }


def analyse_chart(chart):
    chart["relations"] = detect_chart_relations(chart)
    chart["branch_factors"] = get_branch_weight_factors(chart)
    tally = tally_elements(chart)
    strength = judge_day_master_strength(chart, tally)
    chart["element_tally"] = tally
    chart["strength"] = strength
    chart["useful_gods"] = get_useful_gods(chart, strength["key"])
    chart["ten_gods"] = map_ten_gods(chart)
    chart["ten_god_tally"] = tally_ten_gods(chart)
    chart["dominant_ten_god"] = get_dominant_ten_god(chart, chart["ten_god_tally"])
    chart["year_branch_relation"] = get_year_branch_relation(chart)
    chart["shen_sha"] = detect_shen_sha(chart)
    return chart


def describe_city(city, assumed):
    city_name, city_longitude, city_zone, city_province = BIRTH_CITIES[city]
    return {
        "key": city,
        "name": city_name,
        "province": city_province,
        "longitude": city_longitude,
        "zone": city_zone,
        "zone_meridian": TIME_ZONE_MERIDIANS[city_zone],
        "assumed": assumed,
    }


def build_four_pillars(birth_date, birth_hour=None, birth_minute=0,
                       city_key=None, gender=None):
    effective_date = birth_date
    solar_offset = None
    resolved_city = None
    hour_branch = None
    late_zi_calendar_date = None
    matched = resolve_city(city_key)

    if birth_hour is not None:
        resolved_city = describe_city(matched or DEFAULT_CITY, matched is None)

        clock = datetime.datetime(
            birth_date.year, birth_date.month, birth_date.day,
            birth_hour, birth_minute,
        )
        solar_offset = get_true_solar_offset(
            clock, resolved_city["longitude"], resolved_city["zone_meridian"]
        )
        solar_moment = clock + datetime.timedelta(minutes=solar_offset)

        hour_branch = get_hour_branch(solar_moment.hour)
        effective_date = solar_moment.date()

        if solar_moment.hour >= 23:
            late_zi_calendar_date = effective_date
            effective_date += datetime.timedelta(days=1)
    elif matched:
        resolved_city = describe_city(matched, False)

    zone = resolved_city["zone"] if resolved_city else DEFAULT_ZONE
    term_moment = clock if birth_hour is not None else birth_date
    year_stem, year_branch = get_year_pillar(term_moment, zone)
    month_stem, month_branch = get_month_pillar(term_moment, year_stem, zone)
    day_stem, day_branch = get_day_pillar(effective_date)

    chart = {
        "year": describe_pillar(year_stem, year_branch),
        "month": describe_pillar(month_stem, month_branch),
        "day": describe_pillar(day_stem, day_branch),
        "hour": None,
        "day_master": {
            "index": day_stem,
            "name": HEAVENLY_STEMS[day_stem][0],
            "hanzi": HEAVENLY_STEMS[day_stem][1],
            "element": ELEMENT_LABELS[STEM_ELEMENTS[day_stem]][0],
            "element_hanzi": ELEMENT_LABELS[STEM_ELEMENTS[day_stem]][1],
            "polarity": STEM_POLARITY[day_stem],
        },
        "pillar_count": 3,
        "has_hour": False,
        "city": resolved_city,
        "true_solar_offset_minutes": (
            round(solar_offset, 1) if solar_offset is not None else None
        ),
        "late_zi_alternative_day": (
            describe_pillar(*get_day_pillar(late_zi_calendar_date))
            if late_zi_calendar_date is not None
            else None
        ),
    }

    if hour_branch is not None:
        hour_stem, hour_branch = get_hour_pillar(day_stem, hour_branch)
        chart["hour"] = describe_pillar(hour_stem, hour_branch)
        chart["pillar_count"] = 4
        chart["has_hour"] = True

    if gender is not None:
        chart["luck"] = build_luck_pillars(
            effective_date,
            day_stem,
            year_stem,
            month_stem,
            month_branch,
            gender,
            zone,
        )
    else:
        chart["luck"] = None

    return analyse_chart(chart)


def find_month_boundary(target_date, forward=True, zone=DEFAULT_ZONE):
    branch = get_month_branch(target_date, zone)
    step = datetime.timedelta(days=1 if forward else -1)
    probe = target_date

    for _ in range(40):
        probe += step
        if get_month_branch(probe, zone) != branch:
            return probe if forward else probe + datetime.timedelta(days=1)

    return None


MALE_TOKENS = frozenset(
    ["pria", "laki", "laki-laki", "lakilaki", "male", "m", "cowok"]
)

FEMALE_TOKENS = frozenset(
    ["wanita", "perempuan", "female", "f", "cewek"]
)


def normalise_gender(gender):
    token = str(gender).strip().lower()
    if token in MALE_TOKENS:
        return "pria"
    if token in FEMALE_TOKENS:
        return "wanita"
    return None


def get_luck_direction(year_stem, gender):
    normalised = normalise_gender(gender)
    if normalised is None:
        return None
    stem_is_yang = STEM_POLARITY[year_stem] == "yang"
    return "maju" if stem_is_yang == (normalised == "pria") else "mundur"


def get_luck_start_age(birth_date, direction, zone=DEFAULT_ZONE):
    forward = direction == "maju"
    boundary = find_month_boundary(birth_date, forward, zone)

    if boundary is None:
        return {"years": 0, "months": 0, "days_to_term": 0}

    days = abs((boundary - birth_date).days)
    return {
        "years": days // 3,
        "months": (days % 3) * 4,
        "days_to_term": days,
    }


def describe_pillar_gods(day_stem, stem, branch):
    stem_god = get_ten_god(day_stem, stem)
    tally = {stem_god: 1.0}
    for position, hidden in enumerate(HIDDEN_STEMS[branch]):
        weight = HIDDEN_STEM_WEIGHTS[min(position, len(HIDDEN_STEM_WEIGHTS) - 1)]
        key = get_ten_god(day_stem, hidden)
        tally[key] = tally.get(key, 0.0) + weight
    dominant = min(
        tally,
        key=lambda key: (-tally[key], key != stem_god, TEN_GOD_ORDER[key]),
    )
    return {
        "stem_god": describe_ten_god(day_stem, stem),
        "hidden_gods": [describe_ten_god(day_stem, hidden)
                        for hidden in HIDDEN_STEMS[branch]],
        "dominant_god": {
            "key": dominant,
            "name": TEN_GOD_LABELS[dominant][0],
            "hanzi": TEN_GOD_LABELS[dominant][1],
            "meaning": TEN_GOD_LABELS[dominant][2],
        },
    }


def build_luck_pillars(birth_date, day_stem, year_stem, month_stem,
                       month_branch, gender, zone=DEFAULT_ZONE, count=9):
    direction = get_luck_direction(year_stem, gender)
    if direction is None:
        return None
    start = get_luck_start_age(birth_date, direction, zone)
    step = 1 if direction == "maju" else -1

    pillars = []
    for i in range(1, count + 1):
        stem = (month_stem + step * i) % 10
        branch = (month_branch + step * i) % 12
        age_from = start["years"] + (i - 1) * 10
        pillars.append(
            {
                "order": i,
                "age_from": age_from,
                "age_to": age_from + 9,
                "year_from": birth_date.year + age_from,
                "year_to": birth_date.year + age_from + 9,
                **describe_pillar(stem, branch),
                **describe_pillar_gods(day_stem, stem, branch),
            }
        )

    return {
        "direction": direction,
        "start_age_years": start["years"],
        "start_age_months": start["months"],
        "days_to_term": start["days_to_term"],
        "pillars": pillars,
    }


def collect_branches(chart):
    return {
        slot: chart[slot]["branch_index"]
        for slot in ("year", "month", "day", "hour")
        if chart[slot] is not None
    }


def collect_stems(chart):
    return {
        slot: chart[slot]["stem_index"]
        for slot in ("year", "month", "day", "hour")
        if chart[slot] is not None
    }


def _slots_with_branch(branches, target):
    return [slot for slot, value in branches.items() if value == target]


def detect_shen_sha(chart):
    branches = collect_branches(chart)
    stems = collect_stems(chart)
    day_stem = chart["day"]["stem_index"]
    year_branch = chart["year"]["branch_index"]
    month_branch = chart["month"]["branch_index"]
    group = SAN_HE_GROUP[year_branch]

    found = {}

    def add(key, slots):
        if slots:
            found[key] = sorted(set(slots))

    add("tian_yi", [s for t in TIAN_YI_BY_STEM[day_stem]
                    for s in _slots_with_branch(branches, t)])
    add("wen_chang", _slots_with_branch(branches, WEN_CHANG_BY_STEM[day_stem]))
    add("lu_shen", _slots_with_branch(branches, LU_SHEN_BY_STEM[day_stem]))
    add("yang_ren", _slots_with_branch(branches, YANG_REN_BY_STEM[day_stem]))
    add("jin_yu", _slots_with_branch(branches, JIN_YU_BY_STEM[day_stem]))
    add("tao_hua", _slots_with_branch(branches, TAO_HUA_BY_GROUP[group]))
    add("yi_ma", _slots_with_branch(branches, YI_MA_BY_GROUP[group]))
    add("hua_gai", _slots_with_branch(branches, HUA_GAI_BY_GROUP[group]))

    month_group = SAN_HE_GROUP[month_branch]
    add("yue_de", [slot for slot, stem in stems.items()
                   if stem == YUE_DE_BY_GROUP[month_group]])

    kind, target = TIAN_DE_BY_MONTH[month_branch]
    if kind == "stem":
        add("tian_de", [slot for slot, stem in stems.items() if stem == target])
    else:
        add("tian_de", _slots_with_branch(branches, target))

    gu_chen, gua_su = GU_GUA_BY_YEAR[year_branch]
    add("gu_chen", _slots_with_branch(branches, gu_chen))
    add("gua_su", _slots_with_branch(branches, gua_su))

    return [
        {
            "key": key,
            "name_cn": SHEN_SHA_BANK[key]["name_cn"],
            "icon": SHEN_SHA_BANK[key]["icon"],
            "category": SHEN_SHA_BANK[key]["category"],
            "slots": slots,
        }
        for key, slots in found.items()
    ]


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

def score_daily_fortune(fortune):
    return (
        DAILY_RANK_STATUS_WEIGHT[fortune["branch_relation_key"]]
        + DAILY_RANK_ELEMENT_WEIGHT[fortune["element_relation_key"]]
    )


def resolve_rank_tier(rank):
    if rank <= 3:
        return DAILY_RANK_TIERS[0]
    if rank <= 9:
        return DAILY_RANK_TIERS[1]
    return DAILY_RANK_TIERS[2]


def build_daily_leaderboard(fortunes):
    ranked = sorted(
        fortunes,
        key=lambda item: (-score_daily_fortune(item),
                          SHIOS_LIST.index(item["shio_key"])),
    )

    board = []
    for position, item in enumerate(ranked, 1):
        tier = resolve_rank_tier(position)
        item["rank"] = position
        item["rank_tier"] = tier["key"]
        board.append({
            "rank": position,
            "shio_key": item["shio_key"],
            "name": item["name"],
            "hanzi": item["hanzi"],
            "score": score_daily_fortune(item),
            "status": item["status"],
            "status_code": item["status_code"],
            "element_relation": item["element_relation"],
            "element_hanzi": item["element_hanzi"],
            "tier": tier["key"],
            "tier_label": tier["label"],
            "tier_code": tier["code"],
            "tier_note": tier["note"],
        })
    return board


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

        branch_relation_key = get_branch_relation(today_idx, idx)
        status, pool = DAILY_RELATION_VIEW[branch_relation_key]
        status_code = BRANCH_RELATION_META[branch_relation_key]["code"]
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
                "branch_relation_key": branch_relation_key,
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

    leaderboard = build_daily_leaderboard(results)

    formatted_date = target_date.strftime("%d %B %Y")
    stem_name, stem_hanzi = HEAVENLY_STEMS[stem_idx]
    branch_name, branch_hanzi = EARTHLY_BRANCHES[shio_index]
    month_branch_name, month_branch_hanzi = EARTHLY_BRANCHES[month_branch]
    day_element_name, day_element_hanzi = ELEMENT_LABELS[day_element]

    return {
        "leaderboard": leaderboard,
        "leaderboard_note": DAILY_RANK_NOTE,
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
    "Jam ini selaras dengan jam tradisional (時辰) shio-mu. Ini konvensi penanggalan Tionghoa, "
    "bukan ketentuan dalam praktik Buddha pelindung kelahiran (本命佛)."
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


def describe_element_side(self_key, other_key, self_label=None, other_label=None):
    self_element = BRANCH_ELEMENTS[SHIOS_LIST.index(self_key)]
    other_element = BRANCH_ELEMENTS[SHIOS_LIST.index(other_key)]
    role = get_element_role_pair(self_element, other_element)
    entry = PAIR_ELEMENT_DYNAMIC_BANK[role]
    fields = {
        "self": self_label or SHIO_DATA[self_key]["name"],
        "other": other_label or SHIO_DATA[other_key]["name"],
        "self_element": ELEMENT_LABELS[self_element][0],
        "other_element": ELEMENT_LABELS[other_element][0],
    }
    return {
        "shio": SHIO_DATA[self_key]["name"],
        "person": self_label,
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


def get_pair_element_dynamic(key_a, key_b, label_a=None, label_b=None):
    if key_a not in SHIO_DATA or key_b not in SHIO_DATA:
        return None
    return {
        "for_shio1": describe_element_side(key_a, key_b, label_a, label_b),
        "for_shio2": describe_element_side(key_b, key_a, label_b, label_a),
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


def get_year_layer(date1, date2):
    if date1 is None or date2 is None:
        return None

    pillar1 = describe_year_pillar(date1)
    pillar2 = describe_year_pillar(date2)

    stem_pair = tuple(sorted((pillar1["stem_index"], pillar2["stem_index"])))
    stem_relation = dict(STEM_RELATION_BANK.get(stem_pair, STEM_NEUTRAL))

    return {
        "shio1": {**pillar1, "nayin_relation": describe_nayin_side(pillar1, pillar2)},
        "shio2": {**pillar2, "nayin_relation": describe_nayin_side(pillar2, pillar1)},
        "stem_relation": stem_relation,
        "lichun_note": (
            "Tahun Imlek berganti di awal musim semi (立春, sekitar 4 Februari), bukan 1 Januari. "
            "Kelahiran Januari sampai awal Februari masuk pilar tahun sebelumnya."
        ),
    }


SOLITUDE_STARS = ("gu_chen", "gua_su")

BAZI_LAYER_NOTE = (
    "Lapisan ini dihitung dari pilar hari (日柱) kedua tanggal, bukan dari "
    "shionya. Di pencocokan jodoh (合婚) klasik justru pilar hari inilah yang dibaca lebih dulu, "
    "karena cabang hari adalah istana pasangan (夫妻宮). Halaman ini cuma "
    "meminta tanggal, jadi hitungannya memakai tiga pilar — sah dibaca, tapi "
    "lapisan jam tidak ikut."
)


DEFAULT_LENS = "asmara"


def resolve_lens(lens):
    return RELATION_LENS[lens if lens in RELATION_LENS else DEFAULT_LENS]


def describe_relation_label(relation_key, lens=DEFAULT_LENS):
    if not resolve_lens(lens)["romantic"] and relation_key in NEUTRAL_RELATION_LABELS:
        return NEUTRAL_RELATION_LABELS[relation_key]
    return BRANCH_RELATION_META[relation_key]["label"]


def pair_side_labels(name1, name2):
    if name1 != name2:
        return name1, name2
    return name1 + " (pertama)", name2 + " (kedua)"


def describe_day_pillar_match(chart1, chart2, lens=DEFAULT_LENS):
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
        "text": (
            DAY_PILLAR_RELATION_BANK
            if resolve_lens(lens)["romantic"]
            else NEUTRAL_DAY_PILLAR_RELATION_BANK
        )[relation_key],
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


def describe_useful_god_match(chart1, chart2, label1, label2, lens=DEFAULT_LENS):
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
    elif burdens_to1 or burdens_to2:
        key = "beban_sepihak"
    else:
        key = "netral"

    giver, receiver = (label1, label2) if supplies_to2 else (label2, label1)
    burdener, burdened = (label1, label2) if burdens_to2 else (label2, label1)
    entry = USEFUL_GOD_MATCH_BANK[key]
    note = entry["note"]
    if not resolve_lens(lens)["romantic"]:
        note = NEUTRAL_USEFUL_GOD_NOTES.get(key, note)

    return {
        "key": key,
        "title": entry["title"],
        "code": entry["code"],
        "note": note.format(
            a=label1, b=label2, giver=giver, receiver=receiver,
            burdener=burdener, burdened=burdened,
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


def describe_couple_stars(chart1, chart2, label1, label2, lens=DEFAULT_LENS):
    keys1 = collect_shen_sha_keys(chart1)
    keys2 = collect_shen_sha_keys(chart2)
    romantic = resolve_lens(lens)["romantic"]
    stars = []

    def push(bank_key, who):
        entry = COUPLE_STAR_BANK[bank_key]
        if not romantic and bank_key in NEUTRAL_COUPLE_STARS:
            entry = {**entry, **NEUTRAL_COUPLE_STARS[bank_key]}
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


def get_bazi_layer(date1, date2, name1, name2, lens=DEFAULT_LENS):
    if date1 is None or date2 is None:
        return None

    chart1 = build_four_pillars(date1)
    chart2 = build_four_pillars(date2)
    label1, label2 = pair_side_labels(name1, name2)
    lens_meta = resolve_lens(lens)

    return {
        "note": BAZI_LAYER_NOTE if lens_meta["romantic"] else NEUTRAL_BAZI_LAYER_NOTE,
        "title": lens_meta["day_layer_title"],
        "supply_label": lens_meta["supply_label"],
        "burden_label": lens_meta["burden_label"],
        "day_pillar": describe_day_pillar_match(chart1, chart2, lens),
        "useful_god": describe_useful_god_match(chart1, chart2, label1, label2, lens),
        "couple_stars": describe_couple_stars(chart1, chart2, label1, label2, lens),
    }


COMPAT_NARRATIVE_FIELDS = ("asmara", "persahabatan", "bisnis", "drama", "tips")


def pick_compat_texts(pair_key, compat, day):
    picked = {}
    for field in COMPAT_NARRATIVE_FIELDS:
        texts = compat.get(field) or [""]
        if isinstance(texts, str):
            texts = [texts]
        seed = build_stable_seed(pair_key[0], pair_key[1], field, day.isoformat())
        picked[field] = texts[seed % len(texts)]
    return picked


def describe_lens_narrative(compat, lens=DEFAULT_LENS):
    lens_meta = resolve_lens(lens)
    return {
        "key": lens if lens in RELATION_LENS else DEFAULT_LENS,
        "label": lens_meta["label"],
        "title": lens_meta["narrative_title"],
        "icon": lens_meta["narrative_icon"],
        "text": compat.get(lens_meta["narrative_field"], ""),
    }


def get_shio_compatibility(shio1_key=None, shio2_key=None,
                           birth1=None, birth2=None, lens=DEFAULT_LENS,
                           names=None, day=None):
    date1 = parse_birth_date(birth1) if birth1 else None
    date2 = parse_birth_date(birth2) if birth2 else None
    if birth1 and date1 is None:
        return {"error": "Tanggal lahir pertama tidak valid."}
    if birth2 and date2 is None:
        return {"error": "Tanggal lahir kedua tidak valid."}

    if date1 is not None and date2 is not None:
        shio1_key = SHIOS_LIST[get_year_pillar(date1)[1]]
        shio2_key = SHIOS_LIST[get_year_pillar(date2)[1]]
    if not shio1_key or not shio2_key:
        return {"error": "Isi kedua tanggal lahir dulu."}

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
    person1, person2 = names if names else (None, None)
    label1 = person1 or s1_data["name"]
    label2 = person2 or s2_data["name"]
    texts = pick_compat_texts(pair_key, compat, day or resolve_almanac_date())

    return {
        "shio1": {"name": s1_data["name"], "hanzi": s1_data["hanzi"]},
        "shio2": {"name": s2_data["name"], "hanzi": s2_data["hanzi"]},
        "relationship": describe_relation_label(relation_key, lens),
        "relation_key": relation_key,
        "relation_code": meta["code"],
        "score": compat.get("score", 50),
        **texts,
        "narrative": describe_lens_narrative(texts, lens),
        "pair_relation": dict(PAIR_RELATION_BANK[relation_key]),
        "element_dynamic": get_pair_element_dynamic(
            shio1_key, shio2_key, person1, person2
        ),
        "year_layer": get_year_layer(date1, date2),
        "bazi_layer": get_bazi_layer(date1, date2, label1, label2, lens),
    }

GROUP_BRANCH_NOTE = (
    "Peta ini memakai cabang tahun (shio) saja, bukan pilar hari. Artinya ini "
    "gambaran watak bawaan antaranggota, bukan pencocokan penuh seperti di "
    "Ramalan Pasangan yang ikut membaca pilar hari masing-masing."
)

GROUP_VERDICT_MARGIN = 0.15

GROUP_HIGHLIGHT_LIMIT = 3


def lookup_pair_score(key_a, key_b):
    pair = SHIO_COMPATIBILITY_BANK.get(tuple(sorted((key_a, key_b))))
    return pair.get("score", 50) if pair else 50


def resolve_group_role(tally):
    good, bad, neutral = tally["good"], tally["bad"], tally["neutral"]
    if good and good == bad and good + bad >= neutral:
        return "jembatan"
    if good > bad and good >= neutral:
        return "perekat"
    if bad > good and bad >= neutral:
        return "pemicu"
    return "penyeimbang"


def resolve_group_verdict(counts):
    balance = (counts["good"] - counts["bad"]) / counts["total"]
    if balance >= GROUP_VERDICT_MARGIN:
        return "harmonis"
    if balance <= -GROUP_VERDICT_MARGIN:
        return "bentrok"
    return "campur"


def find_group_triads(members):
    groups = {}
    for member in members:
        branch = SHIOS_LIST.index(member["shio_key"])
        groups.setdefault(SAN_HE_GROUP[branch], {}).setdefault(branch, []).append(member)
    triads = []
    for group_key, branches in groups.items():
        if len(branches) < 3:
            continue
        element = SAN_HE_ELEMENT[group_key]
        triads.append({
            "element": ELEMENT_LABELS[element][0],
            "element_hanzi": ELEMENT_LABELS[element][1],
            "names": [m["name"] for branch in sorted(branches) for m in branches[branch]],
        })
    return triads


def describe_group_dynamic(members, seed=""):
    tallies = {m["slot"]: {"good": 0, "bad": 0, "neutral": 0} for m in members}
    counts = {"good": 0, "bad": 0, "neutral": 0, "total": 0}
    pairs = []
    for first, second in combinations(members, 2):
        relation_key = get_branch_relation(
            SHIOS_LIST.index(first["shio_key"]), SHIOS_LIST.index(second["shio_key"])
        )
        relation = PAIR_RELATION_BANK[relation_key]
        code = relation["code"]
        tallies[first["slot"]][code] += 1
        tallies[second["slot"]][code] += 1
        counts[code] += 1
        counts["total"] += 1
        pairs.append({
            "slots": [first["slot"], second["slot"]],
            "names": [first["name"], second["name"]],
            "relation_key": relation_key,
            "label": describe_relation_label(relation_key, "pertemanan"),
            "hanzi": relation["hanzi"],
            "title": relation["title"],
            "note": relation["note"],
            "code": code,
            "score": lookup_pair_score(first["shio_key"], second["shio_key"]),
        })

    role_seen = {}
    people = []
    for member in members:
        tally = tallies[member["slot"]]
        role_key = resolve_group_role(tally)
        variants = GROUP_ROLE_BANK[role_key]
        offset = role_seen.get(role_key, build_stable_seed(seed, role_key) % len(variants))
        role_seen[role_key] = offset + 1
        variant = variants[offset % len(variants)]
        shio = SHIO_DATA[member["shio_key"]]
        people.append({
            "slot": member["slot"],
            "name": member["name"],
            "shio": shio["name"],
            "hanzi": shio["hanzi"],
            "role_key": role_key,
            "role_title": variant["title"],
            "role_note": variant["note"],
            **tally,
        })

    verdict_key = resolve_group_verdict(counts)
    verdicts = GROUP_VERDICT_BANK[verdict_key]
    verdict = verdicts[build_stable_seed(seed, verdict_key) % len(verdicts)]

    best = sorted(
        (pair for pair in pairs if pair["code"] == "good"),
        key=lambda pair: -pair["score"],
    )[:GROUP_HIGHLIGHT_LIMIT]
    tense = sorted(
        (pair for pair in pairs if pair["code"] == "bad"),
        key=lambda pair: (pair["relation_key"] != "chong", pair["score"]),
    )[:GROUP_HIGHLIGHT_LIMIT]

    return {
        "verdict": {"key": verdict_key, **verdict},
        "counts": counts,
        "members": people,
        "best_pairs": best,
        "tense_pairs": tense,
        "pairs": pairs,
        "triads": find_group_triads(members),
        "note": GROUP_BRANCH_NOTE,
    }


GUESS_HINT_COUNT = 7

GUESS_WORD_PATTERN = re.compile(r"[a-z]{4,}")

GUESS_NAME_PATTERN = re.compile(
    r"\b(" + "|".join(data["name"].lower() for data in SHIO_DATA.values()) + r"|shio)\b"
)

GUESS_HANZI = set("".join(data["hanzi"] for data in SHIO_DATA.values()))

GUESS_COMMONNESS = {}


def is_guess_safe(text):
    lowered = text.lower()
    if GUESS_NAME_PATTERN.search(lowered):
        return False
    return not GUESS_HANZI.intersection(text)


GUESS_DISTINCT_LIMIT = 0.6

GUESS_COMMONNESS_SAMPLE = 5


def collect_raw_guess_pool(shio_key, flavor):
    if flavor == "pedas":
        pool = SHIO_ROASTING_BANK[shio_key]["toxic_traits"]
    else:
        identity = IDENTITY_BANK[shio_key]
        pool = (
            identity["traits_positive"]
            + identity["green_flags"]
            + GUESS_EXTRA_TRAITS[shio_key]
            + GUESS_SIGNATURE_TRAITS[shio_key]
        )
    return [text for text in pool if is_guess_safe(text)]


def collect_guess_pool(shio_key, flavor):
    peak = get_guess_peak_similarity(flavor)
    return [
        text for text in collect_raw_guess_pool(shio_key, flavor)
        if peak[(shio_key, text)] < GUESS_DISTINCT_LIMIT
    ]


def guess_tokens(text):
    return set(GUESS_WORD_PATTERN.findall(text.lower())) - GUESS_STOPWORDS


def measure_guess_similarity(flavor):
    if flavor in GUESS_COMMONNESS:
        return GUESS_COMMONNESS[flavor]
    pools = {key: [(text, guess_tokens(text)) for text in collect_raw_guess_pool(key, flavor)]
             for key in SHIOS_LIST}
    commonness = {}
    peak = {}
    for key, items in pools.items():
        others = [tokens for other, entries in pools.items() if other != key
                  for _, tokens in entries]
        for text, tokens in items:
            similarities = sorted(
                len(tokens & other_tokens) / len(tokens | other_tokens)
                for other_tokens in others
                if tokens | other_tokens
            )
            top = similarities[-GUESS_COMMONNESS_SAMPLE:] or [0.0]
            commonness[(key, text)] = sum(top) / len(top)
            peak[(key, text)] = top[-1]
    GUESS_COMMONNESS[flavor] = (commonness, peak)
    return GUESS_COMMONNESS[flavor]


def get_guess_commonness(flavor):
    return measure_guess_similarity(flavor)[0]


def get_guess_peak_similarity(flavor):
    return measure_guess_similarity(flavor)[1]


def build_guess_hints(shio_key, flavor, rng, count=GUESS_HINT_COUNT):
    pool = collect_guess_pool(shio_key, flavor)
    commonness = get_guess_commonness(flavor)
    signatures = []
    if flavor != "pedas":
        signatures = [text for text in GUESS_SIGNATURE_TRAITS[shio_key] if text in pool]
    rest = [text for text in pool if text not in signatures]
    chosen = rng.sample(rest, min(count - len(signatures), len(rest)))
    return sorted(chosen, key=lambda text: -commonness[(shio_key, text)]) + signatures


YEARLY_LICHUN_NOTE = (
    "Tahun Imlek berganti di awal musim semi (立春), sekitar 4 Februari — bukan 1 Januari. "
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


def resolve_luck_direction(stem_index, gender_key):
    yang = STEM_POLARITY[stem_index] == "yang"
    maju = (yang and gender_key == "pria") or (not yang and gender_key == "wanita")
    return "maju" if maju else "mundur"


def describe_chart_roast(birth_date_str, gender):
    birth_date = parse_birth_date(birth_date_str)
    if birth_date is None:
        return None

    year_stem, year_branch = get_year_pillar(birth_date)
    day_stem, day_branch = get_day_pillar(birth_date)
    actual_shio = SHIOS_LIST[year_branch]
    year_element = STEM_ELEMENTS[year_stem]

    stem_id = DAY_MASTER_BANK_KEYS[day_stem]
    pool = ROAST_DAY_MASTER_BANK[stem_id]
    seed = build_stable_seed("dm_roast", birth_date.toordinal(), stem_id)
    pick = random.Random(seed).choice(pool)
    master = DAY_MASTER_BANK[stem_id]

    gender_key = normalise_gender(gender)
    arah = None
    if gender_key is not None:
        key = resolve_luck_direction(year_stem, gender_key)
        arah_pool = ROAST_DIRECTION_BANK[key]
        arah_seed = build_stable_seed("dir_roast", birth_date.toordinal(), gender_key)
        arah_pick = random.Random(arah_seed).choice(arah_pool)
        arah = {
            "direction": key,
            "direction_hanzi": "順行" if key == "maju" else "逆行",
            "direction_label": "Searah Arus" if key == "maju" else "Melawan Arus",
            "gender": gender_key,
            "polarity": STEM_POLARITY[year_stem],
            **arah_pick,
        }

    return {
        "year_pillar": HEAVENLY_STEMS[year_stem][1] + EARTHLY_BRANCHES[year_branch][1],
        "year_element": ELEMENT_LABELS[year_element][0],
        "year_element_hanzi": ELEMENT_LABELS[year_element][1],
        "year_polarity": STEM_POLARITY[year_stem],
        "shio_name": SHIO_DATA[actual_shio]["name"],
        "shio_key": actual_shio,
        "shio_hanzi": SHIO_DATA[actual_shio]["hanzi"],
        "day_master": {
            "stem_id": stem_id,
            "stem_hanzi": HEAVENLY_STEMS[day_stem][1],
            "stem_name": HEAVENLY_STEMS[day_stem][0],
            "pillar_hanzi": HEAVENLY_STEMS[day_stem][1] + EARTHLY_BRANCHES[day_branch][1],
            "title": master["title"],
            "element": master["element"],
            "polarity": master["polarity"],
            **pick,
        },
        "direction": arah,
    }


def describe_pair_roast(shio1_key, shio2_key):
    idx1 = SHIOS_LIST.index(shio1_key)
    idx2 = SHIOS_LIST.index(shio2_key)
    relation_key = get_branch_relation(idx1, idx2)
    meta = PAIR_RELATION_BANK[relation_key]
    seed = build_stable_seed("pair_roast", shio1_key, shio2_key)
    pool = ROAST_PAIR_BANK[relation_key]
    pick = random.Random(seed).choice(pool)
    return {
        "shio1": {"key": shio1_key, "name": SHIO_DATA[shio1_key]["name"],
                  "hanzi": SHIO_DATA[shio1_key]["hanzi"]},
        "shio2": {"key": shio2_key, "name": SHIO_DATA[shio2_key]["name"],
                  "hanzi": SHIO_DATA[shio2_key]["hanzi"]},
        "relation_key": relation_key,
        "relation_label": meta["label"],
        "relation_hanzi": meta["hanzi"],
        "relation_title": meta["title"],
        "code": meta["code"],
        "variants": len(pool),
        **pick,
    }


DAY_MASTER_BANK_KEYS = [
    "jia", "yi", "bing", "ding", "wu", "ji", "geng", "xin", "ren", "gui",
]


ROAST_VARIANT_POOLS = ("headlines", "catchphrases", "survival_tips")


def build_roast_variants(roast):
    pools = [roast.get(name) or [] for name in ROAST_VARIANT_POOLS]
    longest = max((len(pool) for pool in pools), default=0)
    variants = []
    for index in range(longest):
        headline, catchphrase, survival_tip = (
            pool[index % len(pool)] if pool else "" for pool in pools
        )
        variants.append(
            {
                "headline": headline,
                "catchphrase": catchphrase,
                "survival_tip": survival_tip,
            }
        )
    return variants


def count_roast_combinations(roast):
    total = 1
    for name in ROAST_VARIANT_POOLS:
        total *= max(len(roast.get(name) or []), 1)
    return total


def get_shio_roasting(shio_key=None, partner_key=None, birth_date_str=None,
                      gender=None):
    birth_date = parse_birth_date(birth_date_str) if birth_date_str else None
    if birth_date is not None:
        shio_key = SHIOS_LIST[get_year_pillar(birth_date)[1]]
    if not shio_key:
        return {"error": "Isi tanggal lahir dulu."}
    roast = SHIO_ROASTING_BANK.get(shio_key)
    if not roast:
        return {"error": f"Shio '{shio_key}' tidak ditemukan."}
    partner_roast = None
    if partner_key and partner_key in SHIO_ROASTING_BANK:
        partner_roast = describe_pair_roast(shio_key, partner_key)

    return {
        **roast,
        "variants": build_roast_variants(roast),
        "combination_count": count_roast_combinations(roast),
        "traits_per_draw": ROAST_TRAITS_PER_DRAW,
        "pair_roast": partner_roast,
        "chart_roast": describe_chart_roast(birth_date_str, gender),
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


COOKIE_TONE_PERIOD = 60

COOKIE_TONE_BASE = COOKIE_TONE_PERIOD * (
    datetime.date(2000, 1, 1).toordinal() // COOKIE_TONE_PERIOD
)

COOKIE_TONE_TABLE = {}


def get_cookie_tone_table(shio_key):
    table = COOKIE_TONE_TABLE.get(shio_key)
    if table is None:
        table = [
            pick_day_tone(
                describe_cookie_day(
                    shio_key, datetime.date.fromordinal(COOKIE_TONE_BASE + offset)
                )
            )
            for offset in range(COOKIE_TONE_PERIOD)
        ]
        COOKIE_TONE_TABLE[shio_key] = table
    return table


def count_tone_days(shio_key, tone, ordinal):
    table = get_cookie_tone_table(shio_key)
    full_cycles, offset = divmod(ordinal, COOKIE_TONE_PERIOD)
    return full_cycles * table.count(tone) + table[: offset + 1].count(tone) - 1


def rotate_pool(pool, shio_key, tone, ordinal):
    index = count_tone_days(shio_key, tone, ordinal)
    cycle, position = divmod(index, len(pool))
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
    {"key": key, "name": name, "zone": zone, "province": province}
    for key, (name, _longitude, zone, province) in sorted(
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


def describe_relation_item(key, slots, branches, reach):
    meta = CHART_RELATION_BANK[key]
    return {
        "key": key,
        "hanzi": meta["hanzi"],
        "title": meta["title"],
        "code": meta["code"],
        "note": meta["note"],
        "advice": meta["advice"],
        "slots": [PILLAR_POSITION_BANK[slot]["label"] for slot in slots],
        "branches": "".join(EARTHLY_BRANCHES[b][1] for b in branches),
        "reach": reach,
        "reach_label": CHART_RELATION_REACH[reach]["label"] if reach else None,
        "reach_note": CHART_RELATION_REACH[reach]["note"] if reach else None,
    }


def describe_chart_relations(chart):
    relations = chart["relations"]
    items = []
    for triad in relations["triads"]:
        item = describe_relation_item("triad", triad["slots"], triad["branches"], None)
        element = SAN_HE_ELEMENT[triad["group"]]
        item["element"] = ELEMENT_LABELS[element][0]
        item["element_hanzi"] = ELEMENT_LABELS[element][1]
        items.append(item)
    for pair in relations["pairs"]:
        reach = "adjacent" if pair["adjacent"] else "distant"
        for key in pair["relations"]:
            items.append(describe_relation_item(key, pair["slots"], pair["branches"], reach))
    weakened = any(value < 1.0 for value in chart["branch_factors"].values())
    return {
        "items": items,
        "clash_note": CHART_RELATION_CLASH_NOTE if weakened else None,
    }


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
            "late_zi_alternative_day": (
                chart["late_zi_alternative_day"]["pillar_hanzi"]
                if chart["late_zi_alternative_day"]
                else None
            ),
            "city_zone_only": bool(chart["city"]) and not chart["has_hour"],
            "city_unrecognized": bool(city_key) and chart["city"] is None,
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
        "relations": describe_chart_relations(chart),
        "shen_sha": describe_shen_sha(chart),
        "luck": describe_luck(chart),
        "heritage": describe_heritage(chart),
        "no_birth_time": None if chart["has_hour"] else NO_BIRTH_TIME_BANK,
    }


class QuizUnavailable(Exception):
    pass


class QuizError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


class Transaction:
    def __init__(self, cursor, dialect):
        self.cursor = cursor
        self.dialect = dialect

    def prepare(self, sql):
        if self.dialect == "sqlite":
            return sql.replace("%s", "?")
        return sql

    def execute(self, sql, params=()):
        self.cursor.execute(self.prepare(sql), tuple(params))
        return self.cursor.rowcount

    def fetch_one(self, sql, params=()):
        self.execute(sql, params)
        row = self.cursor.fetchone()
        return dict(row) if row is not None else None

    def fetch_all(self, sql, params=()):
        self.execute(sql, params)
        return [dict(row) for row in self.cursor.fetchall()]

    def lock_room(self, room_code):
        suffix = " FOR UPDATE" if self.dialect == "mysql" else ""
        return self.fetch_one(
            "SELECT * FROM shio_rooms WHERE room_code = %s" + suffix, (room_code,)
        )


class RoomStore:
    def __init__(self, connect, dialect, unavailable_errors=(), integrity_errors=(),
                 on_unavailable=None):
        self.connect = connect
        self.dialect = dialect
        self.unavailable_errors = tuple(unavailable_errors)
        self.integrity_errors = tuple(integrity_errors)
        self.on_unavailable = on_unavailable

    def report_unavailable(self, error):
        if self.on_unavailable is not None:
            self.on_unavailable(error)

    @contextmanager
    def transaction(self):
        try:
            conn = self.connect()
        except self.unavailable_errors as error:
            self.report_unavailable(error)
            raise QuizUnavailable() from error
        if conn is None:
            raise QuizUnavailable()
        try:
            if self.dialect == "sqlite":
                conn.execute("BEGIN IMMEDIATE")
            else:
                with conn.cursor() as setup:
                    setup.execute("SET TRANSACTION ISOLATION LEVEL READ COMMITTED")
                conn.begin()
            cursor = conn.cursor()
            yield Transaction(cursor, self.dialect)
            conn.commit()
        except self.unavailable_errors as error:
            rollback_quietly(conn)
            self.report_unavailable(error)
            raise QuizUnavailable() from error
        except BaseException:
            rollback_quietly(conn)
            raise
        finally:
            try:
                conn.close()
            except Exception:
                pass


def rollback_quietly(conn):
    try:
        conn.rollback()
    except Exception:
        pass


def open_sqlite_connection(path):
    conn = sqlite3.connect(path, timeout=10, isolation_level=None)
    conn.row_factory = sqlite3.Row
    return conn


SQLITE_SCHEMA = [
    """CREATE TABLE IF NOT EXISTS shio_rooms (
        room_code TEXT PRIMARY KEY,
        mode TEXT NOT NULL,
        relation_type TEXT,
        status TEXT NOT NULL,
        capacity INTEGER NOT NULL,
        settings_json TEXT NOT NULL,
        state_json TEXT,
        result_json TEXT,
        creator_device TEXT NOT NULL,
        created_at TEXT NOT NULL,
        updated_at TEXT NOT NULL,
        expires_at TEXT NOT NULL
    )""",
    "CREATE INDEX IF NOT EXISTS idx_shio_rooms_expires ON shio_rooms (expires_at)",
    "CREATE INDEX IF NOT EXISTS idx_shio_rooms_creator ON shio_rooms (creator_device, created_at)",
    """CREATE TABLE IF NOT EXISTS shio_room_participants (
        room_code TEXT NOT NULL,
        slot INTEGER NOT NULL,
        participant_token TEXT NOT NULL UNIQUE,
        name TEXT NOT NULL,
        birth_date TEXT NOT NULL,
        shio_key TEXT NOT NULL,
        answers_json TEXT,
        progress_json TEXT,
        joined_at TEXT NOT NULL,
        PRIMARY KEY (room_code, slot)
    )""",
]


def build_sqlite_store(path):
    store = RoomStore(
        lambda: open_sqlite_connection(path),
        "sqlite",
        unavailable_errors=(sqlite3.OperationalError,),
        integrity_errors=(sqlite3.IntegrityError,),
    )
    conn = open_sqlite_connection(path)
    try:
        for statement in SQLITE_SCHEMA:
            conn.execute(statement)
    finally:
        conn.close()
    return store


def build_mysql_store():
    from core import db

    if not db.HAS_PYMYSQL:
        return RoomStore(lambda: None, "mysql")

    import pymysql

    def on_unavailable(error):
        if isinstance(error, (pymysql.err.OperationalError, pymysql.err.InterfaceError)):
            db.mark_db_offline()

    return RoomStore(
        db.get_mysql_connection,
        "mysql",
        unavailable_errors=(
            pymysql.err.OperationalError,
            pymysql.err.InterfaceError,
            pymysql.err.ProgrammingError,
        ),
        integrity_errors=(pymysql.err.IntegrityError,),
        on_unavailable=on_unavailable,
    )


MODE_LIMITS = {"pasangan": (2, 2), "kelompok": (3, 8), "tebak": (3, 8)}
SLOT_LIMITS = (1, 8)
HOST_SLOT = 1

ROOM_CODE_ALPHABET = "0123456789ABCDEFGHJKMNPQRSTVWXYZ"
ROOM_CODE_LENGTH = 6
ROOM_CODE_ATTEMPTS = 5
ROOM_CODE_ALIASES = str.maketrans({"O": "0", "I": "1", "L": "1"})

ROOM_TTL = datetime.timedelta(hours=24)
ROOM_CREATE_WINDOW = datetime.timedelta(hours=1)
ROOM_CREATE_LIMIT = 10

NAME_MAX_LENGTH = 24
TOKEN_BYTES = 24
MOMENT_FORMAT = "%Y-%m-%d %H:%M:%S"

PAIR_SHIO_WEIGHT = 0.4
PAIR_ANSWER_WEIGHT = 0.6
PAIR_SHIO_SUPPORT_MIN = 60
PAIR_ANSWER_MATCH_MIN = 60
PAIR_VERDICT_QUADRANTS = {
    (True, True): "sejalan",
    (False, True): "beda_bawaan",
    (True, False): "beda_kebiasaan",
    (False, False): "perlu_usaha",
}
PAIR_DISTANCE_LABELS = ["Sama persis", "Berdekatan", "Berjauhan", "Berseberangan"]
PAIR_PAIRING_FLOORS = [0.9, 0.7, 0.5, 0.0]

GUESS_HINT_START = 3
GUESS_VERDICT_TIERS = [(67, "terbaca"), (34, "sebagian"), (0, "misterius")]

STATUS_LOBBY = "lobby"
STATUS_PLAYING = "playing"
STATUS_DONE = "done"


def utc_now():
    return datetime.datetime.now(datetime.timezone.utc).replace(tzinfo=None, microsecond=0)


def format_moment(moment):
    return moment.strftime(MOMENT_FORMAT)


def read_moment(value):
    if isinstance(value, datetime.datetime):
        return value
    return datetime.datetime.strptime(str(value), MOMENT_FORMAT)


def hash_token(token):
    return hashlib.sha256(token.encode("utf-8")).hexdigest()


def generate_room_code():
    return "".join(secrets.choice(ROOM_CODE_ALPHABET) for _ in range(ROOM_CODE_LENGTH))


def normalise_room_code(value):
    if not isinstance(value, str):
        return None
    code = re.sub(r"[\s-]", "", value).upper().translate(ROOM_CODE_ALIASES)
    if len(code) != ROOM_CODE_LENGTH:
        return None
    if any(char not in ROOM_CODE_ALPHABET for char in code):
        return None
    return code


def clean_name(value):
    if not isinstance(value, str):
        raise QuizError("Nama wajib diisi.")
    text = "".join(
        char for char in unicodedata.normalize("NFC", value)
        if not unicodedata.category(char).startswith("C")
    )
    text = " ".join(text.split())
    if not text:
        raise QuizError("Nama wajib diisi.")
    if len(text) > NAME_MAX_LENGTH:
        raise QuizError(f"Nama maksimal {NAME_MAX_LENGTH} karakter.")
    return text


def read_person(payload):
    name = clean_name(payload.get("name"))
    birth_date = parse_birth_date(payload.get("birth_date"))
    if birth_date is None:
        raise QuizError("Tanggal lahir tidak valid.")
    return {
        "name": name,
        "birth_date": birth_date.isoformat(),
        "shio_key": SHIOS_LIST[get_year_pillar(birth_date)[1]],
    }


def load_json(value, fallback):
    if not value:
        return fallback
    return json.loads(value)


def dump_json(value):
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"))


def normalise_participant(row):
    return {
        **row,
        "slot": int(row["slot"]),
        "birth_date": str(row["birth_date"]),
        "answers": load_json(row.get("answers_json"), None),
        "progress": load_json(row.get("progress_json"), {}),
    }


def fetch_participants(tx, room_code):
    rows = tx.fetch_all(
        "SELECT * FROM shio_room_participants WHERE room_code = %s ORDER BY slot",
        (room_code,),
    )
    return [normalise_participant(row) for row in rows]


def require_room(room, now):
    if room is None or read_moment(room["expires_at"]) <= now:
        raise QuizError("Room tidak ditemukan atau sudah kedaluwarsa.", 404)
    return room


def load_room(tx, room_code, now, lock=True):
    if lock:
        room = tx.lock_room(room_code)
    else:
        room = tx.fetch_one("SELECT * FROM shio_rooms WHERE room_code = %s", (room_code,))
    return require_room(room, now)


def find_member(participants, token):
    if not isinstance(token, str) or not token:
        return None
    token_hash = hash_token(token)
    for participant in participants:
        if secrets.compare_digest(participant["participant_token"], token_hash):
            return participant
    return None


def require_member(participants, token):
    member = find_member(participants, token)
    if member is None:
        raise QuizError("Kamu belum terdaftar di room ini.", 403)
    return member


def touch_room(tx, room_code, now, **fields):
    assignments = ["updated_at = %s"]
    params = [format_moment(now)]
    for column, value in fields.items():
        assignments.append(column + " = %s")
        params.append(value)
    params.append(room_code)
    tx.execute(
        "UPDATE shio_rooms SET " + ", ".join(assignments) + " WHERE room_code = %s",
        params,
    )


def insert_participant(tx, room_code, slot, person, now):
    if not SLOT_LIMITS[0] <= slot <= SLOT_LIMITS[1]:
        raise QuizError("Slot peserta di luar batas.", 409)
    token = secrets.token_urlsafe(TOKEN_BYTES)
    tx.execute(
        "INSERT INTO shio_room_participants "
        "(room_code, slot, participant_token, name, birth_date, shio_key, joined_at) "
        "VALUES (%s, %s, %s, %s, %s, %s, %s)",
        (room_code, slot, hash_token(token), person["name"], person["birth_date"],
         person["shio_key"], format_moment(now)),
    )
    return token


def purge_expired_rooms(store, now):
    cutoff = format_moment(now)
    with store.transaction() as tx:
        tx.execute(
            "DELETE FROM shio_room_participants WHERE room_code IN "
            "(SELECT room_code FROM shio_rooms WHERE expires_at <= %s)",
            (cutoff,),
        )
        return tx.execute("DELETE FROM shio_rooms WHERE expires_at <= %s", (cutoff,))


def read_room_settings(payload, mode):
    if mode not in MODE_LIMITS:
        raise QuizError("Mode quiz tidak dikenal.")
    relation_type = None
    settings = {}
    if mode == "pasangan":
        relation_type = payload.get("relation_type")
        if relation_type not in RELATION_LENS:
            raise QuizError("Pilih jenis hubungan dulu: asmara, pertemanan, atau rekan kerja.")
        settings["question_ids"] = list(PAIR_LENS_QUESTION_IDS[relation_type])
    if mode == "tebak":
        flavor = payload.get("flavor") or "manis"
        if flavor not in GUESS_FLAVOR_BANK:
            raise QuizError("Pilih rasa petunjuk: manis atau pedas.")
        settings["flavor"] = flavor
    return relation_type, settings


def create_room(store, payload, device, now=None):
    now = now or utc_now()
    mode = payload.get("mode")
    relation_type, settings = read_room_settings(payload, mode)
    person = read_person(payload)
    purge_expired_rooms(store, now)
    with store.transaction() as tx:
        recent = tx.fetch_one(
            "SELECT COUNT(*) AS total FROM shio_rooms "
            "WHERE creator_device = %s AND created_at > %s",
            (device, format_moment(now - ROOM_CREATE_WINDOW)),
        )
        if int(recent["total"]) >= ROOM_CREATE_LIMIT:
            raise QuizError(
                "Kamu sudah membuat terlalu banyak room dalam satu jam. Coba lagi nanti.", 429
            )
        room_code = None
        for _ in range(ROOM_CODE_ATTEMPTS):
            candidate = generate_room_code()
            if tx.fetch_one(
                "SELECT room_code FROM shio_rooms WHERE room_code = %s", (candidate,)
            ):
                continue
            try:
                tx.execute(
                    "INSERT INTO shio_rooms (room_code, mode, relation_type, status, "
                    "capacity, settings_json, creator_device, created_at, updated_at, "
                    "expires_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)",
                    (candidate, mode, relation_type, STATUS_LOBBY, MODE_LIMITS[mode][1],
                     dump_json(settings), device, format_moment(now), format_moment(now),
                     format_moment(now + ROOM_TTL)),
                )
            except store.integrity_errors:
                continue
            room_code = candidate
            break
        if room_code is None:
            raise QuizError("Gagal membuat kode room. Coba sekali lagi.", 503)
        token = insert_participant(tx, room_code, HOST_SLOT, person, now)
    return {"room_code": room_code, "token": token, "slot": HOST_SLOT}


def join_room(store, room_code, payload, now=None):
    now = now or utc_now()
    person = read_person(payload)
    with store.transaction() as tx:
        room = load_room(tx, room_code, now)
        if room["status"] != STATUS_LOBBY:
            raise QuizError("Room ini sudah mulai atau selesai, tidak bisa bergabung lagi.", 409)
        participants = fetch_participants(tx, room_code)
        if len(participants) >= int(room["capacity"]):
            raise QuizError("Room sudah penuh.", 409)
        slot = max(p["slot"] for p in participants) + 1 if participants else HOST_SLOT
        token = insert_participant(tx, room_code, slot, person, now)
        status = room["status"]
        if room["mode"] == "pasangan" and len(participants) + 1 == int(room["capacity"]):
            status = STATUS_PLAYING
        touch_room(tx, room_code, now, status=status)
    return {"room_code": room_code, "token": token, "slot": slot}


PAIR_QUESTIONS_BY_ID = {question["id"]: question for question in PAIR_QUIZ_QUESTIONS}


def get_pair_questions(question_ids):
    return [PAIR_QUESTIONS_BY_ID[question_id] for question_id in question_ids]


def get_room_pair_questions(room):
    settings = load_json(room["settings_json"], {})
    return get_pair_questions(settings.get("question_ids") or LEGACY_PAIR_QUESTION_IDS)


def read_pair_answers(answers, questions):
    if not isinstance(answers, list) or len(answers) != len(questions):
        raise QuizError("Jawab semua soal dulu.")
    cleaned = []
    for answer, question in zip(answers, questions):
        if isinstance(answer, bool) or not isinstance(answer, int):
            raise QuizError("Format jawaban tidak dikenal.")
        if not 0 <= answer < len(question["options"]):
            raise QuizError("Pilihan jawaban di luar daftar.")
        cleaned.append(answer)
    return cleaned


def resolve_tier(score, tiers):
    for floor, key in tiers:
        if score >= floor:
            return key
    return tiers[-1][1]


def score_pair_answer(question, first, second):
    pairing = question.get("pairing")
    if pairing:
        value = pairing[first][second]
        bucket = next(i for i, floor in enumerate(PAIR_PAIRING_FLOORS) if value >= floor)
        return value, bucket, question["pairing_labels"][bucket]
    span = len(question["options"]) - 1
    distance = abs(first - second)
    label = PAIR_DISTANCE_LABELS[min(distance, len(PAIR_DISTANCE_LABELS) - 1)]
    return 1 - distance / span, distance, label


def compare_pair_answers(answers1, answers2, questions):
    rows = []
    closeness = []
    for question, first, second in zip(questions, answers1, answers2):
        value, distance, label = score_pair_answer(question, first, second)
        closeness.append(value)
        rows.append({
            "question": question["question"],
            "answer1": question["options"][first],
            "answer2": question["options"][second],
            "distance": distance,
            "label": label,
        })
    return rows, round(100 * sum(closeness) / len(closeness))


def resolve_pair_verdict_key(shio_score, answer_score):
    return PAIR_VERDICT_QUADRANTS[
        (shio_score >= PAIR_SHIO_SUPPORT_MIN, answer_score >= PAIR_ANSWER_MATCH_MIN)
    ]


def build_pair_result(room, participants):
    first, second = participants[0], participants[1]
    lens = room["relation_type"]
    compat = get_shio_compatibility(
        birth1=first["birth_date"],
        birth2=second["birth_date"],
        lens=lens,
        names=(first["name"], second["name"]),
    )
    for side in ("shio1", "shio2"):
        if compat.get("year_layer"):
            compat["year_layer"][side].pop("date", None)
    comparisons, answer_score = compare_pair_answers(
        first["answers"], second["answers"], get_room_pair_questions(room)
    )
    shio_score = int(compat.get("score", 50))
    total = round(PAIR_SHIO_WEIGHT * shio_score + PAIR_ANSWER_WEIGHT * answer_score)
    tier = resolve_pair_verdict_key(shio_score, answer_score)
    variants = PAIR_VERDICT_BANK[tier]
    verdict = variants[build_stable_seed(room["room_code"], tier) % len(variants)]
    return {
        "score": total,
        "shio_score": shio_score,
        "answer_score": answer_score,
        "weights": {"shio": PAIR_SHIO_WEIGHT, "answers": PAIR_ANSWER_WEIGHT},
        "verdict": {"key": tier, **verdict},
        "comparisons": comparisons,
        "compatibility": compat,
    }


def submit_answers(store, room_code, token, answers, now=None):
    now = now or utc_now()
    with store.transaction() as tx:
        room = load_room(tx, room_code, now)
        if room["mode"] != "pasangan":
            raise QuizError("Mode ini tidak memakai soal.")
        cleaned = read_pair_answers(answers, get_room_pair_questions(room))
        participants = fetch_participants(tx, room_code)
        member = require_member(participants, token)
        if room["status"] == STATUS_DONE:
            raise QuizError("Hasil room ini sudah terkunci.", 409)
        if member["answers"] is not None:
            raise QuizError("Jawabanmu sudah tersimpan.", 409)
        tx.execute(
            "UPDATE shio_room_participants SET answers_json = %s "
            "WHERE room_code = %s AND slot = %s",
            (dump_json(cleaned), room_code, member["slot"]),
        )
        member["answers"] = cleaned
        complete = (
            len(participants) == int(room["capacity"])
            and all(p["answers"] is not None for p in participants)
        )
        if complete:
            result = build_pair_result(room, participants)
            touch_room(tx, room_code, now, status=STATUS_DONE, result_json=dump_json(result))
        else:
            touch_room(tx, room_code, now)
    return {"completed": complete}


def build_group_result(room, participants):
    members = [
        {"slot": p["slot"], "name": p["name"], "shio_key": p["shio_key"]}
        for p in participants
    ]
    return describe_group_dynamic(members, room["room_code"])


def build_guess_rounds(participants, flavor, rng):
    order = list(participants)
    rng.shuffle(order)
    return [
        {"target_slot": p["slot"], "hints": build_guess_hints(p["shio_key"], flavor, rng)}
        for p in order
    ]


def start_room(store, room_code, token, now=None):
    now = now or utc_now()
    with store.transaction() as tx:
        room = load_room(tx, room_code, now)
        participants = fetch_participants(tx, room_code)
        member = require_member(participants, token)
        if room["mode"] == "pasangan":
            raise QuizError("Ramalan Pasangan mulai otomatis setelah berdua.")
        if member["slot"] != HOST_SLOT:
            raise QuizError("Hanya pembuat room yang bisa memulai.", 403)
        if room["status"] != STATUS_LOBBY:
            raise QuizError("Room ini sudah dimulai.", 409)
        minimum = MODE_LIMITS[room["mode"]][0]
        if len(participants) < minimum:
            raise QuizError(f"Butuh minimal {minimum} orang untuk mulai.", 409)
        if room["mode"] == "kelompok":
            result = build_group_result(room, participants)
            touch_room(tx, room_code, now, status=STATUS_DONE, result_json=dump_json(result))
        else:
            settings = load_json(room["settings_json"], {})
            rng = random.Random(secrets.randbits(64))
            state = {"rounds": build_guess_rounds(participants, settings.get("flavor", "manis"), rng)}
            touch_room(tx, room_code, now, status=STATUS_PLAYING, state_json=dump_json(state))
    return {"started": True}


def guess_points(attempt, options):
    if options <= 1:
        return 100
    return round(100 * (options - attempt) / (options - 1))


def round_entry(progress, index):
    return progress.get(str(index), {"attempts": [], "solved": False, "points": 0})


def find_current_round(rounds, member):
    for index, item in enumerate(rounds):
        if item["target_slot"] == member["slot"]:
            continue
        if not round_entry(member["progress"], index)["solved"]:
            return index
    return None


def is_guess_complete(rounds, participants):
    return all(find_current_round(rounds, p) is None for p in participants)


def submit_guess(store, room_code, token, round_index, guess_slot, now=None):
    now = now or utc_now()
    if isinstance(round_index, bool) or not isinstance(round_index, int):
        raise QuizError("Ronde tidak dikenal.")
    if isinstance(guess_slot, bool) or not isinstance(guess_slot, int):
        raise QuizError("Pilih salah satu teman.")
    with store.transaction() as tx:
        room = load_room(tx, room_code, now)
        if room["mode"] != "tebak":
            raise QuizError("Mode ini tidak memakai tebakan.")
        participants = fetch_participants(tx, room_code)
        member = require_member(participants, token)
        if room["status"] != STATUS_PLAYING:
            raise QuizError("Permainan belum dimulai atau sudah selesai.", 409)
        rounds = load_json(room["state_json"], {"rounds": []})["rounds"]
        if round_index != find_current_round(rounds, member):
            raise QuizError("Ronde ini bukan giliranmu sekarang.", 409)
        slots = {p["slot"] for p in participants}
        if guess_slot == member["slot"] or guess_slot not in slots:
            raise QuizError("Pilih salah satu teman, bukan dirimu sendiri.")
        entry = round_entry(member["progress"], round_index)
        if guess_slot in entry["attempts"]:
            raise QuizError("Teman itu sudah kamu tebak di ronde ini.")
        entry["attempts"].append(guess_slot)
        correct = guess_slot == rounds[round_index]["target_slot"]
        if correct:
            entry["solved"] = True
            entry["points"] = guess_points(len(entry["attempts"]), len(slots) - 1)
        member["progress"][str(round_index)] = entry
        tx.execute(
            "UPDATE shio_room_participants SET progress_json = %s "
            "WHERE room_code = %s AND slot = %s",
            (dump_json(member["progress"]), room_code, member["slot"]),
        )
        if is_guess_complete(rounds, participants):
            result = build_guess_result(room, participants, rounds)
            touch_room(tx, room_code, now, status=STATUS_DONE, result_json=dump_json(result))
        else:
            touch_room(tx, room_code, now)
    return {"correct": correct, "points": entry["points"], "attempts": len(entry["attempts"])}


def build_guess_result(room, participants, rounds):
    by_slot = {p["slot"]: p for p in participants}
    guessers = {p["slot"]: {"points": 0, "solved": 0} for p in participants}
    targets = []
    for index, item in enumerate(rounds):
        target = by_slot[item["target_slot"]]
        scores = []
        for p in participants:
            if p["slot"] == target["slot"]:
                continue
            entry = round_entry(p["progress"], index)
            points = entry["points"] if entry["solved"] else 0
            scores.append(points)
            guessers[p["slot"]]["points"] += points
            guessers[p["slot"]]["solved"] += int(entry["solved"])
        readability = round(sum(scores) / len(scores)) if scores else 0
        tier = resolve_tier(readability, GUESS_VERDICT_TIERS)
        variants = GUESS_VERDICT_BANK[tier]
        verdict = variants[build_stable_seed(room["room_code"], target["slot"]) % len(variants)]
        shio = SHIO_DATA[target["shio_key"]]
        targets.append({
            "slot": target["slot"],
            "name": target["name"],
            "shio": shio["name"],
            "hanzi": shio["hanzi"],
            "readability": readability,
            "verdict": {"key": tier, **verdict},
            "hints": item["hints"],
        })
    leaderboard = sorted(
        (
            {"slot": slot, "name": by_slot[slot]["name"], **tally}
            for slot, tally in guessers.items()
        ),
        key=lambda row: (-row["points"], row["slot"]),
    )
    return {
        "targets": targets,
        "leaderboard": leaderboard,
        "max_points": 100 * (len(participants) - 1),
    }


def finish_room(store, room_code, token, now=None):
    now = now or utc_now()
    with store.transaction() as tx:
        room = load_room(tx, room_code, now)
        participants = fetch_participants(tx, room_code)
        member = require_member(participants, token)
        if member["slot"] != HOST_SLOT:
            raise QuizError("Hanya pembuat room yang bisa mengakhiri permainan.", 403)
        if room["mode"] != "tebak" or room["status"] != STATUS_PLAYING:
            raise QuizError("Tidak ada permainan yang sedang berjalan.", 409)
        rounds = load_json(room["state_json"], {"rounds": []})["rounds"]
        result = build_guess_result(room, participants, rounds)
        touch_room(tx, room_code, now, status=STATUS_DONE, result_json=dump_json(result))
    return {"finished": True}


def describe_participant(participant, member, mode, status):
    visible_shio = mode != "tebak" or status == STATUS_DONE or (
        member is not None and member["slot"] == participant["slot"]
    )
    row = {
        "slot": participant["slot"],
        "name": participant["name"],
        "is_host": participant["slot"] == HOST_SLOT,
        "is_me": member is not None and member["slot"] == participant["slot"],
    }
    if member is not None and visible_shio:
        shio = SHIO_DATA[participant["shio_key"]]
        row["shio"] = shio["name"]
        row["hanzi"] = shio["hanzi"]
    if mode == "pasangan":
        row["answered"] = participant["answers"] is not None
    return row


def describe_guess_turn(room, participants, member):
    rounds = load_json(room["state_json"], {"rounds": []})["rounds"]
    playable = [i for i, item in enumerate(rounds) if item["target_slot"] != member["slot"]]
    index = find_current_round(rounds, member)
    solved = sum(1 for i in playable if round_entry(member["progress"], i)["solved"])
    points = sum(round_entry(member["progress"], i)["points"] for i in playable)
    finished_players = sum(1 for p in participants if find_current_round(rounds, p) is None)
    turn = {
        "total_rounds": len(playable),
        "solved_rounds": solved,
        "points": points,
        "finished_players": finished_players,
        "current": None,
    }
    if index is None:
        return turn
    entry = round_entry(member["progress"], index)
    hints = rounds[index]["hints"]
    shown = min(len(hints), GUESS_HINT_START + len(entry["attempts"]))
    turn["current"] = {
        "round": index,
        "number": playable.index(index) + 1,
        "hints": hints[:shown],
        "hints_total": len(hints),
        "wrong_slots": list(entry["attempts"]),
        "options": [
            {"slot": p["slot"], "name": p["name"]}
            for p in participants if p["slot"] != member["slot"]
        ],
        "max_points": 100,
    }
    return turn


def build_room_view(store, room_code, token, now=None):
    now = now or utc_now()
    with store.transaction() as tx:
        room = load_room(tx, room_code, now, lock=False)
        participants = fetch_participants(tx, room_code)
    member = find_member(participants, token)
    mode = room["mode"]
    status = room["status"]
    minimum, maximum = MODE_LIMITS[mode]
    settings = load_json(room["settings_json"], {})
    view = {
        "room_code": room["room_code"],
        "mode": mode,
        "mode_title": QUIZ_MODE_BANK[mode]["title"],
        "status": status,
        "min_participants": minimum,
        "max_participants": maximum,
        "participant_count": len(participants),
        "expires_at": read_moment(room["expires_at"]).isoformat() + "Z",
        "updated_at": read_moment(room["updated_at"]).isoformat() + "Z",
        "participants": [describe_participant(p, member, mode, status) for p in participants],
        "me": None,
    }
    if room["relation_type"]:
        view["relation_type"] = room["relation_type"]
        view["relation_label"] = RELATION_LENS[room["relation_type"]]["label"]
    if "flavor" in settings:
        view["flavor"] = settings["flavor"]
        view["flavor_label"] = GUESS_FLAVOR_BANK[settings["flavor"]]["label"]
    if member is None:
        return view
    view["me"] = {
        "slot": member["slot"],
        "name": member["name"],
        "is_host": member["slot"] == HOST_SLOT,
    }
    if mode == "pasangan" and status != STATUS_DONE:
        view["me"]["answered"] = member["answers"] is not None
        if member["answers"] is None:
            view["questions"] = [
                {"id": q["id"], "question": q["question"], "options": q["options"]}
                for q in get_room_pair_questions(room)
            ]
    if mode == "tebak" and status == STATUS_PLAYING:
        view["turn"] = describe_guess_turn(room, participants, member)
    if status == STATUS_DONE:
        view["result"] = load_json(room["result_json"], None)
    return view
