from flask import Blueprint, render_template, jsonify, request
from .data import SHIO_DATA, generate_shio_fortune, get_secret_animal, calculate_yearly_fortune, calculate_compatibility, get_all_daily_fortunes, get_shio_guardian

shio_bp = Blueprint('shio', __name__, template_folder='templates', static_folder='static', static_url_path='/shio-static')

@shio_bp.route('/shio')
def shio_index():
    return render_template('shio/index.html')

@shio_bp.route('/shio/guardian')
def guardian_spiritual():
    return render_template('shio/guardian.html')



@shio_bp.route('/api/shio/fortune', methods=['POST'])
def get_shio_fortune():
    data = request.get_json()
    shio_key = data.get('shio')
    element_key = data.get('element')
    time_str = data.get('time')
    
    result = generate_shio_fortune(shio_key, element_key)
    
    if time_str:
        secret_shio = get_secret_animal(time_str)
        if secret_shio:
            result['secret_animal'] = SHIO_DATA.get(secret_shio)["name"]
            
    return jsonify(result)

@shio_bp.route('/api/shio/yearly', methods=['POST'])
def get_shio_yearly():
    data = request.get_json()
    shio_key = data.get('shio')
    year = data.get('year')
    
    if not shio_key or not year:
        return jsonify({"error": "Missing shio or year"}), 400
        
    result = calculate_yearly_fortune(shio_key, year)
    return jsonify(result)

@shio_bp.route('/api/shio/compatibility', methods=['POST'])
def get_shio_compatibility():
    data = request.get_json()
    s1 = data.get('shio1')
    s2 = data.get('shio2')
    e1 = data.get('element1')
    e2 = data.get('element2')
    t1 = data.get('time1')
    t2 = data.get('time2')
    
    if not all([s1, s2, e1, e2]):
        return jsonify({"error": "Missing parameters"}), 400
        
    result = calculate_compatibility(s1, s2, e1, e2, t1, t2)
    return jsonify(result)

@shio_bp.route('/api/shio/daily', methods=['GET'])
def get_shio_daily():
    client_date_str = request.args.get('date')
    result = get_all_daily_fortunes(client_date_str)
    return jsonify(result)

@shio_bp.route('/api/shio/guardian', methods=['POST'])
def get_shio_guardian_endpoint():
    data = request.get_json()
    shio_key = data.get('shio')
    
    if not shio_key:
        return jsonify({"error": "Missing shio"}), 400
        
    result = get_shio_guardian(shio_key)
    return jsonify(result)
