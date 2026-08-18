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
    
    return {
        "title": f"{shio['name']} {element['name']}",
        "fortune": f"Energi kosmik {element['name'].lower()} berpadu dengan karakter {shio['name'].lower()} Anda. {element['vibe']} "
                   f"Kekuatan utama Anda saat ini terletak pada sifat {shio['traits'][0].lower()} dan {shio['traits'][1].lower()}.",
        "lucky_direction": "Timur Laut",
        "lucky_numbers": [3, 8, 12]
    }
