HUB_FEATURES = [
    {
        "key": "harian",
        "short": "Harian",
        "endpoint": "tarot.tarot_daily_page",
        "icon": "fa-sun",
        "title": "Kartu Harian",
        "text": "Satu kartu untuk menemani harimu. Kartunya tetap sama sampai besok, jadi kamu bisa kembali membacanya kapan saja.",
    },
    {
        "key": "bacaan",
        "short": "Bacaan",
        "endpoint": "tarot.tarot_reading_page",
        "icon": "fa-layer-group",
        "title": "Bacaan Tarot",
        "text": "Ajukan pertanyaan, pilih spread satu kartu, tiga kartu, atau Celtic Cross, lalu ambil sendiri kartumu dari dek.",
    },
    {
        "key": "yatidak",
        "short": "Ya/Tidak",
        "endpoint": "tarot.tarot_answer_page",
        "icon": "fa-circle-question",
        "title": "Ya atau Tidak",
        "text": "Untuk pertanyaan tertutup. Satu kartu menjawab ya, tidak, atau belum pasti, lengkap dengan alasannya.",
    },
    {
        "key": "hubungan",
        "short": "Hubungan",
        "endpoint": "tarot.tarot_relationship_page",
        "icon": "fa-heart",
        "title": "Bacaan Hubungan",
        "text": "Tujuh kartu untuk membaca posisimu, posisi dia, apa yang kalian butuhkan, dan ke mana hubungan ini bergerak.",
    },
    {
        "key": "lahir",
        "short": "Lahir",
        "endpoint": "tarot.tarot_birth_page",
        "icon": "fa-star",
        "title": "Kartu Lahir",
        "text": "Tanggal lahirmu dihitung menjadi kartu kepribadian dan kartu jiwa, ditambah kartu tahun yang sedang kamu jalani.",
    },
    {
        "key": "arcani",
        "short": "Kartu",
        "endpoint": "tarot.tarot_cards_page",
        "icon": "fa-book-open",
        "title": "Ensiklopedia Kartu",
        "text": "Ke-78 kartu Rider-Waite: simbol, korespondensi astrologi, serta makna tegak dan terbalik untuk tiap topik.",
    },
]

SUITS = {
    "wands": {
        "name": "Wands",
        "name_id": "Tongkat",
        "name_it": "Bastoni",
        "element": "api",
        "icon": "fa-fire",
        "domain": "semangat, ambisi, kreativitas, dan dorongan untuk bertindak",
    },
    "cups": {
        "name": "Cups",
        "name_id": "Piala",
        "name_it": "Coppe",
        "element": "air",
        "icon": "fa-droplet",
        "domain": "perasaan, hubungan, intuisi, dan kehidupan batin",
    },
    "swords": {
        "name": "Swords",
        "name_id": "Pedang",
        "name_it": "Spade",
        "element": "udara",
        "icon": "fa-wind",
        "domain": "pikiran, keputusan, komunikasi, dan konflik",
    },
    "pentacles": {
        "name": "Pentacles",
        "name_id": "Pentakel",
        "name_it": "Denari",
        "element": "tanah",
        "icon": "fa-mountain",
        "domain": "uang, pekerjaan, tubuh, dan hal-hal yang nyata",
    },
}

ELEMENT_LABELS = {
    "api": "Api",
    "air": "Air",
    "udara": "Udara",
    "tanah": "Tanah",
}

RANKS = [
    {"key": "ace", "number": 1, "name": "Ace", "name_id": "As"},
    {"key": "two", "number": 2, "name": "Two", "name_id": "Dua"},
    {"key": "three", "number": 3, "name": "Three", "name_id": "Tiga"},
    {"key": "four", "number": 4, "name": "Four", "name_id": "Empat"},
    {"key": "five", "number": 5, "name": "Five", "name_id": "Lima"},
    {"key": "six", "number": 6, "name": "Six", "name_id": "Enam"},
    {"key": "seven", "number": 7, "name": "Seven", "name_id": "Tujuh"},
    {"key": "eight", "number": 8, "name": "Eight", "name_id": "Delapan"},
    {"key": "nine", "number": 9, "name": "Nine", "name_id": "Sembilan"},
    {"key": "ten", "number": 10, "name": "Ten", "name_id": "Sepuluh"},
    {"key": "page", "number": 11, "name": "Page", "name_id": "Pelayan"},
    {"key": "knight", "number": 12, "name": "Knight", "name_id": "Ksatria"},
    {"key": "queen", "number": 13, "name": "Queen", "name_id": "Ratu"},
    {"key": "king", "number": 14, "name": "King", "name_id": "Raja"},
]

COURT_RANKS = ("page", "knight", "queen", "king")

TOPICS = {
    "umum": {"label": "Umum", "icon": "fa-compass"},
    "cinta": {"label": "Cinta", "icon": "fa-heart"},
    "karier": {"label": "Karier", "icon": "fa-briefcase"},
    "keuangan": {"label": "Keuangan", "icon": "fa-coins"},
}

DEFAULT_TOPIC = "umum"

SPREADS = {
    "satu": {
        "name": "Satu Kartu",
        "short": "1 kartu",
        "text": "Satu kartu untuk jawaban yang ringkas dan langsung.",
        "positions": [
            {"key": "inti", "label": "Pesan utama", "prompt": "Inti jawaban atas pertanyaanmu."},
        ],
    },
    "tiga_waktu": {
        "name": "Lalu, Kini, Nanti",
        "short": "3 kartu",
        "text": "Tiga kartu untuk melihat asal situasi, keadaannya sekarang, dan arahnya.",
        "positions": [
            {"key": "lalu", "label": "Masa lalu", "prompt": "Hal yang membentuk situasimu sampai sekarang."},
            {"key": "kini", "label": "Saat ini", "prompt": "Keadaan yang sedang kamu hadapi."},
            {"key": "nanti", "label": "Arah ke depan", "prompt": "Ke mana situasi ini cenderung bergerak bila tidak ada yang berubah."},
        ],
    },
    "tiga_langkah": {
        "name": "Situasi, Tindakan, Hasil",
        "short": "3 kartu",
        "text": "Tiga kartu yang praktis: gambaran situasi, langkah yang membantu, dan hasilnya.",
        "positions": [
            {"key": "situasi", "label": "Situasi", "prompt": "Gambaran jujur tentang posisimu sekarang."},
            {"key": "tindakan", "label": "Tindakan", "prompt": "Langkah yang paling membantu untuk diambil."},
            {"key": "hasil", "label": "Hasil", "prompt": "Kemungkinan hasil bila langkah itu dijalankan."},
        ],
    },
    "celtic": {
        "name": "Celtic Cross",
        "short": "10 kartu",
        "text": "Sepuluh kartu menurut susunan Waite untuk persoalan yang berlapis.",
        "positions": [
            {"key": "inti", "label": "Inti situasi", "prompt": "Apa yang sedang menaungimu, pusat dari pertanyaan ini."},
            {"key": "silang", "label": "Yang menyilang", "prompt": "Kekuatan yang menghalangi atau justru menguji situasi ini."},
            {"key": "mahkota", "label": "Mahkota", "prompt": "Hal terbaik yang bisa dicapai, atau yang sedang kamu sadari dan tuju."},
            {"key": "dasar", "label": "Dasar", "prompt": "Akar persoalan, fondasi yang sudah terbentuk dan belum tentu kamu sadari."},
            {"key": "belakang", "label": "Di belakang", "prompt": "Pengaruh yang baru saja berlalu atau sedang memudar."},
            {"key": "depan", "label": "Di depan", "prompt": "Pengaruh yang akan masuk dalam waktu dekat."},
            {"key": "diri", "label": "Dirimu", "prompt": "Sikap dan posisimu sendiri dalam situasi ini."},
            {"key": "lingkungan", "label": "Lingkungan", "prompt": "Orang-orang dan suasana di sekitarmu, termasuk cara mereka memandangmu."},
            {"key": "harapan", "label": "Harapan dan kekhawatiran", "prompt": "Apa yang kamu harapkan, dan sering kali apa yang diam-diam kamu takutkan."},
            {"key": "hasil", "label": "Hasil", "prompt": "Arah akhir bila semua pengaruh di atas terus berjalan."},
        ],
    },
}

READING_SPREADS = ("satu", "tiga_waktu", "tiga_langkah", "celtic")
DEFAULT_SPREAD = "tiga_waktu"

RELATIONSHIP_POSITIONS = [
    {"key": "kamu", "label": "Kamu", "prompt": "Posisi dan perasaanmu dalam hubungan ini."},
    {"key": "dia", "label": "{Dia}", "prompt": "Posisi dan perasaan {dia}, sejauh yang bisa terbaca."},
    {"key": "hubungan", "label": "Hubungan saat ini", "prompt": "Keadaan hubungan kalian sekarang."},
    {"key": "butuh_kamu", "label": "Yang kamu butuhkan", "prompt": "Hal yang kamu perlukan agar merasa aman dan dihargai."},
    {"key": "butuh_dia", "label": "Yang {dia} butuhkan", "prompt": "Hal yang {dia} perlukan dari hubungan ini."},
    {"key": "tantangan", "label": "Tantangan", "prompt": "Hal yang perlu kalian hadapi bersama."},
    {"key": "arah", "label": "Arah ke depan", "prompt": "Ke mana hubungan ini cenderung bergerak."},
]

ANSWERS = {
    "ya": {"label": "Ya", "text": "Kartu ini condong ke jawaban ya."},
    "tidak": {"label": "Tidak", "text": "Kartu ini condong ke jawaban tidak, setidaknya dalam keadaan sekarang."},
    "belum": {"label": "Belum pasti", "text": "Kartu ini belum memberi jawaban tegas. Ada hal yang masih perlu matang atau perlu kamu cermati dulu."},
}

TONES = {
    "terang": "Mendukung",
    "netral": "Perlu dicermati",
    "berat": "Menantang",
}

ORIENTATION_LABELS = {
    False: "Tegak",
    True: "Terbalik",
}

SOURCES = {
    "waite": "A. E. Waite, The Pictorial Key to the Tarot (1910)",
    "golden_dawn": "Hermetic Order of the Golden Dawn, Book T (korespondensi astrologi dan huruf Ibrani)",
    "pollack": "Rachel Pollack, Seventy-Eight Degrees of Wisdom (1980), rujukan nuansa makna",
    "greer": "Mary K. Greer, Who Are You in the Tarot? (2011), metode kartu lahir",
    "deck": "Dek Rider-Waite 1909, ilustrasi Pamela Colman Smith (domain publik)",
}

GLOSSARY = {
    "arcana_mayor": "Dua puluh dua kartu bernomor 0 sampai XXI yang menggambarkan pelajaran dan peristiwa besar dalam hidup.",
    "arcana_minor": "Lima puluh enam kartu dalam empat suit yang menggambarkan urusan sehari-hari, dari perasaan sampai pekerjaan.",
    "kartu_istana": "Page, Knight, Queen, dan King. Kartu ini sering mewakili orang lain, peran, atau sisi tertentu dari dirimu.",
    "terbalik": "Kartu yang muncul terbalik membawa energi yang tertahan, tertunda, berlebihan, atau sedang bekerja di dalam diri.",
    "spread": "Susunan posisi kartu. Setiap posisi memberi konteks, sehingga satu kartu bisa terbaca berbeda di posisi yang berbeda.",
    "korespondensi": "Pasangan astrologi dan huruf Ibrani untuk tiap kartu menurut tradisi Golden Dawn, yang juga dipakai Waite.",
    "kartu_lahir": "Kartu Arcana Mayor yang dihitung dari tanggal lahir. Kartu kepribadian tampak di luar, kartu jiwa bekerja di dalam.",
}

DISCLAIMER = "Tarot di sini dipakai sebagai alat refleksi, bukan ramalan pasti. Untuk urusan kesehatan, hukum, atau keuangan yang serius, tetap konsultasikan dengan ahlinya."

DAILY_NOTE = "Kartu harian dipilih sekali untuk setiap perangkat per hari (WIB). Kalau kamu membukanya lagi hari ini, kartunya tetap sama."

DRAW_NOTE = "Dek dikocok ulang setiap kali kamu membuka bacaan. Pilih kartu yang paling menarik perhatianmu, tidak perlu dipikir terlalu lama."

QUESTION_HINT = "Pertanyaan terbuka biasanya menghasilkan bacaan yang lebih jernih, misalnya \"Apa yang perlu kupahami tentang pekerjaanku sekarang?\""

YESNO_HINT = "Ajukan satu pertanyaan tertutup yang jawabannya ya atau tidak. Hindari menanyakan hal yang sama berulang kali di hari yang sama."

BIRTH_NOTE = "Dihitung dengan metode Mary K. Greer: bulan, tanggal, dan tahun lahir dijumlahkan, lalu digitnya dijumlahkan lagi sampai bernilai 22 atau kurang."

QUESTION_MAX_LENGTH = 200
NAME_MAX_LENGTH = 24
