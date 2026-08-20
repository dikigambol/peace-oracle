# ============================================================
# 🔮 SHIO FORTUNE BANK — Bank Ramalan per Kategori
# ============================================================
# STATUS: 📝 SKELETON — Siap diisi konten
#
# FUNGSI: Menggantikan karir_pool, keuangan_pool, asmara_pool,
#         kesehatan_pool di generate_shio_fortune() yang saat ini
#         cuma punya 3 variasi template per kategori.
#
# TARGET: 30-50 ramalan unik per Shio × 4 kategori = 1.440–2.400 entri
#
# CARA MENGISI:
# Tulis ramalan yang spesifik untuk karakter masing-masing Shio,
# bukan template generik. Bisa ditambahkan field "mood" untuk
# mencocokkan dengan elemen user.
# ============================================================

SHIO_FORTUNE_BANK = {
    "tikus": {
        "karir": [
            # Contoh format — isi minimal 30 entri per Shio
            {
                "id": 1,
                "text": "Insting bisnis Tikus lagi tajam! Ada peluang kolaborasi mengejutkan dari orang yang tidak terduga. Jangan ragu bilang 'ya' hari ini.",
                "mood": "optimis"
            },
            {
                "id": 2,
                "text": "Hati-hati dengan rekan kerja yang terlalu manis. Sifat cerdik Tikus bisa mendeteksi satu orang di sekitarmu yang menyimpan agenda tersembunyi.",
                "mood": "waspada"
            },
            {
                "id": 3,
                "text": "Kemampuan adaptasimu sedang diperlukan di tempat kerja. Perubahan mendadak justru menjadi panggung untukmu bersinar.",
                "mood": "optimis"
            },
            # TODO: Tambahkan 27-47 entri lagi
        ],
        "keuangan": [
            {
                "id": 1,
                "text": "Ada potensi rezeki dari investasi atau tabungan lama. Tikus yang cermat keuangannya akan merasakan buahnya hari ini.",
                "mood": "optimis"
            },
            {
                "id": 2,
                "text": "Jangan tergoda diskon besar-besaran. Sifat oportunis Tikus bisa berubah jadi pemborosan kalau gak direm.",
                "mood": "waspada"
            },
            {
                "id": 3,
                "text": "Hari yang bagus untuk menyusun ulang budget bulanan. Otak analitis Tikus sedang tajam untuk kalkulasi finansial.",
                "mood": "netral"
            },
            # TODO: Tambahkan 27-47 entri lagi
        ],
        "asmara": [
            {
                "id": 1,
                "text": "Pesona cerdik dan humoris Tikus sedang bersinar hari ini. Gebetan atau pasangan bakal makin tertarik sama cara kamu berkomunikasi.",
                "mood": "optimis"
            },
            {
                "id": 2,
                "text": "Jangan terlalu banyak menghitung untung-rugi dalam hubungan. Cinta butuh ketulusan, bukan spreadsheet.",
                "mood": "waspada"
            },
            {
                "id": 3,
                "text": "Momen romantis muncul dari obrolan santai yang tak terduga. Buka hatimu untuk koneksi baru.",
                "mood": "optimis"
            },
            # TODO: Tambahkan 27-47 entri lagi
        ],
        "kesehatan": [
            {
                "id": 1,
                "text": "Pikiran Tikus yang selalu aktif butuh istirahat. Kurangi screen time malam ini dan ganti dengan meditasi ringan.",
                "mood": "netral"
            },
            {
                "id": 2,
                "text": "Pola makan Tikus yang sering gak teratur mulai menunjukkan efeknya. Mulai sarapan teratur mulai besok!",
                "mood": "waspada"
            },
            {
                "id": 3,
                "text": "Energi fisik sedang prima! Hari yang bagus untuk olahraga kardio atau jalan pagi sambil brainstorming.",
                "mood": "optimis"
            },
            # TODO: Tambahkan 27-47 entri lagi
        ]
    },
    "kerbau": {
        "karir": [
            # TODO: Isi 30-50 entri
        ],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "macan": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "kelinci": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "naga": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "ular": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "kuda": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "kambing": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "monyet": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "ayam": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "anjing": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    },
    "babi": {
        "karir": [],
        "keuangan": [],
        "asmara": [],
        "kesehatan": []
    }
}
