import os
import secrets
import sys

MINIMUM_PYTHON = (3, 12)

if sys.version_info < MINIMUM_PYTHON:
    raise RuntimeError(
        "Peace Oracle membutuhkan Python "
        f"{MINIMUM_PYTHON[0]}.{MINIMUM_PYTHON[1]} atau lebih baru, "
        f"terpasang {sys.version.split()[0]}."
    )

from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template
from core.core import init_app
from modules.zodiak.routes import zodiak_bp
from modules.shio.routes import shio_bp
from modules.weton.routes import weton_bp
from modules.tarot.routes import tarot_bp

app = Flask(__name__, template_folder="core/templates", static_folder="core/static")
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

app.register_blueprint(zodiak_bp)
app.register_blueprint(shio_bp)
app.register_blueprint(weton_bp)
app.register_blueprint(tarot_bp)
init_app(app)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/.well-known/<path:filename>')
def well_known_trap(filename):
    message = (
        "404 - Not written in the stars.\n\n"
        "The Peace Oracle checked the zodiac, the twelve earthly branches,\n"
        "the Javanese calendar, and a freshly shuffled tarot deck.\n"
        "None of them know this file.\n\n"
        "Scrape any deeper and you may draw The Tower, land on a Rebo Wekasan,\n"
        "and catch seven years of bad Feng Shui on your servers.\n\n"
        "Return to your base in peace ✌️"
    )
    return message, 404, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/robots.txt')
def robots_txt():
    message = (
        "User-agent: *\n"
        "Disallow: /api/\n"
        "Disallow: /bad-karma\n"
        "Disallow: /negative-energy\n\n"
        "# Hello, bot. All four of our oracles can see you.\n"
        "# Read the pages all you like, but leave /api/ to the humans.\n"
        "# The stars have been consulted. Crawl in peace."
    )
    return message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route("/api/db-debug")
def db_debug():
    import time
    from core.core import HAS_FIREBASE, get_firestore_client, get_service_account_dict
    has_env = bool(os.environ.get("FIREBASE_SERVICE_ACCOUNT_KEY"))
    has_file = os.path.isfile("serviceAccountKey.json") or os.path.isfile(os.path.join(os.path.dirname(__file__), "serviceAccountKey.json"))
    diag = {
        "provider": "firebase_firestore",
        "has_firebase_package": HAS_FIREBASE,
        "has_env_key": has_env,
        "has_local_file": has_file,
    }
    sa_dict = get_service_account_dict()
    if not sa_dict:
        diag["status"] = "error"
        diag["message"] = "Kredensial Firebase tidak ditemukan. Tambahkan FIREBASE_SERVICE_ACCOUNT_KEY di Environment Variables Vercel."
        return diag, 500
    diag["project_id"] = sa_dict.get("project_id")
    diag["client_email"] = sa_dict.get("client_email")
    try:
        db = get_firestore_client()
        if not db:
            diag["status"] = "error"
            diag["message"] = "Gagal inisialisasi Firestore client."
            return diag, 500
        test_ref = db.collection("_healthcheck").document("ping")
        test_ref.set({"timestamp": time.time(), "status": "ok"})
        doc = test_ref.get()
        diag["status"] = "success"
        diag["ping_result"] = doc.to_dict()
        return diag, 200
    except Exception as e:
        diag["status"] = "error"
        diag["error_type"] = type(e).__name__
        diag["error_message"] = str(e)
        return diag, 500

if __name__ == "__main__":
    raw_debug = os.getenv("FLASK_DEBUG", "false").strip().lower()
    is_debug = raw_debug in ("true", "1", "t", "yes")

    if os.getenv("FLASK_ENV", "").lower() == "production":
        is_debug = False

    default_host = "127.0.0.1" if is_debug else "0.0.0.0"
    host = os.getenv("FLASK_HOST", default_host)
    port = int(os.getenv("FLASK_PORT", 5000))

    app.run(host=host, port=port, debug=is_debug)
