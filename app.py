import os
import secrets
from dotenv import load_dotenv

load_dotenv()
from flask import Flask, render_template
from modules.zodiak.routes import zodiak_bp
from modules.shio.routes import shio_bp
from modules.weton.routes import weton_bp
from modules.tarot.routes import tarot_bp

app = Flask(__name__, template_folder="core/templates", static_folder="core/static")

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', secrets.token_hex(32))

app.register_blueprint(zodiak_bp)
app.register_blueprint(shio_bp)
app.register_blueprint(weton_bp)
app.register_blueprint(tarot_bp)

@app.route("/")
def home():
    return render_template("home.html")

@app.route('/.well-known/<path:filename>')
def well_known_trap(filename):
    message = (
        "Greetings, cosmic crawler.\n"
        "The Peace Oracle has foreseen your arrival.\n"
        "Your data scraping attempts radiate a deeply chaotic aura.\n"
        "Beware: scraping too deep into this dimension may inflict "
        "7 years of bad Feng Shui upon your servers.\n\n"
        "Return to your base in peace ✌️"
    )
    return message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

@app.route('/robots.txt')
def robots_txt():
    message = (
        "User-agent: *\n"
        "Disallow: /bad-karma\n"
        "Disallow: /negative-energy\n\n"
        "# Hello bot! Our third eye is watching you.\n"
        "# Feel free to crawl, but do not disrupt our cosmic order."
    )
    return message, 200, {'Content-Type': 'text/plain; charset=utf-8'}

if __name__ == "__main__":
    raw_debug = os.getenv("FLASK_DEBUG", "false").strip().lower()
    is_debug = raw_debug in ("true", "1", "t", "yes")

    if os.getenv("FLASK_ENV", "").lower() == "production":
        is_debug = False

    default_host = "127.0.0.1" if is_debug else "0.0.0.0"
    host = os.getenv("FLASK_HOST", default_host)
    port = int(os.getenv("FLASK_PORT", 5000))

    app.run(host=host, port=port, debug=is_debug)
