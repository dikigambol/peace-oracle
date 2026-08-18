from flask import Blueprint, render_template, jsonify, request
from .data import SHIO_DATA, ELEMENT_DATA, generate_shio_fortune

shio_bp = Blueprint('shio', __name__, template_folder='templates', static_folder='static', static_url_path='/shio-static')

@shio_bp.route('/shio')
def shio_index():
    return render_template('shio/index.html')

@shio_bp.route('/api/shio/fortune', methods=['POST'])
def get_shio_fortune():
    data = request.get_json()
    shio_key = data.get('shio')
    element_key = data.get('element')
    result = generate_shio_fortune(shio_key, element_key)
    return jsonify(result)
