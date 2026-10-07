PANCASUDA = {
    "name": "Pancasuda",
    "divisor": 5,
    "results": [
        {"name": "Pati", "arti": "rawan kehilangan, termasuk kehilangan pemasukan", "tone": "berat"},
        {"name": "Sri", "arti": "rezeki lancar dan melimpah", "tone": "baik"},
        {"name": "Lungguh", "arti": "mendapat derajat atau kedudukan", "tone": "baik"},
        {"name": "Gedhong", "arti": "harta benda bertambah", "tone": "baik"},
        {"name": "Lara", "arti": "rawan sakit dan kesusahan", "tone": "berat"},
    ],
    "source": (
        "Pancasuda, neptu weton lahir ditambah neptu hari lalu dibagi 5 (detikJateng, merujuk Miswanto, "
        "Wariga dan Primbon, dan Ranoewidjojo, Primbon Masa Kini)"
    ),
}

HAJAT = {
    "nikah": {
        "label": "Nikah",
        "icon": "fa-ring",
        "inti": "Untuk nikah, hari pantangan disaring dulu, lalu sasi Jawa ikut dilihat. Ada sasi yang dihindari dan ada yang dipercaya membawa berkah.",
        "saran": "Anggap hasilnya daftar pendek, lalu obrolkan bareng keluarga besar. Tiap daerah bisa punya pakem nikah sendiri.",
        "pantangan": ["taliwangke", "samparwangke", "sarik_agung", "kala_dite"],
        "sasi_hindari": {
            "sura": "Nikah di sasi Sura dipercaya bikin rumah tangga sering cekcok dan hidup terasa berat.",
            "mulud": "Sasi Mulud dihindari karena dipercaya membawa duka bagi salah satu pasangan.",
            "pasa": "Sasi Pasa atau bulan puasa dihindari karena dipercaya membawa musibah besar bagi pasangan.",
            "sela": "Sasi Sela (Dulkangidah) dipercaya bikin pasangan sering sakit dan berselisih dengan kerabat.",
        },
        "sasi_baik": {
            "jumadilakir": "Sasi Jumadilakir dipercaya membawa rezeki dan harta yang berlimpah.",
            "rejeb": "Sasi Rejeb dipercaya membawa berkah, keselamatan, dan banyak keturunan.",
            "ruwah": "Sasi Ruwah dipercaya membawa keselamatan dan kedamaian dalam rumah tangga.",
            "besar": "Sasi Besar dipercaya baik untuk hajat apa pun karena membawa banyak rezeki dan kebahagiaan.",
        },
        "petung": False,
        "source": (
            "Sasi nikah menurut Primbon Betaljemur Adammakna (Intisari) dan Kitab Primbon Lengkap serta "
            "Primbon Masa Kini (detikJogja)"
        ),
    },
    "pindah": {
        "label": "Pindah rumah",
        "icon": "fa-house-chimney",
        "inti": "Untuk pindah rumah, hari pantangan disaring dulu. Kalau weton lahirmu diisi, petung Pancasuda ikut menilai tiap hari.",
        "saran": "Hari pindahan tidak harus hari angkut semua barang. Banyak keluarga cukup membawa barang simbolis dulu di hari yang dipilih.",
        "pantangan": ["taliwangke", "samparwangke", "sarik_agung", "kala_dite"],
        "sasi_hindari": {},
        "sasi_baik": {},
        "petung": True,
        "source": "Hari pindah rumah dengan Pancasuda dan catatan pantangan primbon (detikJateng)",
    },
    "bangun_rumah": {
        "label": "Bangun rumah",
        "icon": "fa-trowel-bricks",
        "inti": "Untuk mulai bangun rumah, hari pantangan disaring dulu, lalu sasi Jawa ikut dilihat. Ada tiga sasi yang dipercaya paling pas.",
        "saran": "Hari baik cuma pembuka. Pastikan izin bangunan, anggaran, dan tukang sudah siap sebelum peletakan batu pertama.",
        "pantangan": ["taliwangke", "samparwangke", "sarik_agung", "kala_dite"],
        "sasi_hindari": {},
        "sasi_baik": {
            "bakdamulud": "Sasi Bakdamulud dipercaya mendatangkan rezeki lancar dan kedamaian bagi penghuni rumah.",
            "ruwah": "Sasi Ruwah dipercaya membawa kemakmuran dan derajat yang terangkat bagi rumah yang dibangun.",
            "besar": "Sasi Besar dipercaya paling baik untuk membangun rumah karena membawa kebahagiaan, keselamatan, dan rezeki.",
        },
        "petung": False,
        "source": "Sasi baik membangun rumah menurut primbon Jawa (BorobudurNews dan Liputan6)",
    },
    "usaha": {
        "label": "Buka usaha",
        "icon": "fa-store",
        "inti": "Untuk buka usaha, hari pantangan disaring dulu. Kalau weton lahir pemilik diisi, Pancasuda ikut menilai tiap hari.",
        "saran": "Hari baik membantu mantap melangkah, tapi riset pasar dan arus kas tetap penentu utama. Siapkan keduanya sebelum launching.",
        "pantangan": ["samparwangke", "sarik_agung", "dhendhan_kukudan"],
        "sasi_hindari": {},
        "sasi_baik": {},
        "petung": True,
        "source": "Hari memulai usaha dengan Pancasuda dari weton pemilik (detikJateng)",
    },
    "transaksi": {
        "label": "Transaksi besar",
        "icon": "fa-handshake",
        "inti": "Untuk transaksi besar, primbon yang kami pakai hanya menyaring hari pantangan, termasuk Dhendhan Kukudan yang terkait utang.",
        "saran": "Hari bebas pantangan bukan jaminan untung. Cek ulang kontrak, cicilan, dan anggaranmu sebelum tanda tangan.",
        "pantangan": ["dhendhan_kukudan", "samparwangke", "sarik_agung"],
        "sasi_hindari": {},
        "sasi_baik": {},
        "petung": False,
        "source": "Catatan pantangan primbon untuk transaksi dan hajat penting",
    },
}

DEFAULT_HAJAT = "nikah"

DINA_TONE_LABELS = {
    "baik": "Paling pas",
    "aman": "Bebas pantangan",
    "campur": "Kurang disarankan",
    "berat": "Sebaiknya dihindari",
}

DINA_NOTE = (
    "Hari Jawa berganti saat maghrib. Kalau acaramu mulai malam, cek juga weton hari berikutnya di kalender."
)

DINA_PETUNG_HINT = "Isi weton lahir supaya petung Pancasuda ikut menilai tiap hari."

DINA_DISCLAIMER = (
    "Hasil ini merangkum aturan primbon yang sumbernya bisa ditelusuri, bukan jaminan acara lancar. "
    "Pakai sebagai referensi budaya, keputusan tetap di tanganmu."
)
