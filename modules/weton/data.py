import calendar
import datetime
import random
import re
import zlib

import ephem

from .bank import (
    HARI,
    PASARAN,
    WUKU,
    SASI,
    TAUN,
    TAUN_WUNTU,
    WINDU,
    WINDU_ADI_ALIP_YEAR,
    KURUP,
    ASAPON_FIRST_YEAR,
    ASAPON_LAST_YEAR,
    ASAPON_START,
    SUPPORTED_FIRST_DATE,
    MANGSA,
    PAARASAN,
    SOURCES,
    WATAK_HARI,
    WATAK_PASARAN,
    WATAK_NEPTU,
    WATAK_PAARASAN,
    WATAK_WUKU,
    WETON_CITIES,
    WETON_CITY_ALIASES,
    WETON_DEFAULT_CITY,
    WETON_ZONE_OFFSETS,
    WETON_LENS,
    DEFAULT_LENS,
    PETUNG,
    PETUNG_RESULTS,
    TONE_LABELS,
    MATCH_DISCLAIMER,
    HARI_ISTIMEWA,
    PANTANGAN,
    PANTANGAN_WUKU,
    TALIWANGKE_SASI,
    KEBLAT_PASARAN,
    CALENDAR_SOURCES,
    CALENDAR_NOTE,
    CALENDAR_DISCLAIMER,
    WETONAN_NOTE,
    ROAST_WETON,
    ROAST_DUO,
    ROAST_DISCLAIMER,
    ROAST_SOURCE,
)

JDN_OFFSET = 1721425
WUKU_EPOCH_ORDINAL = -1721279
WUKU_CYCLE = 210
WINDU_YEARS = 8
YEAR_LENGTH_WASTU = 354
YEAR_LENGTH_WUNTU = 355
FIRST_ELEVEN_SASI_DAYS = sum(30 if index % 2 == 0 else 29 for index in range(11))
SUNSET_HORIZON = "-0:34"
NAME_MAX_LENGTH = 24
WIB = datetime.timezone(datetime.timedelta(hours=7))
DAY = datetime.timedelta(days=1)

ASAPON_START_DATE = datetime.date(*ASAPON_START)
SUPPORTED_FIRST = datetime.date(*SUPPORTED_FIRST_DATE)


class WetonError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def get_taun_name(year):
    return TAUN[(year - ASAPON_FIRST_YEAR) % WINDU_YEARS]


def get_year_length(year):
    return YEAR_LENGTH_WUNTU if get_taun_name(year) in TAUN_WUNTU else YEAR_LENGTH_WASTU


def get_sura_start(year):
    if year >= ASAPON_FIRST_YEAR:
        start = ASAPON_START_DATE
        for previous in range(ASAPON_FIRST_YEAR, year):
            start += datetime.timedelta(days=get_year_length(previous))
        return start
    start = ASAPON_START_DATE + DAY
    for previous in range(year, ASAPON_FIRST_YEAR):
        start -= datetime.timedelta(days=get_year_length(previous))
    return start


SUPPORTED_LAST = get_sura_start(ASAPON_LAST_YEAR + 1) - DAY


def get_kurup(year):
    return KURUP["asapon" if year >= ASAPON_FIRST_YEAR else "aboge"]


def get_windu_name(year):
    alip_year = year - (year - ASAPON_FIRST_YEAR) % WINDU_YEARS
    return WINDU[((alip_year - WINDU_ADI_ALIP_YEAR) // WINDU_YEARS) % len(WINDU)]


def get_javanese_date(day):
    year = ASAPON_FIRST_YEAR + int((day - ASAPON_START_DATE).days // 354.375)
    while get_sura_start(year) > day:
        year -= 1
    while get_sura_start(year + 1) <= day:
        year += 1
    year_start = get_sura_start(year)
    year_length = (get_sura_start(year + 1) - year_start).days
    offset = (day - year_start).days
    for index, sasi in enumerate(SASI):
        if index == len(SASI) - 1:
            length = year_length - FIRST_ELEVEN_SASI_DAYS
        else:
            length = 30 if index % 2 == 0 else 29
        if offset < length:
            break
        offset -= length
    kurup = get_kurup(year)
    return {
        "tanggal": offset + 1,
        "sasi": sasi["name"],
        "sasi_key": sasi["key"],
        "tahun": year,
        "taun": get_taun_name(year),
        "windu": get_windu_name(year),
        "kurup": kurup["name"],
        "kurup_long": kurup["long_name"],
        "year_length": year_length,
    }


def get_weton(day):
    hari = HARI[day.weekday()]
    pasaran = PASARAN[(day.toordinal() + JDN_OFFSET) % len(PASARAN)]
    return {
        "hari": hari["name"],
        "hari_key": hari["key"],
        "hari_jawa": hari["jawa"],
        "pasaran": pasaran["name"],
        "pasaran_key": pasaran["key"],
        "neptu_hari": hari["neptu"],
        "neptu_pasaran": pasaran["neptu"],
        "neptu": hari["neptu"] + pasaran["neptu"],
        "label": f"{hari['name']} {pasaran['name']}",
    }


def get_wuku(day):
    position = (day.toordinal() - WUKU_EPOCH_ORDINAL) % WUKU_CYCLE
    wuku = WUKU[position // 7]
    return {
        "name": wuku["name"],
        "key": wuku["key"],
        "dewa": wuku["dewa"],
        "number": position // 7 + 1,
        "day_in_wuku": position % 7 + 1,
    }


def get_mangsa(day):
    starts = []
    for index, mangsa in enumerate(MANGSA):
        month, date = mangsa["start"]
        year = day.year if (month, date) <= (day.month, day.day) else day.year - 1
        starts.append((datetime.date(year, month, date), index))
    start, index = max(starts)
    mangsa = MANGSA[index]
    following = MANGSA[(index + 1) % len(MANGSA)]
    month, date = following["start"]
    end_year = start.year if (month, date) > (start.month, start.day) else start.year + 1
    end = datetime.date(end_year, month, date) - DAY
    return {
        "number": index + 1,
        "name": mangsa["name"],
        "key": mangsa["key"],
        "sanskrit": mangsa["sanskrit"],
        "candra": mangsa["candra"],
        "arti": mangsa["arti"],
        "start": start.isoformat(),
        "end": end.isoformat(),
    }


def normalise_city_text(value):
    return re.sub(r"[^a-z0-9]+", " ", str(value).lower()).strip()


def build_city_lookup():
    lookup = {}
    bare_names = {}
    for key, row in WETON_CITIES.items():
        bare = normalise_city_text(row[0].split(",")[0])
        bare_names[bare] = bare_names.get(bare, 0) + 1
    for key, row in WETON_CITIES.items():
        lookup[normalise_city_text(key)] = key
        lookup.setdefault(normalise_city_text(row[0]), key)
        bare = normalise_city_text(row[0].split(",")[0])
        if bare_names[bare] == 1:
            lookup.setdefault(bare, key)
    for alias, target in WETON_CITY_ALIASES.items():
        lookup[normalise_city_text(alias)] = target
    return lookup


CITY_LOOKUP = build_city_lookup()

CITY_OPTIONS = [
    {"key": key, "name": row[0], "province": row[4], "zone": row[3]}
    for key, row in sorted(WETON_CITIES.items(), key=lambda item: item[1][0])
]


def resolve_city(value):
    if not value:
        return None
    return CITY_LOOKUP.get(normalise_city_text(value))


def describe_city(key):
    name, latitude, longitude, zone, province = WETON_CITIES[key]
    return {
        "key": key,
        "name": name,
        "province": province,
        "zone": zone,
        "latitude": latitude,
        "longitude": longitude,
    }


def get_sunset(day, city_key):
    _, latitude, longitude, zone, _ = WETON_CITIES[city_key]
    offset = datetime.timedelta(hours=WETON_ZONE_OFFSETS[zone])
    observer = ephem.Observer()
    observer.lat = str(latitude)
    observer.lon = str(longitude)
    observer.elevation = 0
    observer.pressure = 0
    observer.horizon = SUNSET_HORIZON
    observer.date = ephem.Date(datetime.datetime(day.year, day.month, day.day, 12) - offset)
    setting = observer.next_setting(ephem.Sun(), use_center=False).datetime() + offset
    return setting.replace(microsecond=0)


def format_clock(moment):
    return moment.strftime("%H.%M")


def read_birth_date(value):
    if not isinstance(value, str) or not value.strip():
        raise WetonError("Isi tanggal lahir dulu.")
    try:
        parsed = datetime.date.fromisoformat(value.strip())
    except ValueError:
        raise WetonError("Format tanggal lahir tidak dikenali. Pakai format TTTT-BB-HH.")
    if parsed < SUPPORTED_FIRST or parsed > SUPPORTED_LAST:
        raise WetonError(
            f"Hitungan Weton ini mendukung tanggal {format_long_date(SUPPORTED_FIRST)} "
            f"sampai {format_long_date(SUPPORTED_LAST)}."
        )
    return parsed


def read_birth_time(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return None
    if not isinstance(value, str):
        raise WetonError("Format jam lahir tidak dikenali. Pakai format JJ:MM.")
    match = re.fullmatch(r"(\d{1,2})[:.](\d{2})", value.strip())
    if not match or int(match.group(1)) > 23 or int(match.group(2)) > 59:
        raise WetonError("Format jam lahir tidak dikenali. Pakai format JJ:MM.")
    return datetime.time(int(match.group(1)), int(match.group(2)))


def read_city(value):
    if value is None or (isinstance(value, str) and not value.strip()):
        return WETON_DEFAULT_CITY, True
    key = resolve_city(value)
    if key is None:
        raise WetonError("Kota lahir belum ada di daftar. Pilih kota terdekat dari daftar yang tersedia.")
    return key, False


MONTH_NAMES = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]


def format_long_date(day):
    return f"{day.day} {MONTH_NAMES[day.month - 1]} {day.year}"


def describe_javanese_day(day):
    weton = get_weton(day)
    return {
        "weton": weton,
        "wuku": get_wuku(day),
        "jawa": get_javanese_date(day),
        "mangsa": get_mangsa(day),
    }


def build_maghrib_note(birth_time, city, sunset, after_sunset, next_label, same_label, subject=None):
    place = f"di {city['name']}"
    clock = format_clock(sunset)
    who = subject or "kamu"
    who_title = who[:1].upper() + who[1:]
    weton_word = "wetonnya" if subject else "wetonmu"
    if birth_time is None:
        return {
            "kind": "unknown",
            "text": (
                f"Jam lahir tidak diisi, jadi dihitung sebagai lahir siang hari. Kalau {who} lahir setelah "
                f"maghrib (sekitar {clock} {place}), {weton_word} jadi {next_label}."
            ),
            "sunset": clock,
        }
    if after_sunset:
        return {
            "kind": "after",
            "text": (
                f"{who_title} lahir pukul {birth_time.strftime('%H.%M')}, setelah matahari terbenam ({clock} {place}). "
                f"Dalam hitungan Jawa hari sudah berganti, jadi {weton_word} {next_label}."
            ),
            "sunset": clock,
        }
    return {
        "kind": "before",
        "text": (
            f"{who_title} lahir pukul {birth_time.strftime('%H.%M')}, sebelum matahari terbenam ({clock} {place}), "
            f"jadi {weton_word} tetap {same_label}."
        ),
        "sunset": clock,
    }


def build_watak(weton, wuku, paarasan_name):
    return {
        "hari": {"title": f"Watak hari {weton['hari']}", **WATAK_HARI[weton["hari_key"]]},
        "pasaran": {"title": f"Watak pasaran {weton['pasaran']}", **WATAK_PASARAN[weton["pasaran_key"]]},
        "neptu": {"title": f"Watak neptu {weton['neptu']}", **WATAK_NEPTU[weton["neptu"]]},
        "wuku": {"title": f"Watak wuku {wuku['name']}", **WATAK_WUKU[wuku["key"]]},
        "paarasan": {"title": paarasan_name, **WATAK_PAARASAN[paarasan_name]},
    }


def resolve_birth(payload, subject=None):
    payload = payload if isinstance(payload, dict) else {}
    birth_date = read_birth_date(payload.get("tanggal"))
    birth_time = read_birth_time(payload.get("jam"))
    city_key, city_defaulted = read_city(payload.get("kota"))
    city = describe_city(city_key)
    sunset = get_sunset(birth_date, city_key)
    after_sunset = birth_time is not None and birth_time >= sunset.time()
    javanese_day = birth_date + DAY if after_sunset else birth_date
    if javanese_day > SUPPORTED_LAST:
        raise WetonError(
            f"Hitungan Weton ini mendukung tanggal sampai {format_long_date(SUPPORTED_LAST)}."
        )
    note = build_maghrib_note(
        birth_time, city, sunset, after_sunset,
        get_weton(birth_date + DAY)["label"], get_weton(birth_date)["label"], subject,
    )
    return {
        "input": {
            "tanggal": birth_date.isoformat(),
            "tanggal_label": format_long_date(birth_date),
            "jam": birth_time.strftime("%H:%M") if birth_time else None,
            "kota": city,
            "kota_default": city_defaulted,
        },
        "javanese_day": javanese_day,
        "after_sunset": after_sunset,
        "maghrib": note,
    }


def build_birth_reading(payload):
    birth = resolve_birth(payload)
    reading = describe_javanese_day(birth["javanese_day"])
    weton = reading["weton"]
    paarasan_name = PAARASAN[weton["neptu"]]
    return {
        "input": birth["input"],
        "javanese_day": birth["javanese_day"].isoformat(),
        "after_sunset": birth["after_sunset"],
        "weton": weton,
        "wuku": reading["wuku"],
        "jawa": reading["jawa"],
        "mangsa": reading["mangsa"],
        "paarasan": paarasan_name,
        "watak": build_watak(weton, reading["wuku"], paarasan_name),
        "maghrib": birth["maghrib"],
        "sources": SOURCES,
    }


def stable_seed(*parts):
    return zlib.crc32("|".join(str(part) for part in parts).encode("utf-8"))


def today_wib():
    return datetime.datetime.now(WIB).date()


def read_name(value, fallback):
    if value is None:
        return fallback
    if not isinstance(value, str):
        raise WetonError("Nama hanya boleh berupa teks.")
    cleaned = " ".join("".join(ch for ch in value if ch.isprintable()).split())
    if len(cleaned) > NAME_MAX_LENGTH:
        raise WetonError(f"Nama maksimal {NAME_MAX_LENGTH} karakter.")
    return cleaned or fallback


def read_lens(value):
    if value in (None, ""):
        return DEFAULT_LENS
    if value not in WETON_LENS:
        raise WetonError("Pilih jenis hubungan: asmara, pertemanan, atau rekan kerja.")
    return value


def compute_petung(petung_key, total):
    petung = PETUNG[petung_key]
    divisor = petung["divisor"]
    remainder = total % divisor
    return {
        "key": petung_key,
        "name": petung["name"],
        "divisor": divisor,
        "remainder": remainder,
        "result_key": petung["results"][remainder],
        "formula": f"{total} : {divisor} = {total // divisor} sisa {remainder}",
        "source": petung["source"],
    }


def describe_petung_result(result_key, lens, seed):
    result = PETUNG_RESULTS[result_key]
    reading = result["lens"][lens]
    return {
        "key": result_key,
        "name": result["name"],
        "tone": result["tone"],
        "tone_label": TONE_LABELS[result["tone"]],
        "meaning": result["meaning"],
        "inti": reading["inti"],
        "saran": reading["saran"][seed % len(reading["saran"])],
    }


def read_person(payload, fallback_name):
    payload = payload if isinstance(payload, dict) else {}
    name = read_name(payload.get("nama"), fallback_name)
    subject = name if name != fallback_name else fallback_name.lower()
    try:
        birth = resolve_birth(payload, subject)
    except WetonError as error:
        raise WetonError(f"{name}: {error.message}", error.status)
    weton = get_weton(birth["javanese_day"])
    return {
        "nama": name,
        "input": birth["input"],
        "after_sunset": birth["after_sunset"],
        "maghrib": birth["maghrib"],
        "weton": weton,
    }


def build_match_reading(payload, today=None):
    payload = payload if isinstance(payload, dict) else {}
    lens_key = read_lens(payload.get("lens"))
    first = read_person(payload.get("a"), "Orang pertama")
    second = read_person(payload.get("b"), "Orang kedua")
    total = first["weton"]["neptu"] + second["weton"]["neptu"]
    day = (today or today_wib()).isoformat()
    petung = []
    for petung_key in PETUNG:
        computed = compute_petung(petung_key, total)
        seed = stable_seed(first["weton"]["label"], second["weton"]["label"], lens_key, petung_key, day)
        computed["result"] = describe_petung_result(computed.pop("result_key"), lens_key, seed)
        petung.append(computed)
    lens = WETON_LENS[lens_key]
    return {
        "lens": {"key": lens_key, **lens},
        "people": [first, second],
        "total_neptu": total,
        "total_formula": f"{first['weton']['neptu']} + {second['weton']['neptu']} = {total}",
        "petung": petung,
        "disclaimer": MATCH_DISCLAIMER,
        "day": day,
    }


WETON_CYCLE = 35


def read_month(value):
    if not isinstance(value, str) or not re.fullmatch(r"\d{4}-\d{2}", value.strip()):
        raise WetonError("Format bulan tidak dikenali. Pakai format TTTT-BB.")
    year, month = (int(part) for part in value.strip().split("-"))
    if not 1 <= month <= 12:
        raise WetonError("Format bulan tidak dikenali. Pakai format TTTT-BB.")
    return datetime.date(year, month, 1)


def read_calendar_date(value):
    if not isinstance(value, str) or not value.strip():
        raise WetonError("Pilih tanggal dulu.")
    try:
        return datetime.date.fromisoformat(value.strip())
    except ValueError:
        raise WetonError("Format tanggal tidak dikenali. Pakai format TTTT-BB-HH.")


def check_calendar_range(month_start):
    if month_start < SUPPORTED_FIRST.replace(day=1) or month_start > SUPPORTED_LAST.replace(day=1):
        raise WetonError(
            f"Kalender ini mendukung {MONTH_NAMES[SUPPORTED_FIRST.month - 1]} {SUPPORTED_FIRST.year} "
            f"sampai {MONTH_NAMES[SUPPORTED_LAST.month - 1]} {SUPPORTED_LAST.year}."
        )


def shift_month(month_start, step):
    index = month_start.year * 12 + month_start.month - 1 + step
    return datetime.date(index // 12, index % 12 + 1, 1)


def find_istimewa(weton, jawa):
    keys = [
        key for key, item in HARI_ISTIMEWA.items()
        if item["hari"] == weton["hari_key"] and item["pasaran"] == weton["pasaran_key"]
    ]
    if jawa["tanggal"] == 1 and jawa["sasi_key"] == "sura":
        keys.append("satu_sura")
    return keys


def find_pantangan(weton, wuku, jawa):
    found = []
    for kind, wuku_key, hari_key, pasaran_key in PANTANGAN_WUKU:
        if wuku["key"] != wuku_key or weton["hari_key"] != hari_key:
            continue
        if pasaran_key is not None and pasaran_key != weton["pasaran_key"]:
            continue
        found.append({"key": kind, "basis": "wuku", "basis_label": f"menurut wuku {wuku['name']}"})
    if TALIWANGKE_SASI[jawa["sasi_key"]] == (weton["hari_key"], weton["pasaran_key"]):
        found.append({"key": "taliwangke", "basis": "sasi", "basis_label": f"menurut sasi {jawa['sasi']}"})
    return found


def describe_calendar_day(day, today, wetonan_label):
    weton = get_weton(day)
    wuku = get_wuku(day)
    jawa = get_javanese_date(day)
    return {
        "date": day.isoformat(),
        "day": day.day,
        "weekday": day.weekday(),
        "label": format_long_date(day),
        "weton": weton,
        "wuku": wuku,
        "jawa": jawa,
        "mangsa": get_mangsa(day)["key"],
        "istimewa": find_istimewa(weton, jawa),
        "pantangan": find_pantangan(weton, wuku, jawa),
        "wetonan": weton["label"] == wetonan_label,
        "today": day == today,
    }


def find_next_wetonan(label, today):
    for offset in range(WETON_CYCLE):
        day = today + datetime.timedelta(days=offset)
        if day > SUPPORTED_LAST:
            return None
        if get_weton(day)["label"] == label:
            return {"date": day.isoformat(), "label": format_long_date(day), "days": offset}
    return None


def describe_jawa_span(first, last):
    start = get_javanese_date(first)
    end = get_javanese_date(last)
    if start["sasi"] == end["sasi"] and start["tahun"] == end["tahun"]:
        return f"{start['sasi']} {start['tahun']}"
    if start["tahun"] == end["tahun"]:
        return f"{start['sasi']} – {end['sasi']} {end['tahun']}"
    return f"{start['sasi']} {start['tahun']} – {end['sasi']} {end['tahun']}"


def build_wetonan(payload, today):
    if payload is None:
        return None
    if not isinstance(payload, dict):
        raise WetonError("Data weton lahir tidak dikenali.")
    if not payload.get("tanggal"):
        return None
    birth = resolve_birth(payload)
    weton = get_weton(birth["javanese_day"])
    return {
        "input": birth["input"],
        "maghrib": birth["maghrib"],
        "weton": weton,
        "next": find_next_wetonan(weton["label"], today),
        "note": WETONAN_NOTE,
    }


def build_calendar(payload, today=None):
    payload = payload if isinstance(payload, dict) else {}
    today = today or today_wib()
    if payload.get("tanggal"):
        selected = read_calendar_date(payload.get("tanggal"))
        month_start = selected.replace(day=1)
    elif payload.get("bulan"):
        month_start = read_month(payload.get("bulan"))
        selected = today if today.replace(day=1) == month_start else month_start
    else:
        month_start = today.replace(day=1)
        selected = today
    check_calendar_range(month_start)
    wetonan = build_wetonan(payload.get("lahir"), today)
    wetonan_label = wetonan["weton"]["label"] if wetonan else None
    length = calendar.monthrange(month_start.year, month_start.month)[1]
    first = max(month_start, SUPPORTED_FIRST)
    last = min(month_start.replace(day=length), SUPPORTED_LAST)
    selected = min(max(selected, first), last)
    days = []
    mangsa = {}
    day = first
    while day <= last:
        entry = describe_calendar_day(day, today, wetonan_label)
        if entry["mangsa"] not in mangsa:
            mangsa[entry["mangsa"]] = get_mangsa(day)
        days.append(entry)
        day += DAY
    previous = shift_month(month_start, -1)
    following = shift_month(month_start, 1)
    return {
        "month": {
            "key": month_start.strftime("%Y-%m"),
            "label": f"{MONTH_NAMES[month_start.month - 1]} {month_start.year}",
            "jawa_label": describe_jawa_span(first, last),
            "first_weekday": month_start.weekday(),
            "length": length,
            "prev": previous.strftime("%Y-%m") if previous >= SUPPORTED_FIRST.replace(day=1) else None,
            "next": following.strftime("%Y-%m") if following <= SUPPORTED_LAST.replace(day=1) else None,
        },
        "today": today.isoformat(),
        "selected": selected.isoformat(),
        "days": days,
        "mangsa": mangsa,
        "istimewa_info": HARI_ISTIMEWA,
        "pantangan_info": PANTANGAN,
        "keblat": KEBLAT_PASARAN,
        "wetonan": wetonan,
        "note": CALENDAR_NOTE,
        "disclaimer": CALENDAR_DISCLAIMER,
        "sources": CALENDAR_SOURCES,
    }


def weton_key(weton):
    return f"{weton['hari_key']}_{weton['pasaran_key']}"


def seeded_order(items, seed):
    order = list(items)
    random.Random(seed).shuffle(order)
    return order


def build_roasting(payload, today=None):
    payload = payload if isinstance(payload, dict) else {}
    day = (today or today_wib()).isoformat()
    birth = resolve_birth(payload.get("a"))
    weton = get_weton(birth["javanese_day"])
    person = {
        "input": birth["input"],
        "maghrib": birth["maghrib"],
        "weton": weton,
        "paarasan": PAARASAN[weton["neptu"]],
    }
    roasts = seeded_order(ROAST_WETON[weton_key(weton)], stable_seed(weton["label"], "roast", day))
    duo = None
    if payload.get("b") is not None:
        partner = read_person(payload.get("b"), "Orang kedua")
        total = weton["neptu"] + partner["weton"]["neptu"]
        petung = compute_petung("sisa8", total)
        result_key = petung.pop("result_key")
        result = PETUNG_RESULTS[result_key]
        duo = {
            "partner": partner,
            "total": total,
            "formula": f"{weton['neptu']} + {partner['weton']['neptu']} = {total}",
            "petung": {
                **petung,
                "result_key": result_key,
                "result_name": result["name"],
                "tone": result["tone"],
                "tone_label": TONE_LABELS[result["tone"]],
            },
            "roasts": seeded_order(
                ROAST_DUO[result_key], stable_seed(weton["label"], partner["weton"]["label"], "duo", day),
            ),
        }
    return {
        "person": person,
        "roasts": roasts,
        "duo": duo,
        "day": day,
        "disclaimer": ROAST_DISCLAIMER,
        "source": ROAST_SOURCE,
    }
