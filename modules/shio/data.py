import random
import datetime
from .bank import (
    DAILY_CIONG_MESSAGES, DAILY_SAN_HE_MESSAGES, DAILY_LIU_HE_MESSAGES,
    DAILY_WARNING_MESSAGES, DAILY_TAI_SUI_MESSAGES, DAILY_NEUTRAL_MESSAGES,
    SHIO_DAILY_TIPS, SHIO_GUARDIAN_BANK
)

SHIO_DATA = {
    "tikus": {"name": "Tikus", "icon": "🐀", "hanzi": "鼠", "traits": ["Cerdik", "Adaptif", "Kreatif", "Agresif"]},
    "kerbau": {"name": "Kerbau", "icon": "🐂", "hanzi": "牛", "traits": ["Dapat diandalkan", "Tenang", "Metodis", "Keras Kepala"]},
    "macan": {"name": "Macan", "icon": "🐅", "hanzi": "虎", "traits": ["Pemberani", "Kompetitif", "Tidak dapat diprediksi", "Percaya diri"]},
    "kelinci": {"name": "Kelinci", "icon": "🐇", "hanzi": "兔", "traits": ["Lemah lembut", "Tenang", "Elegan", "Waspada"]},
    "naga": {"name": "Naga", "icon": "🐉", "hanzi": "龍", "traits": ["Percaya diri", "Cerdas", "Antusias", "Dominan"]},
    "ular": {"name": "Ular", "icon": "🐍", "hanzi": "蛇", "traits": ["Penuh teka-teki", "Cerdas", "Bijaksana", "Materialistis"]},
    "kuda": {"name": "Kuda", "icon": "🐎", "hanzi": "馬", "traits": ["Aktif", "Energik", "Lucu", "Tidak sabar"]},
    "kambing": {"name": "Kambing", "icon": "🐐", "hanzi": "羊", "traits": ["Tenang", "Lembut", "Simpatik", "Pemalu"]},
    "monyet": {"name": "Monyet", "icon": "🐒", "hanzi": "猴", "traits": ["Cerdas", "Inovatif", "Suka bergaul", "Egois"]},
    "ayam": {"name": "Ayam", "icon": "🐓", "hanzi": "雞", "traits": ["Pengamat", "Pekerja keras", "Berani", "Sombong"]},
    "anjing": {"name": "Anjing", "icon": "🐕", "hanzi": "狗", "traits": ["Sangat setia", "Jujur", "Baik hati", "Penuh kehati-hatian"]},
    "babi": {"name": "Babi", "icon": "🐖", "hanzi": "豬", "traits": ["Welaskasih", "Murah hati", "Rajin", "Materialistis"]}
}

ELEMENT_DATA = {
    "kayu": {"name": "Kayu", "color": "Hijau", "vibe": "Pertumbuhan dan kasih sayang. Momen untuk berekspansi."},
    "api": {"name": "Api", "color": "Merah", "vibe": "Semangat dan keberanian. Saatnya mengambil risiko."},
    "tanah": {"name": "Tanah", "color": "Cokelat", "vibe": "Kestabilan dan kepraktisan. Fokus pada hal-hal fundamental."},
    "logam": {"name": "Logam", "color": "Putih/Emas", "vibe": "Fokus dan ketekunan. Jangan menyerah pada rintangan."},
    "air": {"name": "Air", "color": "Hitam/Biru", "vibe": "Kebijaksanaan dan fleksibilitas. Mengalir bersama perubahan."}
}

SHIOS_LIST = ["tikus", "kerbau", "macan", "kelinci", "naga", "ular", "kuda", "kambing", "monyet", "ayam", "anjing", "babi"]
ELEMENTS_LIST = ["kayu", "api", "tanah", "logam", "air"]
LIU_HE_PAIRS = [(0,1), (1,0), (2,11), (11,2), (3,10), (10,3), (4,9), (9,4), (5,8), (8,5), (6,7), (7,6)]

def generate_shio_fortune(shio_key, element_key):
    shio = SHIO_DATA.get(shio_key, SHIO_DATA["naga"])
    element = ELEMENT_DATA.get(element_key, ELEMENT_DATA["kayu"])
    
    # Deterministic generation based on combination
    seed_val = sum(ord(c) for c in (shio_key + element_key))
    rng = random.Random(seed_val)
    
    career_pool = [
        f"Peluang emas di tempat kerja. Karakter {shio['traits'][0].lower()} Anda dihargai oleh atasan.",
        f"Waktunya berkolaborasi. Energi {element['name']} membawa hoki dalam negosiasi. Pertahankan semangat {shio['traits'][2].lower()}.",
        f"Ada hambatan kecil, namun dedikasi {shio['traits'][1].lower()} Anda akan menyelesaikannya. Hindari konflik."
    ]
    
    finance_pool = [
        f"Ada potensi rezeki dari investasi masa lalu. Pertahankan sikap {shio['traits'][1].lower()} dalam mengelola keuangan.",
        f"Energi {element['name']} mendatangkan kelimpahan, namun sifat {shio['traits'][3].lower()} Anda bisa membuat pemborosan. Berhati-hatilah.",
        f"Bulan ini stabil. Keputusan finansial yang Anda buat dengan cara {shio['traits'][0].lower()} akan membuahkan hasil manis di masa depan."
    ]
    
    romance_pool = [
        f"Hubungan asmara sedang hangat. Sifat {shio['traits'][2].lower()} membuat pasangan semakin lengket. {element['name']} memperkuat ikatan.",
        f"Jika lajang, pesona {shio['traits'][0].lower()} Anda menarik perhatian seseorang. Jika berpasangan, waspadai sifat {shio['traits'][3].lower()} yang memicu konflik.",
        f"Waktunya kejujuran emosional. {element['vibe']} Karakter {shio['traits'][1].lower()} Anda akan membantu menjembatani perbedaan pendapat."
    ]
    
    health_pool = [
        f"Fokus pada vitalitas elemen {element['name']}. Sifat {shio['traits'][3].lower()} terkadang memicu stres mental, perbanyak relaksasi.",
        f"Kesehatan fisik sangat prima berkat gaya hidup {shio['traits'][0].lower()}. Jangan lupa seimbangkan dengan kesehatan spiritual.",
        f"Ada sedikit penurunan energi kosmik. Hindari begadang, dan jadikan sifat {shio['traits'][1].lower()} Anda untuk disiplin berolahraga."
    ]

    result = {
        "title": f"{shio['name']} {element['name']}",
        "fortune": f"Ramalan paduan kosmik antara {shio['name']} dan {element['name']} membentuk energi unik bagi jalan hidup Anda saat ini.",
        "traits": ", ".join(shio["traits"]),
        "vibe": element["vibe"],
        "career": rng.choice(career_pool),
        "finance": rng.choice(finance_pool),
        "romance": rng.choice(romance_pool),
        "health": rng.choice(health_pool)
    }

    # Daily dynamic seed for lucky numbers and direction
    from datetime import date
    daily_seed = seed_val + sum(ord(c) for c in str(date.today()))
    daily_rng = random.Random(daily_seed)
    
    result["lucky_direction"] = daily_rng.choice(["Utara", "Selatan", "Timur", "Barat", "Timur Laut", "Barat Daya", "Tenggara", "Barat Laut"])
    result["lucky_numbers"] = [daily_rng.randint(1, 9), daily_rng.randint(10, 30), daily_rng.randint(31, 99)]
    
    return result

def get_secret_animal(time_str):
    if not time_str:
        return None
    try:
        hours, mins = map(int, time_str.split(':'))
        time_val = hours + (mins / 60.0)
    except:
        return None
        
    if time_val >= 23 or time_val < 1: return "tikus"
    elif 1 <= time_val < 3: return "kerbau"
    elif 3 <= time_val < 5: return "macan"
    elif 5 <= time_val < 7: return "kelinci"
    elif 7 <= time_val < 9: return "naga"
    elif 9 <= time_val < 11: return "ular"
    elif 11 <= time_val < 13: return "kuda"
    elif 13 <= time_val < 15: return "kambing"
    elif 15 <= time_val < 17: return "monyet"
    elif 17 <= time_val < 19: return "ayam"
    elif 19 <= time_val < 21: return "anjing"
    else: return "babi"

def calculate_yearly_fortune(user_shio_key, current_year):
    # Determine the Shio of the current_year
    # Base year 1924 = Rat
    year_index = (int(current_year) - 1924) % 12
    year_shio_key = SHIOS_LIST[year_index]
    
    user_shio_data = SHIO_DATA.get(user_shio_key, SHIO_DATA["naga"])
    year_shio_data = SHIO_DATA.get(year_shio_key, SHIO_DATA["naga"])
    
    # Calculate relationship
    # Simple harmony/clash based on distance in the 12-cycle
    user_idx = SHIOS_LIST.index(user_shio_key)
    distance = abs(user_idx - year_index)
    if distance > 6:
        distance = 12 - distance
        
    score = 50
    status = "Netral"
    desc = f"Tahun {current_year} (Tahun {year_shio_data['name']}) membawa energi yang netral bagi Anda. Fokus pada konsistensi."
    
    if distance == 6: # Clash (Liu Chong)
        score = 30
        status = "Penuh Tantangan (Ciong)"
        desc = f"Tahun {year_shio_data['name']} bertolak belakang secara langsung (Ciong) dengan Shio {user_shio_data['name']}. Ini tahun untuk menahan diri, hindari keputusan impulsif, dan banyaklah bersabar."
    elif distance == 4: # 3 Harmony (San He)
        score = 85
        status = "Sangat Menguntungkan (San He)"
        desc = f"Energi Tahun {year_shio_data['name']} bersinergi sempurna dengan Anda. Ini adalah tahun emas untuk ekspansi karir dan asmara!"
    elif distance == 0: # Same animal (Ben Ming Nian)
        score = 45
        status = "Tahun Kelahiran (Tai Sui)"
        desc = f"Ini adalah Tahun {user_shio_data['name']}, tahun kelahiran Shio Anda (Tai Sui). Sering dianggap masa fluktuatif. Berhati-hatilah dan kenakan elemen penyeimbang."
    elif (user_idx, year_index) in LIU_HE_PAIRS: # 6 Harmonies (Liu He)
        score = 95
        status = "Keselarasan Sempurna (Liu He)"
        desc = f"Tahun {year_shio_data['name']} membawa Harmoni Keenam bagi {user_shio_data['name']}. Ada penolong misterius dan rezeki tak terduga!"
    else:
        score = 65
        status = "Stabil dan Lancar"
        desc = f"Tahun {year_shio_data['name']} bersahabat dengan {user_shio_data['name']}. Peluang karir dan hubungan akan berjalan mulus jika diusahakan."
        
    return {
        "year": current_year,
        "year_shio": year_shio_data['name'],
        "user_shio": user_shio_data['name'],
        "score": score,
        "status": status,
        "description": desc
    }

def calculate_compatibility(shio1_key, shio2_key, elem1_key, elem2_key, time1=None, time2=None):
    idx1 = SHIOS_LIST.index(shio1_key)
    idx2 = SHIOS_LIST.index(shio2_key)
    
    # Shio Score
    dist = abs(idx1 - idx2)
    if dist > 6: dist = 12 - dist
    
    shio_score = 50
    shio_rel = "Biasa Saja"
    if dist == 6:
        shio_score = 20
        shio_rel = "Ciong (Bentrokan Ekstrem)"
    elif dist == 4:
        shio_score = 90
        shio_rel = "San He (Tiga Harmoni)"
    elif (idx1, idx2) in LIU_HE_PAIRS:
        shio_score = 100
        shio_rel = "Liu He (Jodoh Kosmik Sejati)"
    elif dist == 3:
        shio_score = 40
        shio_rel = "Ketegangan (Friksi Rahasia)"
    elif dist == 2:
        shio_score = 65
        shio_rel = "Harmoni Kecil"
    else:
        shio_score = 60
        shio_rel = "Netral"
        
    # Element Score
    e_idx1 = ELEMENTS_LIST.index(elem1_key)
    e_idx2 = ELEMENTS_LIST.index(elem2_key)
    
    # Wood(0)->Fire(1)->Earth(2)->Metal(3)->Water(4)->Wood(0)
    elem_score = 50
    elem_rel = "Biasa"
    
    if e_idx1 == e_idx2:
        elem_score = 70
        elem_rel = "Saling Mengerti (Elemen Sama)"
    elif (e_idx1 + 1) % 5 == e_idx2 or (e_idx2 + 1) % 5 == e_idx1:
        elem_score = 95
        elem_rel = "Saling Menghidupi (Sheng)"
    elif (e_idx1 + 2) % 5 == e_idx2 or (e_idx2 + 2) % 5 == e_idx1:
        elem_score = 30
        elem_rel = "Saling Menghancurkan (Ke)"
        
    final_score = int((shio_score * 0.7) + (elem_score * 0.3))
    
    status = "Tidak Cocok"
    if final_score >= 85: status = "Soulmate Kosmik"
    elif final_score >= 70: status = "Sangat Cocok"
    elif final_score >= 50: status = "Perlu Kompromi"
    
    desc_romance = f"Kombinasi Shio ({shio_rel}) dan Elemen ({elem_rel}) menghasilkan dinamika yang unik."
    if final_score >= 80:
        desc_romance += " Dalam hubungan asmara, kalian adalah pasangan yang saling melengkapi dan bisa membangun masa depan yang cerah bersama."
    elif final_score >= 60:
        desc_romance += " Asmara kalian butuh banyak komunikasi. Sifat yang bertolak belakang bisa menjadi daya tarik, asalkan ego ditekan."
    else:
        desc_romance += " Hubungan asmara dipenuhi ujian dan perselisihan prinsip. Dibutuhkan kedewasaan luar biasa untuk bertahan."
        
    desc_business = "Di ranah bisnis dan karir, "
    if final_score >= 80:
        desc_business += "energi elemen kalian bersinergi baik, menghasilkan keuntungan berlipat."
    elif final_score >= 60:
        desc_business += "kalian memiliki visi dan etos kerja yang sejalan."
    else:
        desc_business += "kalian rentan berdebat soal arah keuangan. Hindari membuka usaha bersama tanpa perjanjian hitam di atas putih."
        
    # Secret Animal Logic
    secret_rel = ""
    if time1 and time2:
        sec1 = get_secret_animal(time1)
        sec2 = get_secret_animal(time2)
        if sec1 and sec2:
            s_idx1 = SHIOS_LIST.index(sec1)
            s_idx2 = SHIOS_LIST.index(sec2)
            dist_sec = abs(s_idx1 - s_idx2)
            if dist_sec > 6: dist_sec = 12 - dist_sec
            
            s_rel_name = "Netral secara Batin"
            if dist_sec == 6: s_rel_name = "Bentrokan Batin (Ciong Tersembunyi)"
            elif dist_sec == 4: s_rel_name = "Jiwa yang Selaras (San He)"
            elif dist_sec == 3: s_rel_name = "Gesekan Emosional Rahasia"
            elif (s_idx1, s_idx2) in LIU_HE_PAIRS:
                s_rel_name = "Ikatan Batin Jodoh Sejati (Liu He)"
                
            secret_rel = f"{SHIO_DATA.get(sec1)['name']} bertemu {SHIO_DATA.get(sec2)['name']} - {s_rel_name}"

    return {
        "s1_name": f"{SHIO_DATA.get(shio1_key)['name']} {ELEMENT_DATA.get(elem1_key)['name']}",
        "s2_name": f"{SHIO_DATA.get(shio2_key)['name']} {ELEMENT_DATA.get(elem2_key)['name']}",
        "score": final_score,
        "status": status,
        "shio_relation": shio_rel,
        "elem_relation": elem_rel,
        "secret_relation": secret_rel,
        "desc_romance": desc_romance,
        "desc_business": desc_business
    }

def get_daily_shio(client_date_str=None):
    """Calculate the Shio of today based on anchor Jan 1, 2024 = Jia Zi (Wood Rat)"""
    anchor_date = datetime.date(2024, 1, 1) # Rat
    
    if client_date_str:
        try:
            year, month, day = map(int, client_date_str.split('-'))
            target_date = datetime.date(year, month, day)
        except:
            target_date = datetime.date.today()
    else:
        target_date = datetime.date.today()
        
    days_diff = (target_date - anchor_date).days
    
    shio_index = days_diff % 12
    return SHIOS_LIST[shio_index], target_date

def get_all_daily_fortunes(client_date_str=None):
    today_shio_key, target_date = get_daily_shio(client_date_str)
    today_shio_data = SHIO_DATA.get(today_shio_key)
    
    today_idx = SHIOS_LIST.index(today_shio_key)
    
    # Daily seed — same day = same messages, different day = different messages
    daily_seed = sum(ord(c) for c in str(target_date))
    
    results = []
    
    for shio_key in SHIOS_LIST:
        idx = SHIOS_LIST.index(shio_key)
        shio_data = SHIO_DATA.get(shio_key)
        
        dist = abs(today_idx - idx)
        if dist > 6:
            dist = 12 - dist
        
        # Create a unique seed per shio + day combo for varied selection
        msg_seed = daily_seed + idx
        msg_rng = random.Random(msg_seed)
            
        if dist == 6:
            status = "Ciong (Bentrokan)"
            status_code = "bad"
            message = msg_rng.choice(DAILY_CIONG_MESSAGES)
        elif dist == 4:
            status = "San He (Sangat Hoki)"
            status_code = "good"
            message = msg_rng.choice(DAILY_SAN_HE_MESSAGES)
        elif (today_idx, idx) in LIU_HE_PAIRS:
            status = "Liu He (Hoki Ekstra)"
            status_code = "good"
            message = msg_rng.choice(DAILY_LIU_HE_MESSAGES)
        elif dist == 3:
            status = "Waspada (Ketegangan)"
            status_code = "bad"
            message = msg_rng.choice(DAILY_WARNING_MESSAGES)
        elif dist == 0:
            status = "Hari Kembar (Tai Sui)"
            status_code = "neutral"
            message = msg_rng.choice(DAILY_TAI_SUI_MESSAGES)
        else:
            status = "Netral & Stabil"
            status_code = "neutral"
            message = msg_rng.choice(DAILY_NEUTRAL_MESSAGES)
        
        # Pick a daily tip specific to this shio
        tips_list = SHIO_DAILY_TIPS.get(shio_key, [])
        daily_tip = msg_rng.choice(tips_list) if tips_list else ""
            
        results.append({
            "shio_key": shio_key,
            "name": shio_data["name"],
            "icon": shio_data["icon"],
            "hanzi": shio_data["hanzi"],
            "status": status,
            "status_code": status_code,
            "message": message,
            "daily_tip": daily_tip
        })
        
    # Format current date dynamically
    formatted_date = target_date.strftime("%d %B %Y")
        
    return {
        "date_str": formatted_date,
        "today_shio_name": today_shio_data["name"],
        "today_shio_icon": today_shio_data["icon"],
        "today_shio_hanzi": today_shio_data["hanzi"],
        "fortunes": results
    }

def get_shio_guardian(shio_key):
    """Retrieve guardian spiritual data for a given shio."""
    return SHIO_GUARDIAN_BANK.get(shio_key, {})
