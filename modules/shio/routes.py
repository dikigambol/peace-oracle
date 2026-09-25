from flask import Blueprint, render_template, jsonify, request, current_app, abort
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
    QuizError,
    QuizUnavailable,
    build_mysql_store,
)
from .bank import RELATION_LENS, QUIZ_MODE_BANK, GUESS_FLAVOR_BANK
from . import data as shio_data

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
    result = get_shio_compatibility(
        read_text(data, "shio1"),
        read_text(data, "shio2"),
        read_text(data, "tanggal1"),
        read_text(data, "tanggal2"),
        read_text(data, "lens") or "asmara",
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
    result = get_shio_roasting(
        read_text(data, "shio"),
        read_text(data, "pasangan"),
        read_text(data, "tanggal"),
        read_text(data, "gender"),
    )
    if "error" in result:
        return jsonify(result), 400
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


QUIZ_OFFLINE_MESSAGE = (
    "Quiz lagi offline karena basis datanya belum bisa dihubungi. "
    "Fitur shio lain tetap jalan normal, coba quiz lagi nanti."
)


def get_quiz_store():
    store = current_app.config.get("SHIO_QUIZ_STORE")
    if store is None:
        store = build_mysql_store()
        current_app.config["SHIO_QUIZ_STORE"] = store
    return store


def get_quiz_device():
    from core.device import get_device_id

    return get_device_id()


def read_quiz_token():
    return request.headers.get("X-Quiz-Token", "").strip()


def run_quiz(action, success_status=200):
    try:
        return jsonify(action()), success_status
    except QuizUnavailable:
        return jsonify({"error": QUIZ_OFFLINE_MESSAGE}), 503
    except QuizError as error:
        return jsonify({"error": error.message}), error.status


def require_room_code(raw_code):
    code = shio_data.normalise_room_code(raw_code)
    if code is None:
        raise QuizError("Kode room tidak valid.", 404)
    return code


@shio_bp.route("/shio/quiz")
def shio_quiz_page():
    return render_template(
        "shio/quiz.html",
        modes=QUIZ_MODE_BANK,
        lenses=RELATION_LENS,
        flavors=GUESS_FLAVOR_BANK,
        limits=shio_data.MODE_LIMITS,
    )


@shio_bp.route("/shio/quiz/<room_code>")
def shio_quiz_room_page(room_code):
    code = shio_data.normalise_room_code(room_code)
    if code is None:
        abort(404)
    return render_template("shio/quiz-room.html", room_code=code)


@shio_bp.route("/api/shio/quiz/rooms", methods=["POST"])
def shio_quiz_create():
    data = read_payload()
    return run_quiz(
        lambda: shio_data.create_room(get_quiz_store(), data, get_quiz_device()), 201
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>", methods=["GET"])
def shio_quiz_view(room_code):
    return run_quiz(
        lambda: shio_data.build_room_view(
            get_quiz_store(), require_room_code(room_code), read_quiz_token()
        )
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>/join", methods=["POST"])
def shio_quiz_join(room_code):
    data = read_payload()
    return run_quiz(
        lambda: shio_data.join_room(get_quiz_store(), require_room_code(room_code), data), 201
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>/answers", methods=["POST"])
def shio_quiz_answers(room_code):
    data = read_payload()
    return run_quiz(
        lambda: shio_data.submit_answers(
            get_quiz_store(), require_room_code(room_code), read_quiz_token(),
            data.get("answers"),
        )
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>/start", methods=["POST"])
def shio_quiz_start(room_code):
    return run_quiz(
        lambda: shio_data.start_room(
            get_quiz_store(), require_room_code(room_code), read_quiz_token()
        )
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>/guess", methods=["POST"])
def shio_quiz_guess(room_code):
    data = read_payload()
    return run_quiz(
        lambda: shio_data.submit_guess(
            get_quiz_store(), require_room_code(room_code), read_quiz_token(),
            data.get("round"), data.get("slot"),
        )
    )


@shio_bp.route("/api/shio/quiz/rooms/<room_code>/finish", methods=["POST"])
def shio_quiz_finish(room_code):
    return run_quiz(
        lambda: shio_data.finish_room(
            get_quiz_store(), require_room_code(room_code), read_quiz_token()
        )
    )
