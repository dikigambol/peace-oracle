from flask import Blueprint, render_template, jsonify, request
from .data import *

zodiak_bp = Blueprint(
    "zodiak",
    __name__,
    template_folder="templates",
    static_folder="static",
    static_url_path="/zodiak-static",
)


@zodiak_bp.route("/zodiak")
def home():
    return render_template("zodiak/index.html")


@zodiak_bp.route("/zodiak/kecocokan")
def compatibility_page():
    return render_template("zodiak/kecocokan.html")


@zodiak_bp.route("/zodiak/general")
@zodiak_bp.route("/zodiak/karakter")
def general_page():
    return render_template("zodiak/general.html")


@zodiak_bp.route("/zodiak/roasting")
def roasting_page():
    return render_template("zodiak/roasting.html")


@zodiak_bp.route("/api/zodiak/roast", methods=["GET", "POST"])
def get_roasting_data():
    sign_key = None
    refresh = request.args.get("refresh") == "1" or request.args.get("roll") == "1"
    if request.method == "POST":
        data = request.get_json() or {}
        sign_key = data.get("sign")
        birthdate = data.get("birthdate")
        if not refresh:
            refresh = data.get("refresh") == 1 or data.get("roll") == 1
        if birthdate:
            try:
                parts = birthdate.split("-")
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
    else:
        sign_key = request.args.get("sign")
        birthdate = request.args.get("birthdate")
        if birthdate:
            try:
                parts = birthdate.split("-")
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
        elif sign_key:
            sign_key = sign_key.lower()
    if not sign_key or sign_key not in ZODIAC_DATA:
        sign_key = "aries"
    z = ZODIAC_DATA[sign_key]
    roast_info = get_ai_roast(sign_key, refresh=refresh)
    sign_b = None
    if request.method == "POST":
        data = request.get_json() or {}
        sign_b = data.get("sign_b")
    else:
        sign_b = request.args.get("sign_b")
    relationship_roast = None
    if sign_b and sign_b.lower() in ZODIAC_DATA:
        relationship_roast = get_ai_relationship_roast(
            sign_key, sign_b.lower(), refresh=refresh
        )
    return jsonify(
        {
            "sign_key": sign_key,
            "name": z["name"],
            "element": z["element"],
            "date_range": z["date_range"],
            "roast": roast_info,
            "relationship_roast": relationship_roast,
        }
    )


@zodiak_bp.route("/api/zodiak/zodiac/<sign>")
def get_zodiac(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404
    z = ZODIAC_DATA[sign_key]
    cosmic = get_cosmic_context()
    genz_readings = get_daily_horoscope(sign_key, cosmic)
    dynamic_ratings = genz_readings.get("ratings") or generate_dynamic_ratings(
        z["base_ratings"], cosmic, z["ruler_planet"], sign_key
    )
    youtube_track = genz_readings.get("youtube_track") or get_daily_youtube_track(
        sign_key, cosmic
    )
    ruler_planet = z["ruler_planet"]
    planet_info = cosmic["planet_status"].get(ruler_planet, {})
    ruler_status = planet_info.get("label", "✅ Langsung")
    strengths = genz_readings.get("strengths") or z["strengths"]
    weaknesses = genz_readings.get("weaknesses") or z["weaknesses"]
    return jsonify(
        {
            "name": z["name"],
            "date_range": z["date_range"],
            "element": z["element"],
            "ruler": z["ruler"],
            "strengths": strengths,
            "weaknesses": weaknesses,
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
                "weather": cosmic["weather"],
            },
        }
    )


@zodiak_bp.route("/api/zodiak/general/<sign>")
@zodiak_bp.route("/api/zodiak/karakter/<sign>")
def get_general_details(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404
    z = ZODIAC_DATA[sign_key]
    char = GENERAL_CHARACTERISTICS.get(sign_key, GENERAL_CHARACTERISTICS["aries"])
    return jsonify(
        {
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
            "fun_fact": char["fun_fact"],
        }
    )


@zodiak_bp.route("/api/zodiak/compatibility/<sign_one>/<sign_two>")
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
        base_metrics.update(
            {"score": 80, "love": 82, "comm": 78, "trust": 85, "future": 75}
        )
    elif (
        (s1_key == "scorpio" and s2_key == "cancer")
        or (s1_key == "cancer" and s2_key == "scorpio")
        or (s1_key == "leo" and s2_key == "aries")
        or (s1_key == "aries" and s2_key == "leo")
        or (s1_key == "gemini" and s2_key == "libra")
        or (s1_key == "libra" and s2_key == "gemini")
    ):
        base_metrics.update(
            {"score": 98, "love": 99, "comm": 97, "trust": 98, "future": 98}
        )
    base_score = base_metrics["score"]
    love_score = min(99, max(45, int(base_score * 1.02)))
    if love_score >= 85:
        love_status = "Sangat Harmonis (Kosmik Selaras) ✨"
        love_summary = f"Kombinasi asmara antara {z1['name']} ({elem_one}) dan {z2['name']} ({elem_two}) membentuk perpaduan cinta yang luar biasa kuat dan penuh daya tarik emosional."
        love_strengths = [
            "Chemistry cinta meletup-letup dan romantis",
            "Saling memahami perasaan tanpa banyak bicara",
            "Dukungan emosional yang hangat dan menenangkan",
        ]
        love_challenges = [
            "Kecenderungan menyembunyikan masalah emosional kecil",
            "Menjaga ritme romansa agar tidak menjadi rutinitas",
        ]
    elif love_score >= 70:
        love_status = "Cinta Kuat & Komitmen Tinggi 💖"
        love_summary = f"Hubungan {z1['name']} dan {z2['name']} memiliki fondasi kesetiaan yang stabil. Perbedaan gaya mencintai justru saling melengkapi kelemahan masing-masing."
        love_strengths = [
            "Saling melengkapi bahasa cinta (love language)",
            "Kesetiaan tinggi dan komitmen jangka panjang",
            "Rasa aman saat bersama",
        ]
        love_challenges = [
            "Perbedaan cara merespon konflik emosional",
            "Butuh waktu untuk menyelaraskan ekspektasi",
        ]
    else:
        love_status = "Tantangan Kompromi Asmara ⚡"
        love_summary = f"Perpaduan elemen {elem_one} dan {elem_two} membutuhkan kesabaran ekstra dalam asmara. Butuh komunikasi terbuka untuk menyelaraskan keinginan ego."
        love_strengths = [
            "Memberikan pelajaran kedewasaan emosional",
            "Daya tarik perbedaan karakter yang kuat",
            "Menumbuhkan rasa toleransi tinggi",
        ]
        love_challenges = [
            "Kecerobohan emosi saat dipicu rasa cemburu",
            "Perbedaan ritme mengekspresikan kasih sayang",
        ]
    friend_score = min(
        99,
        max(
            40,
            int(
                base_score * 0.98
                + (
                    10
                    if elem_one in ["Udara", "Api"] and elem_two in ["Udara", "Api"]
                    else 0
                )
            ),
        ),
    )
    if friend_score >= 85:
        friend_status = "Bestie Sejati (Frekuensi Selaras) 🤝"
        friend_summary = f"Sebagai sahabat, {z1['name']} dan {z2['name']} adalah kombinasi duo paling seru! Keduanya bisa ngobrolin apa saja dari spill the tea hingga topik filsafat tanpa takut di-judge."
        friend_strengths = [
            "Frekuensi humor dan nyambung obrolannya 100%",
            "Tempat curhat aman tanpa rasa canggung",
            "Selalu siap saling bantu di masa sulit",
        ]
        friend_challenges = [
            "Sering lupa waktu kalau udah ketemu dan ngobrol",
            "Keduanya sama-sama suka ceplas-ceplos",
        ]
    elif friend_score >= 70:
        friend_status = "Teman Asyik & Suportif 🥳"
        friend_summary = f"Pertemanan antara {z1['name']} dan {z2['name']} sangat menyenangkan untuk diajak nongkrong, berpetualang, atau nyobain hal-hal baru bersama."
        friend_strengths = [
            "Asyik diajak jalan-jalan atau nyobain kuliner baru",
            "Saling mendukung impian satu sama lain",
            "Bisa menjaga rahasia dengan baik",
        ]
        friend_challenges = [
            "Kadang butuh waktu sendiri jika mood sedang tidak bagus",
            "Jarang menyampaikan rasa tidak suka secara langsung",
        ]
    else:
        friend_status = "Teman Kasual (Perlu Saling Menghormati) ☕"
        friend_summary = f"Hubungan pertemanan ini paling pas berada di tingkat kasual. Menghormati batasan dan ruang pribadi adalah kunci agar hubungan pertemanan tetap awet."
        friend_strengths = [
            "Membawa sudut pandang baru yang tidak terpikirkan",
            "Menguji batas kepekaan sosial",
            "Menyenangkan saat mengerjakan proyek hobi tertentu",
        ]
        friend_challenges = [
            "Gaya bercanda kadang tidak sengaja menyinggung perasaan",
            "Perbedaan selera aktivitas waktu luang",
        ]
    work_score = min(
        99,
        max(
            40,
            int(
                base_score * 0.95
                + (
                    12
                    if elem_one in ["Tanah", "Api"] and elem_two in ["Tanah", "Api"]
                    else 5
                )
            ),
        ),
    )
    if work_score >= 85:
        work_status = "Dream Team Profesional (Sinergi Tinggi) 💼"
        work_summary = f"Di tempat kerja, {z1['name']} dan {z2['name']} adalah kombinasi Dream Team! Satu pihak mahir memikirkan ide & strategi, sementara pihak lainnya tangguh dalam eksekusi target."
        work_strengths = [
            "Sinergi eksekusi proyek sangat cepat dan efisien",
            "Pembagian tugas yang sangat alami dan saling melengkapi",
            "Fokus tinggi pada pencapaian target kerja",
        ]
        work_challenges = [
            "Keduanya bisa terlalu kompetitif jika tidak menetapkan tujuan bersama",
            "Cenderung lupa istirahat karena keasyikan kerja",
        ]
    elif work_score >= 70:
        work_status = "Rekan Kerja Efisien & Produktif 📈"
        work_summary = f"Kerja sama profesional antara {z1['name']} dan {z2['name']} berjalan lancar dan terorganisir. Mereka dapat mencapai deadline dengan hasil memuaskan."
        work_strengths = [
            "Komunikasi profesional yang jelas dan terarah",
            "Saling menghormati wewenang dan job description",
            "Dapat diandalkan dalam pemecahan masalah teknis",
        ]
        work_challenges = [
            "Perlu menyelaraskan ritme kerja saat tekanan deadline tinggi",
            "Kadang terlalu kaku dalam mengambil keputusan kompromi",
        ]
    else:
        work_status = "Perlu Pembagian Tugas Jelas 🛠️"
        work_summary = f"Dalam dunia kerja, {z1['name']} dan {z2['name']} membutuhkan struktur dan SOP yang sangat transparan agar tidak terjadi tumpang tindih wewenang."
        work_strengths = [
            "Saling menguji kelemahan konsep bisnis sebelum eksekusi",
            "Mendorong kehati-hatian dalam mengambil risiko",
            "Membuat analisis kerja menjadi lebih tajam",
        ]
        work_challenges = [
            "Potensi benturan ego saat mempertahankan ide masing-masing",
            "Perbedaan gaya manajemen waktu",
        ]
    modes_data = {
        "romance": {
            "label": "Pasangan (Asmara)",
            "icon": "fa-heart",
            "score": love_score,
            "status": love_status,
            "summary": love_summary,
            "strengths": love_strengths,
            "challenges": love_challenges,
            "metrics": {
                "love": base_metrics["love"],
                "comm": base_metrics["comm"],
                "trust": base_metrics["trust"],
                "future": base_metrics["future"],
            },
        },
        "friendship": {
            "label": "Sahabat (Bestie)",
            "icon": "fa-user-group",
            "score": friend_score,
            "status": friend_status,
            "summary": friend_summary,
            "strengths": friend_strengths,
            "challenges": friend_challenges,
            "metrics": {
                "love": base_metrics["comm"],
                "comm": base_metrics["comm"],
                "trust": base_metrics["trust"],
                "future": int((friend_score + base_metrics["comm"]) / 2),
            },
        },
        "work": {
            "label": "Rekan Kerja",
            "icon": "fa-briefcase",
            "score": work_score,
            "status": work_status,
            "summary": work_summary,
            "strengths": work_strengths,
            "challenges": work_challenges,
            "metrics": {
                "love": base_metrics["comm"],
                "comm": base_metrics["comm"],
                "trust": base_metrics["trust"],
                "future": int((work_score + base_metrics["trust"]) / 2),
            },
        },
    }
    modes_data = get_ai_compatibility_modes(
        s1_key, s2_key, z1["name"], elem_one, z2["name"], elem_two, modes_data
    )
    return jsonify(
        {
            "sign_one": z1["name"],
            "sign_two": z2["name"],
            "element_one": elem_one,
            "element_two": elem_two,
            "modes": modes_data,
        }
    )


import json, random, string
from .quiz_bank import (
    PARTNER_QUIZ_QUESTIONS,
    calculate_quiz_match,
    get_ai_couple_quiz_analysis,
)
from .ai_limiter import _get_mysql_connection


@zodiak_bp.route("/api/zodiak/quiz/questions")
def get_quiz_questions():
    return jsonify({"questions": PARTNER_QUIZ_QUESTIONS})


@zodiak_bp.route("/api/zodiak/quiz/create_room", methods=["POST"])
def create_quiz_room():
    data = request.get_json(silent=True) or {}
    host_name = str(data.get("host_name", "")).strip()
    host_sign = str(data.get("host_sign", "")).strip().lower()
    if not host_name or not host_sign:
        return jsonify({"error": "Nama dan Zodiak Host wajib diisi."}), 400
    code_chars = "".join(random.choices(string.ascii_uppercase + string.digits, k=5))
    room_code = f"RO-{code_chars}"
    conn = _get_mysql_connection()
    if conn:
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    INSERT INTO quiz_rooms (room_code, host_name, host_sign, host_answers, status)
                    VALUES (%s, %s, %s, NULL, 'waiting');
                """,
                    (room_code, host_name, host_sign),
                )
            conn.close()
        except Exception as e:
            if conn:
                conn.close()
            return jsonify({"error": f"Gagal membuat room di database: {str(e)}"}), 500
    else:
        return jsonify({"error": "Database tidak terhubung."}), 500
    share_url = f"{request.host_url}zodiak/kecocokan?room={room_code}"
    return jsonify(
        {
            "status": "success",
            "room_code": room_code,
            "share_url": share_url,
            "host_name": host_name,
            "host_sign": host_sign,
        }
    )


@zodiak_bp.route("/api/zodiak/quiz/join_room", methods=["POST"])
def join_quiz_room():
    data = request.get_json(silent=True) or {}
    room_code = str(data.get("room_code", "")).strip().upper()
    partner_name = str(data.get("partner_name", "")).strip()
    partner_sign = str(data.get("partner_sign", "")).strip().lower()
    if not room_code or not partner_name or not partner_sign:
        return (
            jsonify({"error": "Kode room, nama, dan zodiak partner wajib diisi."}),
            400,
        )
    conn = _get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database tidak terhubung."}), 500
    row = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quiz_rooms WHERE room_code = %s;", (room_code,)
            )
            row = cursor.fetchone()
    except Exception:
        pass
    if not row:
        if conn:
            conn.close()
        return (
            jsonify({"error": "Room tidak ditemukan. Pastikan kode room benar."}),
            404,
        )
    if row.get("status") == "completed":
        h_sign = (row["host_sign"] or "").lower()
        p_sign = (row["partner_sign"] or "").lower()
        zodiac_score = 75
        if h_sign in ZODIAC_DATA and p_sign in ZODIAC_DATA:
            e1 = ZODIAC_DATA[h_sign]["element"]
            e2 = ZODIAC_DATA[p_sign]["element"]
            zodiac_score = ELEMENT_COMPATIBILITY.get(e1, {}).get(e2, {}).get("love", 75)
        breakdown = (
            json.loads(row["breakdown_json"]) if row.get("breakdown_json") else []
        )
        ai_result = (
            json.loads(row["ai_result_json"]) if row.get("ai_result_json") else None
        )
        if conn:
            conn.close()
        return jsonify(
            {
                "status": "completed",
                "is_locked": True,
                "message": "Room ini sudah selesai terisi dan dijawab oleh kedua pasangan.",
                "room_code": room_code,
                "host_name": row["host_name"],
                "host_sign": row["host_sign"],
                "partner_name": row.get("partner_name"),
                "partner_sign": row.get("partner_sign"),
                "match_score": row.get("match_score", 0),
                "zodiac_score": zodiac_score,
                "breakdown": breakdown,
                "ai_result": ai_result,
            }
        )
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                """
                UPDATE quiz_rooms 
                SET partner_name = %s, partner_sign = %s
                WHERE room_code = %s;
            """,
                (partner_name, partner_sign, room_code),
            )
        conn.close()
    except Exception:
        if conn:
            conn.close()
    return jsonify(
        {
            "status": "success",
            "room_code": room_code,
            "host_name": row["host_name"],
            "host_sign": row["host_sign"],
            "partner_name": partner_name,
            "partner_sign": partner_sign,
        }
    )


@zodiak_bp.route("/api/zodiak/quiz/submit_answers", methods=["POST"])
def submit_quiz_answers():
    data = request.get_json(silent=True) or {}
    room_code = str(data.get("room_code", "")).strip().upper()
    role = str(data.get("role", "host")).strip().lower()
    answers = data.get("answers", [])
    if not room_code or not isinstance(answers, list) or len(answers) < 10:
        return jsonify({"error": "Data jawaban 10 pertanyaan tidak lengkap."}), 400
    conn = _get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database tidak terhubung."}), 500
    row = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quiz_rooms WHERE room_code = %s;", (room_code,)
            )
            row = cursor.fetchone()
    except Exception:
        pass
    if not row:
        if conn:
            conn.close()
        return jsonify({"error": "Room tidak ditemukan."}), 404
    if row.get("status") == "completed":
        h_sign = (row["host_sign"] or "").lower()
        p_sign = (row["partner_sign"] or "").lower()
        zodiac_score = 75
        if h_sign in ZODIAC_DATA and p_sign in ZODIAC_DATA:
            e1 = ZODIAC_DATA[h_sign]["element"]
            e2 = ZODIAC_DATA[p_sign]["element"]
            zodiac_score = ELEMENT_COMPATIBILITY.get(e1, {}).get(e2, {}).get("love", 75)
        breakdown = (
            json.loads(row["breakdown_json"]) if row.get("breakdown_json") else []
        )
        ai_result = (
            json.loads(row["ai_result_json"]) if row.get("ai_result_json") else None
        )
        if conn:
            conn.close()
        return jsonify(
            {
                "status": "completed",
                "is_locked": True,
                "message": "Room ini sudah selesai dan jawabannya telah terkunci.",
                "room_code": room_code,
                "host_name": row["host_name"],
                "host_sign": row["host_sign"],
                "partner_name": row.get("partner_name"),
                "partner_sign": row.get("partner_sign"),
                "match_score": row.get("match_score", 0),
                "zodiac_score": zodiac_score,
                "breakdown": breakdown,
                "ai_result": ai_result,
            }
        )
    host_answers = json.loads(row["host_answers"]) if row.get("host_answers") else None
    partner_answers = (
        json.loads(row["partner_answers"]) if row.get("partner_answers") else None
    )
    if role == "host":
        host_answers = answers
        sql_update = "UPDATE quiz_rooms SET host_answers = %s WHERE room_code = %s;"
    else:
        partner_answers = answers
        sql_update = "UPDATE quiz_rooms SET partner_answers = %s WHERE room_code = %s;"
    try:
        with conn.cursor() as cursor:
            cursor.execute(sql_update, (json.dumps(answers), room_code))
    except Exception as e:
        if conn:
            conn.close()
        return jsonify({"error": f"Gagal menyimpan jawaban: {str(e)}"}), 500
    is_both_completed = (
        host_answers is not None
        and isinstance(host_answers, list)
        and len(host_answers) >= 10
        and partner_answers is not None
        and isinstance(partner_answers, list)
        and len(partner_answers) >= 10
    )
    match_score = row.get("match_score", 0)
    breakdown = json.loads(row["breakdown_json"]) if row.get("breakdown_json") else []
    ai_result = json.loads(row["ai_result_json"]) if row.get("ai_result_json") else None
    if is_both_completed:
        match_score, breakdown = calculate_quiz_match(host_answers, partner_answers)
        host_name = row["host_name"]
        host_sign = row["host_sign"]
        partner_name = row.get("partner_name") or "Partner"
        partner_sign = row.get("partner_sign") or "taurus"
        ai_result = get_ai_couple_quiz_analysis(
            host_name, host_sign, partner_name, partner_sign, match_score, breakdown
        )
        try:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    UPDATE quiz_rooms 
                    SET status = 'completed', match_score = %s, breakdown_json = %s, ai_result_json = %s
                    WHERE room_code = %s;
                """,
                    (
                        match_score,
                        json.dumps(breakdown),
                        json.dumps(ai_result),
                        room_code,
                    ),
                )
            conn.close()
        except Exception:
            if conn:
                conn.close()
    else:
        if conn:
            conn.close()
    host_sign = row["host_sign"]
    partner_sign = row.get("partner_sign") or "taurus"
    zodiac_score = 75
    if host_sign in ZODIAC_DATA and partner_sign in ZODIAC_DATA:
        e1 = ZODIAC_DATA[host_sign]["element"]
        e2 = ZODIAC_DATA[partner_sign]["element"]
        zodiac_score = ELEMENT_COMPATIBILITY.get(e1, {}).get(e2, {}).get("love", 75)
    return jsonify(
        {
            "status": "completed" if is_both_completed else "waiting_other",
            "room_code": room_code,
            "host_name": row["host_name"],
            "host_sign": row["host_sign"],
            "partner_name": row.get("partner_name"),
            "partner_sign": row.get("partner_sign"),
            "has_host_answered": host_answers is not None,
            "has_partner_answered": partner_answers is not None,
            "match_score": match_score,
            "zodiac_score": zodiac_score,
            "breakdown": breakdown,
            "ai_result": ai_result,
        }
    )


@zodiak_bp.route("/api/zodiak/quiz/room/<room_code>")
def get_quiz_room_status(room_code):
    room_code = room_code.strip().upper()
    conn = _get_mysql_connection()
    if not conn:
        return jsonify({"error": "Database tidak terhubung."}), 500
    row = None
    try:
        with conn.cursor() as cursor:
            cursor.execute(
                "SELECT * FROM quiz_rooms WHERE room_code = %s;", (room_code,)
            )
            row = cursor.fetchone()
        conn.close()
    except Exception:
        if conn:
            conn.close()
    if not row:
        return jsonify({"error": "Room tidak ditemukan."}), 404
    h_sign = row["host_sign"].lower()
    p_sign = (row["partner_sign"] or "").lower()
    zodiac_score = 75
    if h_sign in ZODIAC_DATA and p_sign in ZODIAC_DATA:
        e1 = ZODIAC_DATA[h_sign]["element"]
        e2 = ZODIAC_DATA[p_sign]["element"]
        zodiac_score = ELEMENT_COMPATIBILITY.get(e1, {}).get(e2, {}).get("love", 75)
    host_answers = json.loads(row["host_answers"]) if row.get("host_answers") else None
    partner_answers = (
        json.loads(row["partner_answers"]) if row.get("partner_answers") else None
    )
    breakdown = json.loads(row["breakdown_json"]) if row.get("breakdown_json") else []
    ai_result = json.loads(row["ai_result_json"]) if row.get("ai_result_json") else None
    return jsonify(
        {
            "room_code": row["room_code"],
            "status": row["status"],
            "host_name": row["host_name"],
            "host_sign": row["host_sign"],
            "partner_name": row.get("partner_name"),
            "partner_sign": row.get("partner_sign"),
            "has_host_answered": host_answers is not None,
            "has_partner_answered": partner_answers is not None,
            "match_score": row.get("match_score", 0),
            "zodiac_score": zodiac_score,
            "breakdown": breakdown,
            "ai_result": ai_result,
            "created_at": str(row["created_at"]),
        }
    )
