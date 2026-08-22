from flask import Blueprint, render_template, jsonify, request
from .data import *

zodiak_bp = Blueprint("zodiak", __name__, template_folder="templates", static_folder="static", static_url_path="/zodiak-static")

# ROUTES
@zodiak_bp.route('/zodiak')
def home():
    return render_template('zodiak/index.html')

@zodiak_bp.route('/zodiak/kecocokan')
def compatibility_page():
    return render_template('zodiak/kecocokan.html')

@zodiak_bp.route('/zodiak/general')
@zodiak_bp.route('/zodiak/karakter')
def general_page():
    return render_template('zodiak/general.html')

@zodiak_bp.route('/zodiak/roasting')
def roasting_page():
    return render_template('zodiak/roasting.html')

@zodiak_bp.route('/api/zodiak/roast', methods=['GET', 'POST'])
def get_roasting_data():
    sign_key = None
    refresh = request.args.get('refresh') == '1' or request.args.get('roll') == '1'

    if request.method == 'POST':
        data = request.get_json() or {}
        sign_key = data.get('sign')
        birthdate = data.get('birthdate')
        if not refresh:
            refresh = data.get('refresh') == 1 or data.get('roll') == 1
        if birthdate:
            try:
                parts = birthdate.split('-')
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
    else:
        sign_key = request.args.get('sign')
        birthdate = request.args.get('birthdate')
        if birthdate:
            try:
                parts = birthdate.split('-')
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
        elif sign_key:
            sign_key = sign_key.lower()

    if not sign_key or sign_key not in ZODIAC_DATA:
        sign_key = 'aries'

    z = ZODIAC_DATA[sign_key]
    roast_info = get_ai_roast(sign_key, refresh=refresh)

    sign_b = None
    if request.method == 'POST':
        data = request.get_json() or {}
        sign_b = data.get('sign_b')
    else:
        sign_b = request.args.get('sign_b')

    relationship_roast = None
    if sign_b and sign_b.lower() in ZODIAC_DATA:
        relationship_roast = get_ai_relationship_roast(sign_key, sign_b.lower(), refresh=refresh)

    return jsonify({
        "sign_key": sign_key,
        "name": z["name"],
        "element": z["element"],
        "date_range": z["date_range"],
        "roast": roast_info,
        "relationship_roast": relationship_roast
    })

@zodiak_bp.route('/api/zodiak/zodiac/<sign>')
def get_zodiac(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z = ZODIAC_DATA[sign_key]

    cosmic = get_cosmic_context()
    dynamic_ratings = generate_dynamic_ratings(
        z["base_ratings"], cosmic, z["ruler_planet"], sign_key
    )
    genz_readings = get_daily_horoscope(sign_key, cosmic)
    youtube_track = genz_readings.get("youtube_track") or get_daily_youtube_track(sign_key, cosmic)

    ruler_planet = z["ruler_planet"]
    planet_info = cosmic["planet_status"].get(ruler_planet, {})
    ruler_status = planet_info.get("label", "✅ Langsung")

    return jsonify({
        "name": z["name"],
        "date_range": z["date_range"],
        "element": z["element"],
        "ruler": z["ruler"],
        "strengths": z["strengths"],
        "weaknesses": z["weaknesses"],
        "lucky_number": z["lucky_number"],
        "lucky_color": z["lucky_color"],
        "compatible_signs": z["compatible_signs"],
        "summary": genz_readings["summary"],
        "genz_readings": genz_readings,
        "youtube_track": youtube_track,
        "ratings": dynamic_ratings,
        "cosmic": {
            "date": cosmic["date"],
            "moon_phase": cosmic["moon_phase"],
            "moon_emoji": cosmic["moon_emoji"],
            "moon_illumination": cosmic["moon_illumination"],
            "ruler_status": ruler_status,
            "ruler_is_retrograde": planet_info.get("is_retrograde", False),
            "weather": cosmic["weather"]
        }
    })

@zodiak_bp.route('/api/zodiak/general/<sign>')
@zodiak_bp.route('/api/zodiak/karakter/<sign>')
def get_general_details(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z = ZODIAC_DATA[sign_key]
    char = GENERAL_CHARACTERISTICS.get(sign_key, GENERAL_CHARACTERISTICS["aries"])

    return jsonify({
        "name": z["name"],
        "date_range": z["date_range"],
        "element": z["element"],
        "ruler": z["ruler"],
        "physical_traits": char["physical_traits"],
        "personality": char["personality"],
        "habits": char["habits"],
        "animal_soulmate": char["animal_soulmate"],
        "cosmic_pantry": char["cosmic_pantry"],
        "astro_decor": char["astro_decor"],
        "fun_fact": char["fun_fact"]
    })

@zodiak_bp.route('/api/zodiak/compatibility/<sign_one>/<sign_two>')
def get_compatibility(sign_one, sign_two):
    s1_key = sign_one.lower()
    s2_key = sign_two.lower()

    if s1_key not in ZODIAC_DATA or s2_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z1 = ZODIAC_DATA[s1_key]
    z2 = ZODIAC_DATA[s2_key]

    elem_one = z1["element"]
    elem_two = z2["element"]
    base_metrics = ELEMENT_COMPATIBILITY[elem_one][elem_two].copy()

    if s1_key == s2_key:
        base_metrics.update({"score": 80, "love": 82, "comm": 78, "trust": 85, "future": 75})
    elif (
        (s1_key == 'scorpio' and s2_key == 'cancer') or (s1_key == 'cancer' and s2_key == 'scorpio') or
        (s1_key == 'leo' and s2_key == 'aries') or (s1_key == 'aries' and s2_key == 'leo') or
        (s1_key == 'gemini' and s2_key == 'libra') or (s1_key == 'libra' and s2_key == 'gemini')
    ):
        base_metrics.update({"score": 98, "love": 99, "comm": 97, "trust": 98, "future": 98})

    base_score = base_metrics["score"]

    # 1. MODE PASANGAN (Asmara / Romantis)
    love_score = min(99, max(45, int(base_score * 1.02)))
    if love_score >= 85:
        love_status = "Sangat Harmonis (Kosmik Selaras) ✨"
        love_summary = f"Kombinasi asmara antara {z1['name']} ({elem_one}) dan {z2['name']} ({elem_two}) membentuk perpaduan cinta yang luar biasa kuat dan penuh daya tarik emosional."
        love_strengths = ["Chemistry cinta meletup-letup dan romantis", "Saling memahami perasaan tanpa banyak bicara", "Dukungan emosional yang hangat dan menenangkan"]
        love_challenges = ["Kecenderungan menyembunyikan masalah emosional kecil", "Menjaga ritme romansa agar tidak menjadi rutinitas"]
    elif love_score >= 70:
        love_status = "Cinta Kuat & Komitmen Tinggi 💖"
        love_summary = f"Hubungan {z1['name']} dan {z2['name']} memiliki fondasi kesetiaan yang stabil. Perbedaan gaya mencintai justru saling melengkapi kelemahan masing-masing."
        love_strengths = ["Saling melengkapi bahasa cinta (love language)", "Kesetiaan tinggi dan komitmen jangka panjang", "Rasa aman saat bersama"]
        love_challenges = ["Perbedaan cara merespon konflik emosional", "Butuh waktu untuk menyelaraskan ekspektasi"]
    else:
        love_status = "Tantangan Kompromi Asmara ⚡"
        love_summary = f"Perpaduan elemen {elem_one} dan {elem_two} membutuhkan kesabaran ekstra dalam asmara. Butuh komunikasi terbuka untuk menyelaraskan keinginan ego."
        love_strengths = ["Memberikan pelajaran kedewasaan emosional", "Daya tarik perbedaan karakter yang kuat", "Menumbuhkan rasa toleransi tinggi"]
        love_challenges = ["Kecerobohan emosi saat dipicu rasa cemburu", "Perbedaan ritme mengekspresikan kasih sayang"]

    # 2. MODE SAHABAT (Pertemanan / Bestie)
    friend_score = min(99, max(40, int(base_score * 0.98 + (10 if elem_one in ['Udara', 'Api'] and elem_two in ['Udara', 'Api'] else 0))))
    if friend_score >= 85:
        friend_status = "Bestie Sejati (Frekuensi Selaras) 🤝"
        friend_summary = f"Sebagai sahabat, {z1['name']} dan {z2['name']} adalah kombinasi duo paling seru! Keduanya bisa ngobrolin apa saja dari spill the tea hingga topik filsafat tanpa takut di-judge."
        friend_strengths = ["Frekuensi humor dan nyambung obrolannya 100%", "Tempat curhat aman tanpa rasa canggung", "Selalu siap saling bantu di masa sulit"]
        friend_challenges = ["Sering lupa waktu kalau udah ketemu dan ngobrol", "Keduanya sama-sama suka ceplas-ceplos"]
    elif friend_score >= 70:
        friend_status = "Teman Asyik & Suportif 🥳"
        friend_summary = f"Pertemanan antara {z1['name']} dan {z2['name']} sangat menyenangkan untuk diajak nongkrong, berpetualang, atau nyobain hal-hal baru bersama."
        friend_strengths = ["Asyik diajak jalan-jalan atau nyobain kuliner baru", "Saling mendukung impian satu sama lain", "Bisa menjaga rahasia dengan baik"]
        friend_challenges = ["Kadang butuh waktu sendiri jika mood sedang tidak bagus", "Jarang menyampaikan rasa tidak suka secara langsung"]
    else:
        friend_status = "Teman Kasual (Perlu Saling Menghormati) ☕"
        friend_summary = f"Hubungan pertemanan ini paling pas berada di tingkat kasual. Menghormati batasan dan ruang pribadi adalah kunci agar hubungan pertemanan tetap awet."
        friend_strengths = ["Membawa sudut pandang baru yang tidak terpikirkan", "Menguji batas kepekaan sosial", "Menyenangkan saat mengerjakan proyek hobi tertentu"]
        friend_challenges = ["Gaya bercanda kadang tidak sengaja menyinggung perasaan", "Perbedaan selera aktivitas waktu luang"]

    # 3. MODE REKAN KERJA (Karir / Profesional)
    work_score = min(99, max(40, int(base_score * 0.95 + (12 if elem_one in ['Tanah', 'Api'] and elem_two in ['Tanah', 'Api'] else 5))))
    if work_score >= 85:
        work_status = "Dream Team Profesional (Sinergi Tinggi) 💼"
        work_summary = f"Di tempat kerja, {z1['name']} dan {z2['name']} adalah kombinasi Dream Team! Satu pihak mahir memikirkan ide & strategi, sementara pihak lainnya tangguh dalam eksekusi target."
        work_strengths = ["Sinergi eksekusi proyek sangat cepat dan efisien", "Pembagian tugas yang sangat alami dan saling melengkapi", "Fokus tinggi pada pencapaian target kerja"]
        work_challenges = ["Keduanya bisa terlalu kompetitif jika tidak menetapkan tujuan bersama", "Cenderung lupa istirahat karena keasyikan kerja"]
    elif work_score >= 70:
        work_status = "Rekan Kerja Efisien & Produktif 📈"
        work_summary = f"Kerja sama profesional antara {z1['name']} dan {z2['name']} berjalan lancar dan terorganisir. Mereka dapat mencapai deadline dengan hasil memuaskan."
        work_strengths = ["Komunikasi profesional yang jelas dan terarah", "Saling menghormati wewenang dan job description", "Dapat diandalkan dalam pemecahan masalah teknis"]
        work_challenges = ["Perlu menyelaraskan ritme kerja saat tekanan deadline tinggi", "Kadang terlalu kaku dalam mengambil keputusan kompromi"]
    else:
        work_status = "Perlu Pembagian Tugas Jelas 🛠️"
        work_summary = f"Dalam dunia kerja, {z1['name']} dan {z2['name']} membutuhkan struktur dan SOP yang sangat transparan agar tidak terjadi tumpang tindih wewenang."
        work_strengths = ["Saling menguji kelemahan konsep bisnis sebelum eksekusi", "Mendorong kehati-hatian dalam mengambil risiko", "Membuat analisis kerja menjadi lebih tajam"]
        work_challenges = ["Potensi benturan ego saat mempertahankan ide masing-masing", "Perbedaan gaya manajemen waktu"]

    modes_data = {
        "romance": {
            "label": "Pasangan (Asmara)",
            "icon": "fa-heart",
            "score": love_score,
            "status": love_status,
            "summary": love_summary,
            "strengths": love_strengths,
            "challenges": love_challenges,
            "metrics": {"love": base_metrics["love"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": base_metrics["future"]}
        },
        "friendship": {
            "label": "Sahabat (Bestie)",
            "icon": "fa-user-group",
            "score": friend_score,
            "status": friend_status,
            "summary": friend_summary,
            "strengths": friend_strengths,
            "challenges": friend_challenges,
            "metrics": {"love": base_metrics["comm"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": int((friend_score + base_metrics["comm"]) / 2)}
        },
        "work": {
            "label": "Rekan Kerja",
            "icon": "fa-briefcase",
            "score": work_score,
            "status": work_status,
            "summary": work_summary,
            "strengths": work_strengths,
            "challenges": work_challenges,
            "metrics": {"love": base_metrics["comm"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": int((work_score + base_metrics["trust"]) / 2)}
        }
    }

    modes_data = get_ai_compatibility_modes(s1_key, s2_key, z1["name"], elem_one, z2["name"], elem_two, modes_data)

    return jsonify({
        "sign_one": z1["name"], "sign_two": z2["name"],
        "element_one": elem_one, "element_two": elem_two,
        "modes": modes_data
    })

if __name__ == '__main__':
    pass # app.run(debug=True)
