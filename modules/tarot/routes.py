from flask import Blueprint, render_template, jsonify
from .data import get_random_card

tarot_bp = Blueprint(
    "tarot",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/tarot-static",
)

@tarot_bp.route("/tarot")
def tarot_index():
    # Placeholder for the Tarot home page
    return "Tarot Home - Segera Hadir"

@tarot_bp.route("/api/tarot/draw", methods=["GET"])
def draw_card():
    # Placeholder API to draw a random card
    card = get_random_card()
    return jsonify(card)
