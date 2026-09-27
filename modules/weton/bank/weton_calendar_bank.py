HARI_ISTIMEWA = {
    "anggara_kasih": {
        "name": "Anggara Kasih",
        "hari": "selasa",
        "pasaran": "kliwon",
        "inti": "Selasa Kliwon disebut Anggara Kasih, hari yang dianggap istimewa untuk doa, perenungan, dan merawat rasa sayang.",
        "saran": "Pakai hari ini buat me-time yang bermakna: rapikan pikiran, kirim doa, atau sapa keluarga yang lama nggak kamu hubungi.",
        "source": "Wikipedia bahasa Indonesia (Kliwon, merujuk Primbon Betaljemur Adammakna) dan Kawruh.com",
    },
    "jumat_kliwon": {
        "name": "Jumat Kliwon",
        "hari": "jumat",
        "pasaran": "kliwon",
        "inti": "Jumat Kliwon dianggap hari keramat. Malamnya dimulai Kamis setelah maghrib dan sering diisi ziarah atau doa keselamatan.",
        "saran": "Cocok buat ziarah atau hening sebentar. Kalau kamu nggak menjalankan tradisinya, cukup hormati orang yang menjalankan.",
        "source": "Wikipedia bahasa Indonesia (Kliwon, merujuk Primbon Betaljemur Adammakna) dan Kawruh.com",
    },
    "satu_sura": {
        "name": "1 Sura",
        "hari": None,
        "pasaran": None,
        "inti": "1 Sura adalah tahun baru Jawa. Malam 1 Sura jatuh sehari sebelumnya setelah maghrib, diisi tirakatan atau kirab pusaka.",
        "saran": "Momen pas buat refleksi setahun ke belakang. Tulis satu hal yang mau kamu lepas dan satu hal yang mau kamu mulai.",
        "source": "Aritmetika kalender Sultan Agungan, Wikipedia bahasa Indonesia (Kliwon), dan Kawruh.com",
    },
}

PANTANGAN = {
    "taliwangke": {
        "name": "Taliwangke",
        "arti": "tali mayat",
        "inti": "Primbon mencatat Taliwangke sebagai hari yang biasanya dihindari untuk hajatan besar seperti nikahan atau pindah rumah.",
        "saran": "Kalau kamu atau keluarga memegang tradisi ini, geser acara besar ke hari lain. Urusan harian tetap jalan seperti biasa.",
    },
    "samparwangke": {
        "name": "Samparwangke",
        "arti": "tersandung mayat",
        "inti": "Samparwangke dibaca sebagai hari yang rawan kesulitan tak terduga, jadi primbon menyarankan tidak memulai hajat penting.",
        "saran": "Hari yang pas buat ngerjain yang rutin dulu. Rencana besar bisa disiapkan hari ini, eksekusinya pilih hari lain.",
    },
    "sarik_agung": {
        "name": "Sarik Agung",
        "arti": "pantangan besar",
        "inti": "Sarik Agung dicatat sebagai pantangan besar. Wataknya dikaitkan dengan susahnya bergaul dan urusan yang gampang tersendat.",
        "saran": "Kalau harus ketemu orang baru hari ini, siapkan diri lebih matang dan dengarkan dulu sebelum menanggapi.",
    },
    "kala_dite": {
        "name": "Kala Dite",
        "arti": "bahaya yang mendiami hari Minggu",
        "inti": "Kala Dite adalah hari Minggu tertentu yang menurut primbon penuh halangan, jadi tidak dipakai untuk hajatan.",
        "saran": "Minggu ini cocok buat istirahat dan beberes. Acara besar keluarga lebih aman dijadwalkan di Minggu berikutnya.",
    },
    "dhendhan_kukudan": {
        "name": "Dhendhan Kukudan",
        "arti": "denda yang bisa bikin bangkrut",
        "inti": "Dhendhan Kukudan dikaitkan dengan denda dan urusan utang yang bisa menguras dompet, jadi dihindari untuk transaksi besar.",
        "saran": "Tahan dulu belanja besar atau tanda tangan pinjaman. Cek ulang tagihan dan anggaranmu, itu jauh lebih berguna hari ini.",
    },
}

PANTANGAN_WUKU = [
    ("taliwangke", "landep", "rabu", "pahing"),
    ("taliwangke", "warigalit", "kamis", "pon"),
    ("taliwangke", "kuningan", "jumat", "wage"),
    ("taliwangke", "kuruwelut", "sabtu", "kliwon"),
    ("taliwangke", "wuye", "senin", "kliwon"),
    ("taliwangke", "wayang", "selasa", "legi"),
    ("samparwangke", "sinta", "senin", "pon"),
    ("samparwangke", "warigalit", "senin", "kliwon"),
    ("samparwangke", "langkir", "senin", "pahing"),
    ("samparwangke", "tambir", "senin", "wage"),
    ("samparwangke", "bala", "senin", "legi"),
    ("sarik_agung", "kurantil", "rabu", None),
    ("sarik_agung", "galungan", "rabu", None),
    ("sarik_agung", "marakeh", "rabu", None),
    ("sarik_agung", "bala", "rabu", None),
    ("kala_dite", "warigagung", "minggu", None),
    ("kala_dite", "kuruwelut", "minggu", None),
    ("kala_dite", "dukut", "minggu", None),
    ("dhendhan_kukudan", "galungan", "minggu", None),
    ("dhendhan_kukudan", "galungan", "senin", None),
    ("dhendhan_kukudan", "galungan", "selasa", None),
]

TALIWANGKE_SASI = {
    "sura": ("rabu", "pahing"),
    "sapar": ("kamis", "pon"),
    "mulud": ("jumat", "wage"),
    "bakdamulud": ("sabtu", "kliwon"),
    "jumadilawal": ("senin", "kliwon"),
    "jumadilakir": ("selasa", "legi"),
    "rejeb": ("rabu", "pahing"),
    "ruwah": ("kamis", "pon"),
    "pasa": ("jumat", "wage"),
    "sawal": ("sabtu", "kliwon"),
    "sela": ("senin", "kliwon"),
    "besar": ("selasa", "legi"),
}

KEBLAT_PASARAN = {
    "legi": {"arah": "Timur", "warna": "Putih"},
    "pahing": {"arah": "Selatan", "warna": "Merah"},
    "pon": {"arah": "Barat", "warna": "Kuning"},
    "wage": {"arah": "Utara", "warna": "Hitam"},
    "kliwon": {"arah": "Tengah", "warna": "Abu-abu (sebagian sumber: manca warna)"},
}

CALENDAR_SOURCES = {
    "istimewa": "Wikipedia bahasa Indonesia (Kliwon, merujuk Primbon Betaljemur Adammakna) dan Kawruh.com",
    "pantangan_wuku": "Primbon Jawa: Taliwangke, Samparwangke, Sarik Agung, Kala Dite, dan Dhendhan Kukudan menurut wuku",
    "pantangan_sasi": "Primbon Betaljemur Adammakna: Taliwangke menurut sasi",
    "keblat": "Wikipedia bahasa Indonesia (Legi, Paing, Pon, Wage, Kliwon), merujuk Primbon Betaljemur Adammakna",
}

CALENDAR_NOTE = (
    "Weton di kalender ini berlaku untuk siang hari. Setelah maghrib, hitungan Jawa sudah masuk ke hari berikutnya."
)

CALENDAR_DISCLAIMER = (
    "Hari istimewa dan hari pantangan dicatat dari tradisi primbon, bukan ramalan pasti. "
    "Pakai sebagai referensi budaya, keputusan tetap di tanganmu."
)

WETONAN_NOTE = (
    "Wetonan adalah hari saat weton lahirmu terulang, tiap 35 hari. Banyak keluarga Jawa memakainya untuk selamatan atau puasa weton."
)
