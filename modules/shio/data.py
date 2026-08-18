import random

SHIO_DATA = {
    "tikus": {"name": "Tikus", "icon": "🐀", "traits": ["Cerdik", "Adaptif", "Kreatif", "Agresif"]},
    "kerbau": {"name": "Kerbau", "icon": "🐂", "traits": ["Dapat diandalkan", "Tenang", "Metodis", "Keras Kepala"]},
    "macan": {"name": "Macan", "icon": "🐅", "traits": ["Pemberani", "Kompetitif", "Tidak dapat diprediksi", "Percaya diri"]},
    "kelinci": {"name": "Kelinci", "icon": "🐇", "traits": ["Lemah lembut", "Tenang", "Elegan", "Waspada"]},
    "naga": {"name": "Naga", "icon": "🐉", "traits": ["Percaya diri", "Cerdas", "Antusias", "Dominan"]},
    "ular": {"name": "Ular", "icon": "🐍", "traits": ["Penuh teka-teki", "Cerdas", "Bijaksana", "Materialistis"]},
    "kuda": {"name": "Kuda", "icon": "🐎", "traits": ["Aktif", "Energik", "Lucu", "Tidak sabar"]},
    "kambing": {"name": "Kambing", "icon": "🐐", "traits": ["Tenang", "Lembut", "Simpatik", "Pemalu"]},
    "monyet": {"name": "Monyet", "icon": "🐒", "traits": ["Cerdas", "Inovatif", "Suka bergaul", "Egois"]},
    "ayam": {"name": "Ayam", "icon": "🐓", "traits": ["Pengamat", "Pekerja keras", "Berani", "Sombong"]},
    "anjing": {"name": "Anjing", "icon": "🐕", "traits": ["Sangat setia", "Jujur", "Baik hati", "Penuh kehati-hatian"]},
    "babi": {"name": "Babi", "icon": "🐖", "traits": ["Welaskasih", "Murah hati", "Rajin", "Materialistis"]}
}

ELEMENT_DATA = {
    "kayu": {"name": "Kayu", "color": "Hijau", "vibe": "Pertumbuhan dan kasih sayang. Momen untuk berekspansi."},
    "api": {"name": "Api", "color": "Merah", "vibe": "Semangat dan keberanian. Saatnya mengambil risiko."},
    "tanah": {"name": "Tanah", "color": "Cokelat", "vibe": "Kestabilan dan kepraktisan. Fokus pada hal-hal fundamental."},
    "logam": {"name": "Logam", "color": "Putih/Emas", "vibe": "Fokus dan ketekunan. Jangan menyerah pada rintangan."},
    "air": {"name": "Air", "color": "Hitam/Biru", "vibe": "Kebijaksanaan dan fleksibilitas. Mengalir bersama perubahan."}
}

def generate_shio_fortune(shio_key, element_key):
    shio = SHIO_DATA.get(shio_key, SHIO_DATA["naga"])
    element = ELEMENT_DATA.get(element_key, ELEMENT_DATA["kayu"])
    
    # Deterministic generation based on combination
    seed_val = sum(ord(c) for c in (shio_key + element_key))
    rng = random.Random(seed_val)
    
    karir_pool = [
        f"Karakter {shio['traits'][0].lower()} membawa Anda pada peluang luar biasa. {element['vibe'].split('.')[0]} di tempat kerja.",
        f"Tantangan baru muncul, tapi sisi {shio['traits'][1].lower()} Anda bisa menyelesaikannya. Gunakan energi {element['name']} untuk negosiasi.",
        f"Kerja sama tim akan sangat menguntungkan jika Anda menonjolkan sifat {shio['traits'][0].lower()}. Hindari bersikap terlalu {shio['traits'][3].lower()}."
    ]
    
    keuangan_pool = [
        f"Ada potensi rezeki dari investasi masa lalu. Pertahankan sikap {shio['traits'][1].lower()} dalam mengelola keuangan.",
        f"Energi {element['name']} mendatangkan kelimpahan, namun sifat {shio['traits'][3].lower()} Anda bisa membuat pemborosan. Berhati-hatilah.",
        f"Bulan ini stabil. Keputusan finansial yang Anda buat dengan cara {shio['traits'][0].lower()} akan membuahkan hasil manis di masa depan."
    ]
    
    asmara_pool = [
        f"Hubungan asmara sedang hangat. Sifat {shio['traits'][2].lower()} membuat pasangan semakin lengket. {element['name']} memperkuat ikatan.",
        f"Jika lajang, pesona {shio['traits'][0].lower()} Anda menarik perhatian seseorang. Jika berpasangan, waspadai sifat {shio['traits'][3].lower()} yang memicu konflik.",
        f"Waktunya kejujuran emosional. {element['vibe']} Karakter {shio['traits'][1].lower()} Anda akan membantu menjembatani perbedaan pendapat."
    ]
    
    kesehatan_pool = [
        f"Fokus pada vitalitas elemen {element['name']}. Sifat {shio['traits'][3].lower()} terkadang memicu stres mental, perbanyak relaksasi.",
        f"Kesehatan fisik sangat prima berkat gaya hidup {shio['traits'][0].lower()}. Jangan lupa seimbangkan dengan kesehatan spiritual.",
        f"Ada sedikit penurunan energi kosmik. Hindari begadang, dan jadikan sifat {shio['traits'][1].lower()} Anda untuk disiplin berolahraga."
    ]

    return {
        "title": f"{shio['name']} {element['name']}",
        "fortune": f"Ramalan paduan kosmik antara {shio['name']} dan {element['name']} membentuk energi unik bagi jalan hidup Anda saat ini.",
        "traits": ", ".join(shio["traits"]),
        "vibe": element["vibe"],
        "karir": rng.choice(karir_pool),
        "keuangan": rng.choice(keuangan_pool),
        "asmara": rng.choice(asmara_pool),
        "kesehatan": rng.choice(kesehatan_pool),
        "lucky_direction": rng.choice(["Utara", "Selatan", "Timur", "Barat", "Timur Laut", "Barat Daya", "Tenggara", "Barat Laut"]),
        "lucky_numbers": [rng.randint(1, 9), rng.randint(10, 30), rng.randint(31, 99)]
    }
