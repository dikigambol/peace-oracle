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
    return render_page("weton/tanggalan.html", initial=build_calendar({}))


@weton_bp.route("/api/weton/calendar", methods=["POST"])
def weton_calendar_api():
    return api_response(build_calendar)


@weton_bp.route("/weton/roasting")
def weton_roasting_page():
    return render_page("weton/poyokan.html")


@weton_bp.route("/api/weton/roasting", methods=["POST"])
def weton_roasting_api():
    return api_response(build_roasting)
