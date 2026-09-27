from flask import Blueprint, jsonify, render_template, request

from .bank import DEFAULT_LENS, GLOSSARY, HUB_FEATURES, WETON_LENS
from .data import (
    CITY_OPTIONS,
    SUPPORTED_FIRST,
    SUPPORTED_LAST,
    WetonError,
    build_birth_reading,
    build_calendar,
    build_match_reading,
    build_roasting,
)

weton_bp = Blueprint(
    "weton",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/weton-static",
)


@weton_bp.route("/weton")
def weton_index():
    return render_template("weton/index.html", features=HUB_FEATURES)


@weton_bp.route("/weton/birth")
def weton_birth_page():
    return render_template(
        "weton/lair.html",
        cities=CITY_OPTIONS,
        glossary=GLOSSARY,
        first_date=SUPPORTED_FIRST.isoformat(),
        last_date=SUPPORTED_LAST.isoformat(),
    )


@weton_bp.route("/api/weton/birth", methods=["POST"])
def weton_birth_api():
    try:
        return jsonify(build_birth_reading(request.get_json(silent=True)))
    except WetonError as error:
        return jsonify({"error": error.message}), error.status


@weton_bp.route("/weton/compatibility")
def weton_compatibility_page():
    return render_template(
        "weton/cocog.html",
        cities=CITY_OPTIONS,
        glossary=GLOSSARY,
        lenses=WETON_LENS,
        default_lens=DEFAULT_LENS,
        first_date=SUPPORTED_FIRST.isoformat(),
        last_date=SUPPORTED_LAST.isoformat(),
    )


@weton_bp.route("/api/weton/compatibility", methods=["POST"])
def weton_compatibility_api():
    try:
        return jsonify(build_match_reading(request.get_json(silent=True)))
    except WetonError as error:
        return jsonify({"error": error.message}), error.status


@weton_bp.route("/weton/calendar")
def weton_calendar_page():
    return render_template(
        "weton/tanggalan.html",
        cities=CITY_OPTIONS,
        glossary=GLOSSARY,
        initial=build_calendar({}),
        first_date=SUPPORTED_FIRST.isoformat(),
        last_date=SUPPORTED_LAST.isoformat(),
    )


@weton_bp.route("/api/weton/calendar", methods=["POST"])
def weton_calendar_api():
    try:
        return jsonify(build_calendar(request.get_json(silent=True)))
    except WetonError as error:
        return jsonify({"error": error.message}), error.status


@weton_bp.route("/weton/roasting")
def weton_roasting_page():
    return render_template(
        "weton/poyokan.html",
        cities=CITY_OPTIONS,
        glossary=GLOSSARY,
        first_date=SUPPORTED_FIRST.isoformat(),
        last_date=SUPPORTED_LAST.isoformat(),
    )


@weton_bp.route("/api/weton/roasting", methods=["POST"])
def weton_roasting_api():
    try:
        return jsonify(build_roasting(request.get_json(silent=True)))
    except WetonError as error:
        return jsonify({"error": error.message}), error.status
