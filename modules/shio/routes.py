from flask import Blueprint, render_template, jsonify, request
from .data import (
    get_all_daily_fortunes,
    get_shio_guardian,
    get_shio_compatibility,
    get_shio_yearly,
    get_current_imlek_year,
    get_shio_roasting,
    get_fortune_cookie,
    get_shio_destiny,
    DESTINY_CITIES,
    DESTINY_SCHOOL,
)

shio_bp = Blueprint(
    "shio",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/shio-static",
)

def read_payload():
    data = request.get_json(silent=True)
    return data if isinstance(data, dict) else {}


def read_text(data, field):
    value = data.get(field)
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


@shio_bp.route("/shio")
def shio_index():
    return render_template("shio/index.html")

@shio_bp.route("/shio/destiny")
def shio_destiny_page():
    return render_template(
        "shio/destiny.html", cities=DESTINY_CITIES, school=DESTINY_SCHOOL
    )

@shio_bp.route("/shio/guardian")
def guardian_spiritual():
    return render_template("shio/guardian.html")

@shio_bp.route("/shio/compatibility")
def shio_compatibility():
    return render_template("shio/compatibility.html")

@shio_bp.route("/shio/yearly")
def shio_yearly_page():
    return render_template(
        "shio/yearly.html", current_year=get_current_imlek_year()
    )

@shio_bp.route("/shio/roasting")
def shio_roasting_page():
    return render_template("shio/roasting.html")

@shio_bp.route("/shio/fortune-cookie")
def shio_fortune_cookie_page():
    return render_template("shio/fortune-cookie.html")

@shio_bp.route("/api/shio/daily", methods=["GET"])
def get_shio_daily():
    client_date_str = request.args.get("date")
    result = get_all_daily_fortunes(client_date_str)
    return jsonify(result)

@shio_bp.route("/api/shio/guardian", methods=["POST"])
def get_shio_guardian_endpoint():
    data = read_payload()
    shio_key = read_text(data, "shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_shio_guardian(shio_key)
    return jsonify(result)

@shio_bp.route("/api/shio/compatibility", methods=["POST"])
def get_shio_compatibility_endpoint():
    data = read_payload()
    shio1 = read_text(data, "shio1")
    shio2 = read_text(data, "shio2")
    if not shio1 or not shio2:
        return jsonify({"error": "Missing shio1 or shio2"}), 400
    result = get_shio_compatibility(
        shio1, shio2, read_text(data, "tanggal1"), read_text(data, "tanggal2")
    )
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)

@shio_bp.route("/api/shio/yearly", methods=["POST"])
def get_shio_yearly_endpoint():
    data = read_payload()
    shio_key = read_text(data, "shio")
    year = data.get("year")
    if not shio_key or year is None:
        return jsonify({"error": "Missing shio or year"}), 400
    result = get_shio_yearly(shio_key, year)
    return jsonify(result)

@shio_bp.route("/api/shio/roasting", methods=["POST"])
def get_shio_roasting_endpoint():
    data = read_payload()
    shio_key = read_text(data, "shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_shio_roasting(shio_key)
    return jsonify(result)

@shio_bp.route("/api/shio/fortune-cookie", methods=["POST"])
def get_fortune_cookie_endpoint():
    data = read_payload()
    shio_key = read_text(data, "shio")
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
    result = get_fortune_cookie(shio_key, read_text(data, "date"))
    return jsonify(result)

@shio_bp.route("/api/shio/destiny", methods=["POST"])
def get_shio_destiny_endpoint():
    data = read_payload()
    result = get_shio_destiny(
        read_text(data, "tanggal"),
        data.get("jam"),
        data.get("menit"),
        read_text(data, "kota"),
        read_text(data, "gender"),
    )
    if "error" in result:
        return jsonify(result), 400
    return jsonify(result)
