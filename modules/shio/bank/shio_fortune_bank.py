# ============================================================
# 📜 SHIO FORTUNE BANK — Ming Li (命理) / Gulungan Takdir
# ============================================================
# Bank data narasi interpretatif untuk fitur "Baca Gulungan Takdir"
# Berisi 10 sub-bank yang digunakan oleh kalkulasi Ba Zi (八字)
#
# Input: Tanggal lahir (wajib) + Jam lahir (opsional)
# Output: 11 seksi hasil pembacaan personal
#
# CATATAN: Chart Ba Zi dihitung secara ALGORITMIK di data.py.
#          Bank ini hanya menyimpan NARASI interpretatif.
# ============================================================


# ============================================================
# 1. DAY_MASTER_BANK — 10 Heavenly Stems (天干)
# ============================================================
# Key: heavenly stem ID (jia, yi, bing, ding, wu, ji, geng, xin, ren, gui)
# Day Master = Heavenly Stem dari Pilar Hari = "diri sejati"
# ============================================================

DAY_MASTER_BANK = {
    "jia": {
        # 甲 — Kayu Yang
        "stem_cn": "甲",
        "stem_id": "Jia",
        "element": "kayu",
        "polarity": "yang",
        "title": "",          # Judul arketipe, cth: "Pohon Besar yang Tak Tergoyahkan"
        "personality": "",    # 2-3 paragraf kepribadian Day Master (Bahasa Indonesia, Gen-Z professional)
        "strengths": [],      # 5-6 kekuatan utama
        "weaknesses": [],     # 5-6 kelemahan utama
    },
    "yi": {
        # 乙 — Kayu Yin
        "stem_cn": "乙",
        "stem_id": "Yi",
        "element": "kayu",
        "polarity": "yin",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "bing": {
        # 丙 — Api Yang
        "stem_cn": "丙",
        "stem_id": "Bing",
        "element": "api",
        "polarity": "yang",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "ding": {
        # 丁 — Api Yin
        "stem_cn": "丁",
        "stem_id": "Ding",
        "element": "api",
        "polarity": "yin",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "wu": {
        # 戊 — Tanah Yang
        "stem_cn": "戊",
        "stem_id": "Wu",
        "element": "tanah",
        "polarity": "yang",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "ji": {
        # 己 — Tanah Yin
        "stem_cn": "己",
        "stem_id": "Ji",
        "element": "tanah",
        "polarity": "yin",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "geng": {
        # 庚 — Logam Yang
        "stem_cn": "庚",
        "stem_id": "Geng",
        "element": "logam",
        "polarity": "yang",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "xin": {
        # 辛 — Logam Yin
        "stem_cn": "辛",
        "stem_id": "Xin",
        "element": "logam",
        "polarity": "yin",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "ren": {
        # 壬 — Air Yang
        "stem_cn": "壬",
        "stem_id": "Ren",
        "element": "air",
        "polarity": "yang",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
    "gui": {
        # 癸 — Air Yin
        "stem_cn": "癸",
        "stem_id": "Gui",
        "element": "air",
        "polarity": "yin",
        "title": "",
        "personality": "",
        "strengths": [],
        "weaknesses": [],
    },
}


# ============================================================
# 2. WUXING_ANALYSIS_BANK — Analisis 5 Elemen (五行)
# ============================================================
# Key: (elemen, status) — status = "dominan" / "lemah" / "kosong"
# Menjelaskan dampak & remedy ketika elemen tertentu terlalu
# kuat, terlalu lemah, atau tidak ada sama sekali di chart.
# ============================================================

WUXING_ANALYSIS_BANK = {
    ("kayu", "dominan"): {
        "status_label": "",     # Label tampilan, cth: "Kayu Mendominasi 🌳⬆"
        "impact": "",           # 2-3 kalimat dampak di kehidupan
        "remedy": "",           # 2-3 kalimat cara menyeimbangkan
    },
    ("kayu", "lemah"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("kayu", "kosong"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("api", "dominan"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("api", "lemah"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("api", "kosong"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("tanah", "dominan"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("tanah", "lemah"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("tanah", "kosong"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("logam", "dominan"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("logam", "lemah"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("logam", "kosong"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("air", "dominan"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("air", "lemah"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
    ("air", "kosong"): {
        "status_label": "",
        "impact": "",
        "remedy": "",
    },
}


# ============================================================
# 3. DESTINY_CAREER_BANK — Proyeksi Karir per Day Master
# ============================================================
# Key: heavenly stem ID (sama seperti DAY_MASTER_BANK)
# ============================================================

DESTINY_CAREER_BANK = {
    "jia": {
        "archetype": "",        # Judul arketipe karir, cth: "Sang Arsitek Visi Besar"
        "ideal_fields": [],     # 5-6 bidang karir ideal
        "work_style": "",       # 2-3 kalimat gaya kerja
        "warning": "",          # 1-2 kalimat peringatan karir
    },
    "yi": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "bing": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "ding": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "wu": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "ji": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "geng": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "xin": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "ren": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
    "gui": {"archetype": "", "ideal_fields": [], "work_style": "", "warning": ""},
}


# ============================================================
# 4. DESTINY_WEALTH_BANK — Peta Keuangan per Day Master
# ============================================================

DESTINY_WEALTH_BANK = {
    "jia": {
        "wealth_type": "",        # Judul tipe rezeki, cth: "Rezeki Mengakar — stabil dari satu sumber besar"
        "investment_advice": "",   # 2-3 kalimat saran investasi
        "financial_trap": "",      # 1-2 kalimat jebakan finansial
        "lucky_period": "",        # 1 kalimat periode keuangan terbaik
    },
    "yi": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "bing": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "ding": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "wu": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "ji": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "geng": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "xin": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "ren": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
    "gui": {"wealth_type": "", "investment_advice": "", "financial_trap": "", "lucky_period": ""},
}


# ============================================================
# 5. DESTINY_LOVE_BANK — Peta Asmara per Day Master
# ============================================================

DESTINY_LOVE_BANK = {
    "jia": {
        "love_type": "",            # Judul tipe asmara, cth: "Romantis Visioner — cinta besar penuh idealisme"
        "ideal_partner_desc": "",   # 2-3 kalimat deskripsi pasangan ideal
        "red_flag": "",             # 1-2 kalimat red flag dalam hubungan
        "peach_blossom_note": "",   # 1-2 kalimat tentang daya tarik romantis
    },
    "yi": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "bing": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "ding": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "wu": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "ji": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "geng": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "xin": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "ren": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
    "gui": {"love_type": "", "ideal_partner_desc": "", "red_flag": "", "peach_blossom_note": ""},
}


# ============================================================
# 6. DESTINY_HEALTH_BANK — Peta Kesehatan
# ============================================================
# Dibagi 2 bagian:
# A. Per Day Master (10 entries) — tipe energi & gaya hidup
# B. Per elemen lemah/kosong (5 entries) — organ rentan
# ============================================================

DESTINY_HEALTH_DAYMASTER = {
    "jia": {
        "energy_type": "",       # Tipe energi fisik, cth: "Energi Batang Besar — kuat tapi kaku"
        "exercise_advice": "",   # 2 kalimat saran olahraga
        "taboo": "",             # 1-2 kalimat pantangan kesehatan
    },
    "yi": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "bing": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "ding": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "wu": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "ji": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "geng": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "xin": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "ren": {"energy_type": "", "exercise_advice": "", "taboo": ""},
    "gui": {"energy_type": "", "exercise_advice": "", "taboo": ""},
}

DESTINY_HEALTH_ELEMENT = {
    # Ketika elemen ini LEMAH atau KOSONG di chart, organ terkait rentan
    "kayu": {
        "vulnerable_organ": "",  # Organ terkait, cth: "Hati (Liver) & Kantung Empedu"
        "symptoms": "",          # 1-2 kalimat gejala umum
        "prevention": "",        # 2 kalimat pencegahan
    },
    "api": {"vulnerable_organ": "", "symptoms": "", "prevention": ""},
    "tanah": {"vulnerable_organ": "", "symptoms": "", "prevention": ""},
    "logam": {"vulnerable_organ": "", "symptoms": "", "prevention": ""},
    "air": {"vulnerable_organ": "", "symptoms": "", "prevention": ""},
}


# ============================================================
# 7. LUCKY_STARS_BANK — Bintang Keberuntungan (吉星)
# ============================================================
# ~12 bintang yang bisa terdeteksi di chart Ba Zi.
# Kalkulasi deteksi dilakukan di data.py.
# ============================================================

LUCKY_STARS_BANK = {
    "tian_yi": {
        # 天乙貴人 — Noble Star / Bintang Penolong
        "name_cn": "天乙貴人",
        "name_id": "",           # Nama Indonesia, cth: "Bintang Penolong Mulia"
        "icon": "⭐",
        "category": "auspicious",  # auspicious / inauspicious / neutral
        "description": "",       # 2-3 kalimat deskripsi bintang
        "life_impact": "",       # 2 kalimat dampak di kehidupan
    },
    "wen_chang": {
        # 文昌星 — Academic Star / Bintang Akademik
        "name_cn": "文昌星",
        "name_id": "",
        "icon": "📚",
        "category": "auspicious",
        "description": "",
        "life_impact": "",
    },
    "tao_hua": {
        # 桃花星 — Peach Blossom Star / Bintang Pesona
        "name_cn": "桃花星",
        "name_id": "",
        "icon": "🌸",
        "category": "neutral",
        "description": "",
        "life_impact": "",
    },
    "yi_ma": {
        # 驛馬星 — Traveling Star / Bintang Perjalanan
        "name_cn": "驛馬星",
        "name_id": "",
        "icon": "🐎",
        "category": "neutral",
        "description": "",
        "life_impact": "",
    },
    "lu_shen": {
        # 祿神 — Wealth/Salary Star / Bintang Rezeki
        "name_cn": "祿神",
        "name_id": "",
        "icon": "💰",
        "category": "auspicious",
        "description": "",
        "life_impact": "",
    },
    "yang_ren": {
        # 羊刃 — Blade Star / Bintang Pedang
        "name_cn": "羊刃",
        "name_id": "",
        "icon": "⚔️",
        "category": "inauspicious",
        "description": "",
        "life_impact": "",
    },
    "hua_gai": {
        # 華蓋星 — Canopy Star / Bintang Spiritual
        "name_cn": "華蓋星",
        "name_id": "",
        "icon": "🛡️",
        "category": "neutral",
        "description": "",
        "life_impact": "",
    },
    "tian_de": {
        # 天德貴人 — Heaven Virtue Star / Bintang Kebajikan
        "name_cn": "天德貴人",
        "name_id": "",
        "icon": "🌟",
        "category": "auspicious",
        "description": "",
        "life_impact": "",
    },
    "yue_de": {
        # 月德貴人 — Moon Virtue Star / Bintang Cahaya Bulan
        "name_cn": "月德貴人",
        "name_id": "",
        "icon": "🌙",
        "category": "auspicious",
        "description": "",
        "life_impact": "",
    },
    "jin_yu": {
        # 金輿星 — Golden Carriage Star / Bintang Kereta Emas
        "name_cn": "金輿星",
        "name_id": "",
        "icon": "🏆",
        "category": "auspicious",
        "description": "",
        "life_impact": "",
    },
    "gu_chen": {
        # 孤辰 — Solitary Star / Bintang Kesendirian
        "name_cn": "孤辰",
        "name_id": "",
        "icon": "🌑",
        "category": "inauspicious",
        "description": "",
        "life_impact": "",
    },
    "gua_su": {
        # 寡宿 — Widow Star / Bintang Janda
        "name_cn": "寡宿",
        "name_id": "",
        "icon": "🥀",
        "category": "inauspicious",
        "description": "",
        "life_impact": "",
    },
}


# ============================================================
# 8. ELEMENT_REMEDY_BANK — Saran Spiritual per Elemen
# ============================================================
# Digunakan ketika user perlu memperkuat elemen yang lemah/kosong.
# ============================================================

ELEMENT_REMEDY_BANK = {
    "kayu": {
        "colors": [],            # Warna keberuntungan, cth: ["Hijau", "Cokelat muda"]
        "directions": [],        # Arah keberuntungan, cth: ["Timur", "Tenggara"]
        "numbers": [],           # Angka keberuntungan
        "crystals": [],          # Kristal/batu yang membantu
        "food_elements": [],     # Makanan yang memperkuat elemen
        "ritual_advice": "",     # 2-3 kalimat saran ritual/kebiasaan
    },
    "api": {"colors": [], "directions": [], "numbers": [], "crystals": [], "food_elements": [], "ritual_advice": ""},
    "tanah": {"colors": [], "directions": [], "numbers": [], "crystals": [], "food_elements": [], "ritual_advice": ""},
    "logam": {"colors": [], "directions": [], "numbers": [], "crystals": [], "food_elements": [], "ritual_advice": ""},
    "air": {"colors": [], "directions": [], "numbers": [], "crystals": [], "food_elements": [], "ritual_advice": ""},
}


# ============================================================
# 9. LIFE_PHASE_BANK — Fase Kehidupan per Elemen Dominan
# ============================================================
# Ketika sebuah fase Da Yun (大運) didominasi elemen tertentu,
# narasi ini menjelaskan karakteristik fase tersebut.
# ============================================================

LIFE_PHASE_BANK = {
    "kayu": {
        "phase_name": "",        # Nama fase, cth: "Fase Pertumbuhan & Ekspansi"
        "description": "",       # 2-3 kalimat tentang karakteristik fase
        "advice": "",            # 1-2 kalimat saran untuk fase ini
    },
    "api": {"phase_name": "", "description": "", "advice": ""},
    "tanah": {"phase_name": "", "description": "", "advice": ""},
    "logam": {"phase_name": "", "description": "", "advice": ""},
    "air": {"phase_name": "", "description": "", "advice": ""},
}


# ============================================================
# 10. IDENTITY_BANK — Identitas & Profil per 12 Shio
# ============================================================
# Key: shio key (tikus, kerbau, macan, ...)
# Berisi 15 konten unik identitas Shio yang sebelumnya ada di
# profile bank — sekarang terintegrasi dalam Ming Li.
#
# Digunakan sebagai data enrichment pada hasil Ba Zi:
# setelah chart dihitung, data Shio user ditambahkan dari sini.
# ============================================================

IDENTITY_BANK = {
    "tikus": {
        "icon": "🐀",
        "earthly_branch": "",          # Cabang Bumi, cth: "Zi (子)"
        "fixed_element": "",           # Elemen tetap Shio, cth: "Air"
        "traits_positive": [],         # 5-6 sifat positif
        "traits_negative": [],         # 4-5 sifat negatif
        "personality_long": "",        # 2 paragraf deskripsi kepribadian mendalam
        "green_flags": [],             # 5 green flags hubungan (Gen-Z style)
        "red_flags": [],               # 5 red flags hubungan (Gen-Z style)
        "alter_ego": {
            # Alter ego per 5 elemen — kepribadian berbeda tiap variasi elemen
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [],           # 4-5 tokoh terkenal dengan tahun lahir
        "lucky_flowers": [],           # 2-3 bunga keberuntungan
        "unlucky_colors": [],          # 2-3 warna sial
        "unlucky_numbers": [],         # 2-3 angka sial
        "best_months": [],             # 2-3 bulan terbaik (angka)
        "worst_months": [],            # 2-3 bulan terburuk (angka)
        "spirit_advice": "",           # 1 paragraf nasihat spiritual
    },
    "kerbau": {
        "icon": "🐂",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "macan": {
        "icon": "🐅",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "kelinci": {
        "icon": "🐇",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "naga": {
        "icon": "🐉",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "ular": {
        "icon": "🐍",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "kuda": {
        "icon": "🐎",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "kambing": {
        "icon": "🐐",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "monyet": {
        "icon": "🐒",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "ayam": {
        "icon": "🐓",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "anjing": {
        "icon": "🐕",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
    "babi": {
        "icon": "🐖",
        "earthly_branch": "", "fixed_element": "",
        "traits_positive": [], "traits_negative": [],
        "personality_long": "",
        "green_flags": [], "red_flags": [],
        "alter_ego": {
            "kayu": {"title": "", "description": ""},
            "api": {"title": "", "description": ""},
            "tanah": {"title": "", "description": ""},
            "logam": {"title": "", "description": ""},
            "air": {"title": "", "description": ""},
        },
        "famous_people": [], "lucky_flowers": [],
        "unlucky_colors": [], "unlucky_numbers": [],
        "best_months": [], "worst_months": [],
        "spirit_advice": "",
    },
}
