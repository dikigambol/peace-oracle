from flask import Blueprint, abort, jsonify, render_template, request

from core.core import get_device_id, get_fingerprint_id

from .bank import (
    BIRTH_NOTE,
    DAILY_NOTE,
    DEFAULT_SPREAD,
    DEFAULT_TOPIC,
    DISCLAIMER,
    DRAW_NOTE,
    GLOSSARY,
    HUB_FEATURES,
    QUESTION_HINT,
    QUESTION_MAX_LENGTH,
    READING_SPREADS,
    SOURCES,
    SPREADS,
    TOPICS,
    YESNO_HINT,
)
from .data import (
    DECK_SIZE,
    YEAR_FIRST,
    YEAR_LAST,
    BIRTH_FIRST,
    TarotError,
    build_birth_card,
    build_daily,
    build_reading,
    build_relationship,
    build_answer,
    card_detail,
    card_groups,
    deck_options,
    format_long_date,
    is_april_fools,
    relationship_positions,
    today_wib,
)
from .ai_client import explain_answer, reply_to_reading

tarot_bp = Blueprint(
    "tarot",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/tarot-static",
)


@tarot_bp.context_processor
def inject_features():
    today = today_wib()
    options = deck_options(today)
    return {
        "features": HUB_FEATURES,
        "deck_size": DECK_SIZE,
        "april_fools": is_april_fools(today),
        "default_deck": options["default"],
        "decks": options["decks"],
        "deck_day": today.isoformat(),
    }


def render_page(template, **extra):
    return render_template(
        template,
        disclaimer=DISCLAIMER,
        draw_note=DRAW_NOTE,
        question_max=QUESTION_MAX_LENGTH,
        **extra,
    )


def ai_clients():
    return (get_device_id(), get_fingerprint_id())


def build_answered_reading(payload):
    reading = build_reading(payload)
    if reading["question"]:
        reading["reply"] = reply_to_reading(reading, ai_clients())
    return reading


def build_explained_answer(payload):
    result = build_answer(payload)
    result["reply"] = explain_answer(result, ai_clients())
    return result


def api_response(builder, *args):
    try:
        return jsonify(builder(request.get_json(silent=True), *args))
    except TarotError as error:
        return jsonify({"error": error.message}), error.status


@tarot_bp.route("/tarot")
def tarot_index():
    return render_template("tarot/index.html")


@tarot_bp.route("/tarot/daily")
def tarot_daily_page():
    return render_page("tarot/giorno.html", daily_note=DAILY_NOTE, today_label=format_long_date(today_wib()))


@tarot_bp.route("/api/tarot/daily", methods=["POST"])
def tarot_daily_api():
    return api_response(build_daily, get_device_id())


@tarot_bp.route("/tarot/reading")
def tarot_reading_page():
    spreads = [{"key": key, **SPREADS[key]} for key in READING_SPREADS]
    return render_page(
        "tarot/lettura.html",
        topics=TOPICS,
        spreads=spreads,
        default_topic=DEFAULT_TOPIC,
        default_spread=DEFAULT_SPREAD,
        question_hint=QUESTION_HINT,
    )


@tarot_bp.route("/api/tarot/reading", methods=["POST"])
def tarot_reading_api():
    return api_response(build_answered_reading)


@tarot_bp.route("/tarot/answer")
def tarot_answer_page():
    return render_page("tarot/sino.html", yesno_hint=YESNO_HINT)


@tarot_bp.route("/api/tarot/answer", methods=["POST"])
def tarot_answer_api():
    return api_response(build_explained_answer)


@tarot_bp.route("/tarot/relationship")
def tarot_relationship_page():
    return render_page("tarot/legame.html", positions=relationship_positions("dia"))


@tarot_bp.route("/api/tarot/relationship", methods=["POST"])
def tarot_relationship_api():
    return api_response(build_relationship)


@tarot_bp.route("/tarot/birth-card")
def tarot_birth_page():
    today = today_wib()
    return render_page(
        "tarot/nascita.html",
        birth_note=BIRTH_NOTE,
        first_date=BIRTH_FIRST.isoformat(),
        last_date=today.isoformat(),
        this_year=today.year,
        year_first=YEAR_FIRST,
        year_last=YEAR_LAST,
    )


@tarot_bp.route("/api/tarot/birth-card", methods=["POST"])
def tarot_birth_api():
    return api_response(build_birth_card)


@tarot_bp.route("/tarot/cards")
def tarot_cards_page():
    return render_page("tarot/arcani.html", groups=card_groups(), glossary=GLOSSARY, sources=SOURCES)


@tarot_bp.route("/tarot/cards/<slug>")
def tarot_card_page(slug):
    card = card_detail(slug)
    if not card:
        abort(404)
    return render_page("tarot/carta.html", card=card, topics=TOPICS, sources=SOURCES)
