import datetime

from flask import Blueprint, jsonify, render_template, request

from .bank import DEFAULT_HAJAT, DEFAULT_LENS, GLOSSARY, HAJAT, HUB_FEATURES, WETON_LENS
from .data import (
    CITY_OPTIONS,
    SUPPORTED_FIRST,
    SUPPORTED_LAST,
    WetonError,
    build_birth_reading,
    build_calendar,
    build_dina_reading,
    build_match_reading,
    build_roasting,
    today_wib,
)

weton_bp = Blueprint(
    "weton",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/weton-static",
)


@weton_bp.context_processor
def inject_features():
    return {"features": HUB_FEATURES}


def render_page(template, **extra):
    return render_template(
        template,
        cities=CITY_OPTIONS,
        first_date=SUPPORTED_FIRST.isoformat(),
        last_date=SUPPORTED_LAST.isoformat(),
        **extra,
    )


def api_response(builder):
    try:
        return jsonify(builder(request.get_json(silent=True)))
    except WetonError as error:
        return jsonify({"error": error.message}), error.status


@weton_bp.route("/weton")
def weton_index():
    return render_template("weton/index.html")


@weton_bp.route("/weton/birth")
def weton_birth_page():
    return render_page("weton/lair.html", glossary=GLOSSARY)


@weton_bp.route("/api/weton/birth", methods=["POST"])
def weton_birth_api():
    return api_response(build_birth_reading)


@weton_bp.route("/weton/compatibility")
def weton_compatibility_page():
    return render_page("weton/cocog.html", lenses=WETON_LENS, default_lens=DEFAULT_LENS)


@weton_bp.route("/api/weton/compatibility", methods=["POST"])
def weton_compatibility_api():
    return api_response(build_match_reading)


@weton_bp.route("/weton/calendar")
def weton_calendar_page():
    try:
        initial = build_calendar({"tanggal": request.args.get("tanggal")})
    except WetonError:
        initial = build_calendar({})
    return render_page("weton/tanggalan.html", initial=initial)


@weton_bp.route("/api/weton/calendar", methods=["POST"])
def weton_calendar_api():
    return api_response(build_calendar)


@weton_bp.route("/weton/roasting")
def weton_roasting_page():
    return render_page("weton/poyokan.html")


@weton_bp.route("/api/weton/roasting", methods=["POST"])
def weton_roasting_api():
    return api_response(build_roasting)


@weton_bp.route("/weton/good-day")
def weton_good_day_page():
    today = today_wib()
    return render_page(
        "weton/dinabecik.html",
        hajat=HAJAT,
        default_hajat=DEFAULT_HAJAT,
        default_start=today.isoformat(),
        default_end=min(today + datetime.timedelta(days=30), SUPPORTED_LAST).isoformat(),
    )


@weton_bp.route("/api/weton/good-day", methods=["POST"])
def weton_good_day_api():
    return api_response(build_dina_reading)
