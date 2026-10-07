import collections
import datetime
import random
import re
import secrets
import zlib

from .bank import (
    ANSWERS,
    WANDS,
    BIRTH_NOTE,
    BOND_DIRECTION,
    BOND_SIDES,
    CELTIC_AXIS,
    CELTIC_CROSSING,
    CELTIC_HOPE,
    CELTIC_MOVEMENT,
    CUPS,
    COUNT_WORDS,
    COURT_HEAVY,
    COURT_RANKS,
    DAILY_NOTE,
    DEFAULT_SPREAD,
    DEFAULT_TOPIC,
    PENTACLES,
    DISCLAIMER,
    ELEMENT_LABELS,
    JIWA,
    KELUARGA,
    KELUARGA_TUNGGAL,
    KEPRIBADIAN,
    MAJOR_WEIGHT,
    NAME_MAX_LENGTH,
    NUMBER_REPEAT,
    ORIENTATION_LABELS,
    OVERALL,
    QUESTION_MAX_LENGTH,
    RANKS,
    READING_SPREADS,
    RELATIONSHIP_POSITIONS,
    REVERSED_WEIGHT,
    SOURCES,
    SWORDS,
    SPREADS,
    SUIT_ABSENT,
    SUIT_DOMINANT,
    SUITS,
    TAHUN,
    TIGA_KARTU,
    TONES,
    TOPICS,
    MAJOR_ARCANA,
)

WIB = datetime.timezone(datetime.timedelta(hours=7))
MINOR_SUITS = {"wands": WANDS, "cups": CUPS, "swords": SWORDS, "pentacles": PENTACLES}
TOPIC_KEYS = tuple(TOPICS)
ANSWER_TONES = {"ya": "terang", "belum": "netral", "tidak": "berat"}
TONE_SCORES = {"terang": 1, "netral": 0, "berat": -1}
ROMAN_NUMERALS = [
    (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I"),
]
MONTH_NAMES = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember",
]
BIRTH_FIRST = datetime.date(1900, 1, 1)
YEAR_FIRST = 1900
YEAR_LAST = 2100
FOOL_BIRTH_NUMBER = 22
REVERSED_CHANCE = 0.5


class TarotError(Exception):
    def __init__(self, message, status=400):
        super().__init__(message)
        self.message = message
        self.status = status


def to_roman(number):
    if number == 0:
        return "0"
    parts = []
    for value, symbol in ROMAN_NUMERALS:
        while number >= value:
            parts.append(symbol)
            number -= value
    return "".join(parts)


def build_major(entry):
    return {
        "slug": entry["slug"],
        "arcana": "major",
        "suit": None,
        "rank": None,
        "number": entry["number"],
        "roman": to_roman(entry["number"]),
        "name": entry["name"],
        "name_id": entry["name_id"],
        "element": entry["element"],
        "astrology": entry["astrology"],
        "hebrew": entry["hebrew"],
        "keywords_up": entry["keywords_up"],
        "keywords_rev": entry["keywords_rev"],
        "symbolism": entry["symbolism"],
        "answer_up": entry["answer_up"],
        "answer_rev": entry["answer_rev"],
        "up": entry["up"],
        "rev": entry["rev"],
    }


def build_minor(suit_key, entry):
    suit = SUITS[suit_key]
    rank = next(item for item in RANKS if item["key"] == entry["rank"])
    is_court = rank["key"] in COURT_RANKS
    return {
        "slug": f"{rank['key']}-of-{suit_key}",
        "arcana": "minor",
        "suit": suit_key,
        "rank": rank["key"],
        "number": rank["number"],
        "roman": rank["name"] if is_court or rank["key"] == "ace" else to_roman(rank["number"]),
        "name": f"{rank['name']} of {suit['name']}",
        "name_id": f"{rank['name_id']} {suit['name_id']}",
        "element": suit["element"],
        "astrology": entry["astrology"],
        "hebrew": None,
        "keywords_up": entry["keywords_up"],
        "keywords_rev": entry["keywords_rev"],
        "symbolism": entry["symbolism"],
        "answer_up": entry["answer_up"],
        "answer_rev": entry["answer_rev"],
        "up": entry["up"],
        "rev": entry["rev"],
    }


def build_deck():
    deck = [build_major(entry) for entry in MAJOR_ARCANA]
    for suit_key, entries in MINOR_SUITS.items():
        deck.extend(build_minor(suit_key, entry) for entry in entries)
    return deck


DECK = build_deck()
DECK_SIZE = len(DECK)
CARDS = {card["slug"]: card for card in DECK}
MAJORS_BY_NUMBER = {card["number"]: card for card in DECK if card["arcana"] == "major"}


def as_dict(payload):
    return payload if isinstance(payload, dict) else {}


def stable_seed(*parts):
    return zlib.crc32("|".join(str(part) for part in parts).encode("utf-8"))


def today_wib():
    return datetime.datetime.now(WIB).date()


def is_april_fools(day):
    return day.month == 4 and day.day == 1


def deck_options(day):
    if is_april_fools(day):
        return {"default": "oracolo", "decks": ["oracolo", "rider"]}
    return {"default": "rider", "decks": ["rider"]}


def format_long_date(day):
    return f"{day.day} {MONTH_NAMES[day.month - 1]} {day.year}"


def clean_text(value):
    if not isinstance(value, str):
        return ""
    return re.sub(r"\s+", " ", value).strip()


def read_question(value, required):
    question = clean_text(value)
    if required and not question:
        raise TarotError("Tulis pertanyaanmu dulu.")
    if len(question) > QUESTION_MAX_LENGTH:
        raise TarotError(f"Pertanyaannya terlalu panjang. Ringkas jadi paling banyak {QUESTION_MAX_LENGTH} karakter.")
    return question


def read_name(value, fallback):
    name = clean_text(value)
    if not name:
        return fallback
    if len(name) > NAME_MAX_LENGTH:
        raise TarotError(f"Nama terlalu panjang. Maksimal {NAME_MAX_LENGTH} karakter.")
    return name


def read_topic(value):
    if value in (None, ""):
        return DEFAULT_TOPIC
    if not isinstance(value, str) or value not in TOPICS:
        raise TarotError("Topik bacaan tidak dikenali.")
    return value


def read_spread(value):
    if value in (None, ""):
        return DEFAULT_SPREAD
    if not isinstance(value, str) or value not in READING_SPREADS:
        raise TarotError("Jenis spread tidak dikenali.")
    return value


def read_reversed(value):
    return value if isinstance(value, bool) else True


def read_picks(value, count):
    if not isinstance(value, list) or len(value) != count:
        noun = "kartu" if count == 1 else f"{count} kartu"
        raise TarotError(f"Pilih tepat {noun} dari dek dulu.")
    for item in value:
        if isinstance(item, bool) or not isinstance(item, int) or not 0 <= item < DECK_SIZE:
            raise TarotError("Pilihan kartu tidak dikenali. Kocok ulang dek, lalu pilih lagi.")
    if len(set(value)) != count:
        raise TarotError("Setiap kartu hanya bisa dipilih sekali.")
    return value


def draw_cards(picks, allow_reversed, rng=None):
    rng = rng or secrets.SystemRandom()
    order = list(DECK)
    rng.shuffle(order)
    drawn = []
    for index in picks:
        reversed_ = allow_reversed and rng.random() < REVERSED_CHANCE
        drawn.append((order[index], reversed_))
    return drawn


def orientation_key(reversed_):
    return "rev" if reversed_ else "up"


def card_answer(card, reversed_):
    return card["answer_rev"] if reversed_ else card["answer_up"]


def card_tone(card, reversed_):
    return ANSWER_TONES[card_answer(card, reversed_)]


def suit_label(card):
    return SUITS[card["suit"]]["name_id"] if card["suit"] else None


def card_summary(card):
    return {
        "slug": card["slug"],
        "name": card["name"],
        "name_id": card["name_id"],
        "arcana": card["arcana"],
        "arcana_label": "Arcana Mayor" if card["arcana"] == "major" else "Arcana Minor",
        "suit": card["suit"],
        "suit_label": suit_label(card),
        "rank": card["rank"],
        "number": card["number"],
        "roman": card["roman"],
        "element_label": ELEMENT_LABELS.get(card["element"]),
        "astrology": card["astrology"],
        "hebrew": card["hebrew"],
    }


def card_title(card, reversed_):
    return f"{card['name']} (terbalik)" if reversed_ else card["name"]


def describe_drawn(card, reversed_, topic, position=None):
    side = card[orientation_key(reversed_)]
    tone = card_tone(card, reversed_)
    described = card_summary(card)
    described.update({
        "reversed": reversed_,
        "orientation_label": ORIENTATION_LABELS[reversed_],
        "keywords": card["keywords_rev"] if reversed_ else card["keywords_up"],
        "meaning": side[topic],
        "saran": side["saran"],
        "tone": tone,
        "tone_label": TONES[tone],
    })
    if position:
        described["position"] = position
    return described


def overall_tone(drawn):
    scores = [TONE_SCORES[card_tone(card, reversed_)] for card, reversed_ in drawn]
    average = sum(scores) / len(scores)
    if average > 0.34:
        return "terang"
    if average < -0.34:
        return "berat"
    return "netral"


def describe_overall(drawn, topic):
    tone = overall_tone(drawn)
    return {"tone": tone, "label": TONES[tone], "text": OVERALL[tone][topic]}


def dominant_suit_threshold(count):
    return max(2, -(-count * 3 // 10))


def find_patterns(drawn, allow_reversed):
    count = len(drawn)
    if count < 3:
        return []
    patterns = []
    majors = sum(1 for card, _ in drawn if card["arcana"] == "major")
    if majors * 2 >= count:
        patterns.append({"key": "mayor", "text": MAJOR_WEIGHT["banyak"]})
    elif majors == 0:
        patterns.append({"key": "mayor", "text": MAJOR_WEIGHT["nihil"]})
    suits = collections.Counter(card["suit"] for card, _ in drawn if card["suit"])
    if suits:
        ranking = suits.most_common()
        top_suit, top_count = ranking[0]
        unique_top = len(ranking) == 1 or ranking[1][1] < top_count
        if unique_top and top_count >= dominant_suit_threshold(count):
            patterns.append({"key": "suit", "text": SUIT_DOMINANT[top_suit]})
    if count >= 7:
        absent = [key for key in SUITS if suits[key] == 0]
        if 0 < len(absent) <= 2:
            patterns.append({"key": "absen", "text": " ".join(SUIT_ABSENT[key] for key in absent)})
    numbers = collections.Counter(
        card["number"] for card, _ in drawn if card["arcana"] == "minor" and card["rank"] not in COURT_RANKS
    )
    for number in sorted(numbers):
        if numbers[number] >= 2:
            text = NUMBER_REPEAT[number].format(jumlah=COUNT_WORDS[numbers[number]])
            patterns.append({"key": f"angka-{number}", "text": text})
    courts = sum(1 for card, _ in drawn if card["rank"] in COURT_RANKS)
    if courts >= (2 if count <= 3 else 3):
        patterns.append({"key": "istana", "text": COURT_HEAVY})
    if allow_reversed:
        flipped = sum(1 for _, reversed_ in drawn if reversed_)
        if flipped == count:
            patterns.append({"key": "terbalik", "text": REVERSED_WEIGHT["semua"]})
        elif flipped * 2 >= count:
            patterns.append({"key": "terbalik", "text": REVERSED_WEIGHT["banyak"]})
    return patterns


def tone_score(card, reversed_):
    return TONE_SCORES[card_tone(card, reversed_)]


def celtic_relations(drawn):
    def title(index):
        return card_title(*drawn[index])

    crossing = CELTIC_CROSSING[card_tone(*drawn[1])].format(a=title(0), b=title(1))
    behind, ahead = tone_score(*drawn[4]), tone_score(*drawn[5])
    movement_key = "naik" if ahead > behind else "turun" if ahead < behind else "datar"
    movement = CELTIC_MOVEMENT[movement_key].format(a=title(4), b=title(5))
    hope_key = "sejalan" if tone_score(*drawn[9]) >= tone_score(*drawn[8]) else "berbeda"
    hope = CELTIC_HOPE[hope_key].format(a=title(8), b=title(9))
    axis_key = "searah" if card_tone(*drawn[2]) == card_tone(*drawn[3]) else "berbeda"
    axis = CELTIC_AXIS[axis_key].format(a=title(2), b=title(3))
    return [
        {"key": "silang", "title": "Inti dan yang menyilang", "text": crossing},
        {"key": "mahkota", "title": "Mahkota dan dasar", "text": axis},
        {"key": "arah", "title": "Dari belakang ke depan", "text": movement},
        {"key": "hasil", "title": "Harapan dan hasil", "text": hope},
    ]


def bond_relations(drawn, partner):
    first, second = card_tone(*drawn[0]), card_tone(*drawn[1])
    sides_key = first if first == second else "beda"
    return [
        {"key": "dua_sisi", "title": "Kamu dan " + partner, "text": BOND_SIDES[sides_key].format(dia=partner)},
        {"key": "arah", "title": "Arah hubungan", "text": BOND_DIRECTION[card_tone(*drawn[6])]},
    ]


def describe_topic(topic):
    return {"key": topic, **TOPICS[topic]}


def build_reading(payload, rng=None):
    payload = as_dict(payload)
    question = read_question(payload.get("question"), required=False)
    topic = read_topic(payload.get("topic"))
    spread_key = read_spread(payload.get("spread"))
    spread = SPREADS[spread_key]
    picks = read_picks(payload.get("picks"), len(spread["positions"]))
    allow_reversed = read_reversed(payload.get("reversed"))
    drawn = draw_cards(picks, allow_reversed, rng)
    cards = [
        describe_drawn(card, reversed_, topic, position)
        for (card, reversed_), position in zip(drawn, spread["positions"])
    ]
    return {
        "question": question,
        "topic": describe_topic(topic),
        "spread": {"key": spread_key, "name": spread["name"], "short": spread["short"]},
        "reversed_allowed": allow_reversed,
        "cards": cards,
        "overall": describe_overall(drawn, topic),
        "patterns": find_patterns(drawn, allow_reversed),
        "relations": celtic_relations(drawn) if spread_key == "celtic" else [],
        "disclaimer": DISCLAIMER,
        "sources": SOURCES,
    }


def relationship_positions(partner):
    capital = partner[:1].upper() + partner[1:]
    return [
        {
            "key": position["key"],
            "label": position["label"].format(Dia=capital, dia=partner),
            "prompt": position["prompt"].format(Dia=capital, dia=partner),
        }
        for position in RELATIONSHIP_POSITIONS
    ]


def build_relationship(payload, rng=None):
    payload = as_dict(payload)
    you = read_name(payload.get("nama_a"), "Kamu")
    partner = read_name(payload.get("nama_b"), "dia")
    positions = relationship_positions(partner)
    picks = read_picks(payload.get("picks"), len(positions))
    allow_reversed = read_reversed(payload.get("reversed"))
    drawn = draw_cards(picks, allow_reversed, rng)
    cards = [
        describe_drawn(card, reversed_, "cinta", position)
        for (card, reversed_), position in zip(drawn, positions)
    ]
    return {
        "people": {"a": you, "b": partner},
        "topic": describe_topic("cinta"),
        "spread": {"key": "hubungan", "name": "Bacaan Hubungan", "short": "7 kartu"},
        "reversed_allowed": allow_reversed,
        "cards": cards,
        "overall": describe_overall(drawn, "cinta"),
        "patterns": find_patterns(drawn, allow_reversed),
        "relations": bond_relations(drawn, partner),
        "disclaimer": DISCLAIMER,
        "sources": SOURCES,
    }


def build_answer(payload, rng=None):
    payload = as_dict(payload)
    question = read_question(payload.get("question"), required=True)
    picks = read_picks(payload.get("picks"), 1)
    allow_reversed = read_reversed(payload.get("reversed"))
    (card, reversed_), = draw_cards(picks, allow_reversed, rng)
    answer_key = card_answer(card, reversed_)
    return {
        "question": question,
        "reversed_allowed": allow_reversed,
        "card": describe_drawn(card, reversed_, "umum"),
        "answer": {"key": answer_key, **ANSWERS[answer_key]},
        "disclaimer": DISCLAIMER,
        "sources": SOURCES,
    }


def build_daily(payload, device_id, today=None):
    payload = as_dict(payload)
    today = today or today_wib()
    allow_reversed = read_reversed(payload.get("reversed"))
    rng = random.Random(stable_seed("harian", device_id, today.isoformat()))
    card = rng.choice(DECK)
    reversed_ = rng.random() < REVERSED_CHANCE and allow_reversed
    side = card[orientation_key(reversed_)]
    described = describe_drawn(card, reversed_, "umum")
    described["meanings"] = {topic: side[topic] for topic in TOPIC_KEYS}
    return {
        "date": today.isoformat(),
        "date_label": format_long_date(today),
        "reversed_allowed": allow_reversed,
        "card": described,
        "topics": [describe_topic(topic) for topic in TOPIC_KEYS],
        "note": DAILY_NOTE,
        "disclaimer": DISCLAIMER,
        "sources": SOURCES,
    }


def digit_sum(number):
    return sum(int(digit) for digit in str(number))


def format_digit_sum(number):
    return " + ".join(str(number)) + f" = {digit_sum(number)}"


def reduce_to_major(total):
    steps = []
    value = total
    while value > FOOL_BIRTH_NUMBER:
        steps.append(format_digit_sum(value))
        value = digit_sum(value)
    return value, steps


def birth_chain(value):
    chain = [value]
    steps = []
    while chain[-1] > 9:
        steps.append(format_digit_sum(chain[-1]))
        chain.append(digit_sum(chain[-1]))
    return chain, steps


def major_for_birth_number(number):
    return MAJORS_BY_NUMBER[0 if number == FOOL_BIRTH_NUMBER else number]


def read_birth_date(value, today):
    if not isinstance(value, str) or not value.strip():
        raise TarotError("Isi tanggal lahirmu dulu.")
    try:
        parsed = datetime.date.fromisoformat(value.strip())
    except ValueError:
        raise TarotError("Format tanggal lahir tidak dikenali. Pakai format TTTT-BB-HH.")
    if parsed < BIRTH_FIRST or parsed > today:
        raise TarotError(f"Tanggal lahir harus antara 1 Januari {BIRTH_FIRST.year} dan hari ini.")
    return parsed


def read_year(value, today):
    if value in (None, ""):
        return today.year
    if isinstance(value, str) and value.strip().isdigit():
        value = int(value.strip())
    if isinstance(value, bool) or not isinstance(value, int) or not YEAR_FIRST <= value <= YEAR_LAST:
        raise TarotError(f"Tahun untuk kartu tahunan harus antara {YEAR_FIRST} dan {YEAR_LAST}.")
    return value


def describe_birth_card(number, role, role_label, text):
    card = major_for_birth_number(number)
    return {"role": role, "role_label": role_label, "birth_number": number, "card": card_summary(card), "text": text}


def build_birth_cards(chain):
    if len(chain) == 1:
        number = chain[0]
        return [describe_birth_card(number, "tunggal", "Kartu kepribadian dan jiwa", KEPRIBADIAN[number] + " " + JIWA[number])], KELUARGA_TUNGGAL
    cards = [describe_birth_card(chain[0], "kepribadian", "Kartu kepribadian", KEPRIBADIAN[chain[0]])]
    if len(chain) == 3:
        cards.append(describe_birth_card(chain[1], "penghubung", "Kartu penghubung", KEPRIBADIAN[chain[1]]))
    cards.append(describe_birth_card(chain[-1], "jiwa", "Kartu jiwa", JIWA[chain[-1]]))
    return cards, TIGA_KARTU if len(chain) == 3 else KELUARGA


def build_birth_card(payload, today=None):
    payload = as_dict(payload)
    today = today or today_wib()
    born = read_birth_date(payload.get("tanggal"), today)
    year = read_year(payload.get("tahun"), today)
    total = born.month + born.day + born.year
    value, reduce_steps = reduce_to_major(total)
    chain, chain_steps = birth_chain(value)
    cards, family = build_birth_cards(chain)
    year_total = born.month + born.day + year
    year_value, year_steps = reduce_to_major(year_total)
    year_card = major_for_birth_number(year_value)
    return {
        "input": {"tanggal": born.isoformat(), "tanggal_label": format_long_date(born), "tahun": year},
        "formula": [f"{born.month} + {born.day} + {born.year} = {total}", *reduce_steps, *chain_steps],
        "cards": cards,
        "family": family,
        "year": {
            "tahun": year,
            "formula": [f"{born.month} + {born.day} + {year} = {year_total}", *year_steps],
            "birth_number": year_value,
            "card": card_summary(year_card),
            "text": TAHUN[year_value],
        },
        "note": BIRTH_NOTE,
        "disclaimer": DISCLAIMER,
        "sources": {"greer": SOURCES["greer"], "waite": SOURCES["waite"]},
    }


def card_groups():
    groups = [{"key": "major", "title": "Arcana Mayor", "cards": [card for card in DECK if card["arcana"] == "major"]}]
    for suit_key, suit in SUITS.items():
        groups.append({
            "key": suit_key,
            "title": f"{suit['name_id']} ({suit['name']})",
            "domain": suit["domain"],
            "cards": [card for card in DECK if card["suit"] == suit_key],
        })
    return groups


def card_detail(slug):
    card = CARDS.get(slug)
    if not card:
        return None
    index = DECK.index(card)
    return {
        **card,
        **card_summary(card),
        "prev": DECK[index - 1] if index > 0 else None,
        "next": DECK[index + 1] if index < DECK_SIZE - 1 else None,
        "answer_up_label": ANSWERS[card["answer_up"]]["label"],
        "answer_rev_label": ANSWERS[card["answer_rev"]]["label"],
        "suit_info": SUITS.get(card["suit"]),
    }
