from flask import Blueprint, render_template, jsonify, request
from .data import (
    SHIO_DATA,
    get_all_daily_fortunes,
    get_shio_guardian,
    get_shio_profile,
    get_shio_compatibility,
    get_shio_fortune,
)

shio_bp = Blueprint(
    "shio",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/shio-static",
)


@shio_bp.route("/shio")
def shio_index():
    return render_template("shio/index.html")


@shio_bp.route("/shio/guardian")
def guardian_spiritual():
    return render_template("shio/guardian.html")


@shio_bp.route("/shio/profile")
def shio_profile():
    return render_template("shio/profile.html")


@shio_bp.route("/shio/compatibility")
def shio_compatibility():
    return render_template("shio/compatibility.html")


@shio_bp.route("/api/shio/daily", methods=["GET"])
def get_shio_daily():
    client_date_str = request.args.get("date")
    result = get_all_daily_fortunes(client_date_str)
    return jsonify(result)


@shio_bp.route("/api/shio/guardian", methods=["POST"])
def get_shio_guardian_endpoint():
    data = request.get_json()
    shio_key = data.get("shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_shio_guardian(shio_key)
    return jsonify(result)


@shio_bp.route("/api/shio/profile", methods=["POST"])
def get_shio_profile_endpoint():
    data = request.get_json()
    shio_key = data.get("shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_shio_profile(shio_key)
    return jsonify(result)


@shio_bp.route("/api/shio/compatibility", methods=["POST"])
def get_shio_compatibility_endpoint():
    data = request.get_json()
    shio1 = data.get("shio1")
    shio2 = data.get("shio2")
    if not shio1 or not shio2:
        return jsonify({"error": "Missing shio1 or shio2"}), 400
    result = get_shio_compatibility(shio1, shio2)
    return jsonify(result)


@shio_bp.route("/api/shio/fortune", methods=["POST"])
def get_shio_fortune_endpoint():
    data = request.get_json()
    shio_key = data.get("shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_shio_fortune(shio_key)
    return jsonify(result)
