from flask import Blueprint, render_template, jsonify, request
from .data import get_weton_info

weton_bp = Blueprint(
    "weton",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/weton-static",
)

@weton_bp.route("/weton")
def weton_index():
    # Placeholder for the Weton home page
    return "Weton Home - Segera Hadir"

@weton_bp.route("/api/weton/calculate", methods=["GET"])
def calculate_weton():
    # Placeholder API for weton
    hari = request.args.get("hari", "Senin")
    pasaran = request.args.get("pasaran", "Legi")
    result = get_weton_info(hari, pasaran)
    return jsonify(result)
