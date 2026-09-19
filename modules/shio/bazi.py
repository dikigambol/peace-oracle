import datetime
import collections
import math
import re
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
    TAO_HUA_BY_GROUP,
    YI_MA_BY_GROUP,
    HUA_GAI_BY_GROUP,
    YUE_DE_BY_GROUP,
    TIAN_DE_BY_MONTH,
    GU_GUA_BY_YEAR,
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

SUPPORTIVE_GODS = frozenset(
    ["bi_jian", "jie_cai", "pian_yin", "zheng_yin"]
)

MONTH_COMMAND_BONUS = 1.5

STRENGTH_THRESHOLDS = [
    (0.15, "cong_ruo"),
    (0.38, "shen_ruo"),
    (0.55, "zhong_he"),
    (0.78, "shen_qiang"),
]

WIB = datetime.timezone(datetime.timedelta(hours=7), "WIB")

LICHUN_LONGITUDE = 315.0

MONTH_BRANCH_YIN = 2


WIB_OFFSET_HOURS = 7


def get_solar_longitude(moment):
    epoch = ephem.Date(moment)
    sun = ephem.Sun()
    sun.compute(epoch)
    return math.degrees(float(ephem.Ecliptic(sun, epoch=epoch).lon)) % 360


def as_local_moment(target):
    if isinstance(target, datetime.datetime):
        return target
    return datetime.datetime(target.year, target.month, target.day, 12, 0)


def get_month_branch(target):
    local = as_local_moment(target)
    utc = local - datetime.timedelta(hours=WIB_OFFSET_HOURS)
    longitude = get_solar_longitude(utc)
    return (int((longitude - LICHUN_LONGITUDE) % 360 // 30) + MONTH_BRANCH_YIN) % 12


def get_day_pillar(target_date):
    jdn = target_date.toordinal() + JULIAN_DAY_OFFSET
    return (jdn + 9) % 10, (jdn + 1) % 12


def get_year_pillar(target):
    month_branch = get_month_branch(target)
    local = as_local_moment(target)
    year = local.year

    if local.month <= 2 and month_branch in (0, 1):
        year -= 1

    return (year - 4) % 10, (year - 4) % 12


def get_month_pillar(target, year_stem):
    branch = get_month_branch(target)
    first_stem = ((year_stem % 5) * 2 + 2) % 10
    offset = (branch - MONTH_BRANCH_YIN) % 12
    return (first_stem + offset) % 10, branch


def get_equation_of_time(moment):
    day_of_year = moment.timetuple().tm_yday
    angle = 2 * math.pi * (day_of_year - 81) / 364
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


def tally_elements(chart):
    tally = {element: 0.0 for element in ELEMENT_LABELS}

    for slot in ("year", "month", "day", "hour"):
        pillar = chart[slot]
        if pillar is None:
            continue
        bonus = MONTH_COMMAND_BONUS if slot == "month" else 1.0
        tally[STEM_ELEMENTS[pillar["stem_index"]]] += 1.0 * bonus
        for position, stem in enumerate(HIDDEN_STEMS[pillar["branch_index"]]):
            weight = HIDDEN_STEM_WEIGHTS[min(position, len(HIDDEN_STEM_WEIGHTS) - 1)]
            tally[STEM_ELEMENTS[stem]] += weight * bonus

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

    for slot in ("year", "month", "day", "hour"):
        pillar = chart[slot]
        if pillar is None:
            continue
        bonus = MONTH_COMMAND_BONUS if slot == "month" else 1.0
        if slot != "day":
            tally[get_ten_god(day_stem, pillar["stem_index"])] += 1.0 * bonus
        for position, stem in enumerate(HIDDEN_STEMS[pillar["branch_index"]]):
            weight = HIDDEN_STEM_WEIGHTS[min(position, len(HIDDEN_STEM_WEIGHTS) - 1)]
            tally[get_ten_god(day_stem, stem)] += weight * bonus

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


def build_four_pillars(birth_date, birth_hour=None, birth_minute=0,
                       city_key=None, gender=None):
    effective_date = birth_date
    solar_offset = None
    resolved_city = None
    hour_branch = None

    if birth_hour is not None:
        matched = resolve_city(city_key)
        city = matched or DEFAULT_CITY
        city_name, city_longitude, city_zone, city_province = BIRTH_CITIES[city]
        zone_meridian = TIME_ZONE_MERIDIANS[city_zone]
        resolved_city = {"key": city, "name": city_name,
                         "province": city_province,
                         "longitude": city_longitude,
                         "zone": city_zone,
                         "zone_meridian": zone_meridian,
                         "assumed": matched is None}

        clock = datetime.datetime(
            birth_date.year, birth_date.month, birth_date.day,
            birth_hour, birth_minute,
        )
        solar_offset = get_true_solar_offset(clock, city_longitude, zone_meridian)
        solar_moment = clock + datetime.timedelta(minutes=solar_offset)

        hour_branch = get_hour_branch(solar_moment.hour)
        effective_date = solar_moment.date()

        if solar_moment.hour >= 23:
            effective_date += datetime.timedelta(days=1)

    term_moment = clock if birth_hour is not None else birth_date
    year_stem, year_branch = get_year_pillar(term_moment)
    month_stem, month_branch = get_month_pillar(term_moment, year_stem)
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
        "true_solar_offset_minutes": round(solar_offset, 1) if solar_offset else None,
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
        )
    else:
        chart["luck"] = None

    return analyse_chart(chart)


def find_month_boundary(target_date, forward=True):
    branch = get_month_branch(target_date)
    step = datetime.timedelta(days=1 if forward else -1)
    probe = target_date

    for _ in range(40):
        probe += step
        if get_month_branch(probe) != branch:
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


def get_luck_start_age(birth_date, direction):
    forward = direction == "maju"
    boundary = find_month_boundary(birth_date, forward)

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
                       month_branch, gender, count=9):
    direction = get_luck_direction(year_stem, gender)
    if direction is None:
        return None
    start = get_luck_start_age(birth_date, direction)
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
