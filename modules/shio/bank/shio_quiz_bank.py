RELATION_LENS = {
    "asmara": {
        "label": "Asmara",
        "narrative_field": "asmara",
        "narrative_title": "Asmara",
        "narrative_icon": "fa-heart",
        "day_layer_title": "Lapisan Pilar Hari — Pencocokan Jodoh (合婚)",
        "supply_label": "Memasok pasangan",
        "burden_label": "Membebani pasangan",
        "romantic": True,
    },
    "pertemanan": {
        "label": "Pertemanan",
        "narrative_field": "persahabatan",
        "narrative_title": "Pertemanan",
        "narrative_icon": "fa-user-group",
        "day_layer_title": "Lapisan Pilar Hari — Watak Sehari-hari",
        "supply_label": "Menguatkan temannya",
        "burden_label": "Menguras temannya",
        "romantic": False,
    },
    "kerja": {
        "label": "Rekan Kerja",
        "narrative_field": "bisnis",
        "narrative_title": "Kerja Sama",
        "narrative_icon": "fa-briefcase",
        "day_layer_title": "Lapisan Pilar Hari — Watak Sehari-hari",
        "supply_label": "Menguatkan rekannya",
        "burden_label": "Menguras rekannya",
        "romantic": False,
    },
}

NEUTRAL_RELATION_LABELS = {
    "liu_he": "Liu He (Enam Harmoni)",
}

NEUTRAL_BAZI_LAYER_NOTE = (
    "Lapisan ini dihitung dari pilar hari (日柱) kedua tanggal, bukan dari "
    "shionya. Pilar hari menggambarkan watak sehari-hari, jadi di sinilah "
    "cara kalian bergaul dan bekerja sama paling terbaca. Hitungannya memakai "
    "tiga pilar — sah dibaca, tapi lapisan jam tidak ikut."
)

NEUTRAL_DAY_PILLAR_RELATION_BANK = {
    "liu_he": "Cabang hari kalian berpasangan enam harmoni (六合). Ritme sehari-hari kalian saling mengunci, jadi kerja sama terasa lancar tanpa banyak diatur.",
    "san_he": "Cabang hari kalian satu kelompok tiga harmoni (三合). Kebiasaan harian kalian menarik ke arah yang sama, jadi gampang sepakat soal hal kecil.",
    "ben_ming": "Cabang hari kalian sama. Kalian mengenali diri sendiri di satu sama lain — nyaman, tapi jarang ada yang menantang.",
    "zi_xing": "Cabang hari kalian sama dan termasuk yang menghukum diri. Pola yang sama berulang di dua orang sekaligus.",
    "netral": "Cabang hari kalian tidak berelasi khusus. Kebiasaan harian kalian netral: tidak saling menarik, tidak saling menolak.",
    "liu_po": "Cabang hari kalian saling merusak (六破). Kesepakatan di antara kalian gampang berubah bentuk; tulis yang penting, jangan andalkan ingatan.",
    "liu_hai": "Cabang hari kalian saling menyakiti (六害). Yang melukai biasanya hal kecil yang dianggap sepele oleh yang melakukannya.",
    "xiang_xing": "Cabang hari kalian saling menghukum (相刑). Kebiasaan harian kalian saling menggerus — biasanya soal siapa yang mengalah dan seberapa sering.",
    "chong": "Cabang hari kalian berseberangan lurus (六冲). Ritme sehari-hari kalian berhadapan langsung, jadi kalian butuh aturan main yang jelas sejak awal.",
}

NEUTRAL_USEFUL_GOD_NOTES = {
    "saling_memasok": "Elemen inti {a} termasuk yang dibutuhkan {b}, dan sebaliknya. Ini hasil terbaik untuk kerja sama apa pun — kalian saling menambal kekurangan, bukan cuma cocok di permukaan.",
    "saling_menguras": "Elemen inti kalian masing-masing justru termasuk yang membebani yang lain. Secara struktur, waktu bersama menuntut tenaga ekstra dari keduanya.",
}

NEUTRAL_COUPLE_STARS = {
    "tao_hua_both": {
        "title": "Dua-duanya Punya Daya Tarik Sosial",
        "note": "Kalian berdua gampang menarik perhatian orang di sekitar. Itu modal jaringan yang besar, asal tidak berebut sorotan di ruangan yang sama.",
    },
    "tao_hua_one": {
        "title": "Satu Pihak Punya Daya Tarik Sosial",
        "note": "Satu dari kalian lebih sering jadi pusat perhatian. Bukan salahnya, tapi yang lain perlu tetap merasa dilihat.",
    },
    "solitude_one": {
        "title": "Satu Pihak Bawa Bintang Kesendirian",
        "note": "Satu dari kalian cenderung menarik diri saat sedang berat. Itu bukan penolakan, dan yang lain perlu tahu itu sejak awal.",
    },
}

PAIR_QUIZ_QUESTIONS = [
    {
        "id": "rencana",
        "question": "Ada ajakan dadakan di akhir pekan. Biasanya kamu...",
        "options": [
            "Langsung ikut, justru seru karena dadakan",
            "Ikut kalau jadwal masih kosong",
            "Perlu dikabari minimal sehari sebelumnya",
            "Lebih suka semua dijadwalkan dari jauh hari",
        ],
    },
    {
        "id": "masalah",
        "question": "Ada masalah di antara kalian. Cara kamu menyelesaikannya...",
        "options": [
            "Dibahas saat itu juga sampai tuntas",
            "Dibahas di hari yang sama setelah agak tenang",
            "Butuh waktu sendiri dulu satu-dua hari",
            "Menunggu sampai masalahnya reda sendiri",
        ],
    },
    {
        "id": "kabar",
        "question": "Soal chat dan kabar, yang paling nyaman buat kamu...",
        "options": [
            "Saling kabari hampir sepanjang hari",
            "Beberapa kali sehari sudah cukup",
            "Sekali-sekali, yang penting ada saat dibutuhkan",
            "Jarang chat, lebih suka ketemu langsung",
        ],
    },
    {
        "id": "uang",
        "question": "Kalau ada biaya bersama, kamu lebih suka...",
        "options": [
            "Dicatat detail sampai ke recehnya",
            "Dibagi rata, dicatat garis besarnya",
            "Gantian bayar, nanti juga impas",
            "Siapa yang sedang longgar, dia yang bayar",
        ],
    },
    {
        "id": "capek",
        "question": "Waktu sedang capek, dukungan yang paling kamu butuhkan...",
        "options": [
            "Ditemani dan diajak ngobrol",
            "Dibantu urusan praktisnya",
            "Ditinggal sebentar tanpa ditanya-tanya",
            "Dibiarkan sampai kamu sendiri yang cerita",
        ],
    },
    {
        "id": "keputusan",
        "question": "Saat harus memutuskan sesuatu bersama, kamu cenderung...",
        "options": [
            "Memimpin dan cepat memutuskan",
            "Mengusulkan lalu minta pendapat",
            "Menimbang semua pilihan dulu lama-lama",
            "Mengikuti yang lain asal tidak merugikan",
        ],
        "pairing": [
            [0.4, 0.9, 0.6, 1.0],
            [0.9, 1.0, 0.8, 0.8],
            [0.6, 0.8, 0.6, 0.7],
            [1.0, 0.8, 0.7, 0.3],
        ],
        "pairing_labels": ["Klop", "Cukup cocok", "Perlu disepakati", "Perlu bagi peran"],
    },
    {
        "id": "jujur",
        "question": "Soal menyampaikan hal yang tidak enak, kamu lebih memilih...",
        "options": [
            "Blak-blakan walau menyakitkan",
            "Jujur tapi pilih kata dengan hati-hati",
            "Menyampaikan lewat sindiran halus",
            "Menyimpannya demi menjaga suasana",
        ],
    },
    {
        "id": "waktu",
        "question": "Cara ideal menghabiskan waktu bareng...",
        "options": [
            "Mencoba kegiatan yang belum pernah dilakukan",
            "Ke tempat favorit yang sudah biasa",
            "Nongkrong santai tanpa rencana",
            "Di rumah saja, sibuk masing-masing tapi tetap bersama",
        ],
    },
    {
        "id": "sayang",
        "question": "Cara paling alami kamu menunjukkan sayang...",
        "options": [
            "Diucapkan terang-terangan hampir tiap hari",
            "Lewat perhatian kecil yang konsisten",
            "Dibuktikan lewat tindakan, jarang diucapkan",
            "Disimpan dalam hati, yang penting setia",
        ],
    },
    {
        "id": "tenggat",
        "question": "Kalau ada tenggat pekerjaan, kamu biasanya...",
        "options": [
            "Selesai jauh sebelum tenggat",
            "Dicicil rata sampai hari tenggat",
            "Ngebut di beberapa hari terakhir",
            "Mepet di jam-jam terakhir",
        ],
    },
    {
        "id": "kritik",
        "question": "Saat hasil kerjamu perlu dikoreksi, kamu lebih suka...",
        "options": [
            "Langsung dan detail, di mana pun",
            "Langsung, tapi disampaikan berdua saja",
            "Dibuka dulu dengan bagian yang sudah bagus",
            "Lewat tulisan supaya bisa dicerna dulu",
        ],
    },
]

PAIR_LENS_QUESTION_IDS = {
    "asmara": ["rencana", "masalah", "kabar", "uang", "capek", "keputusan", "jujur", "sayang"],
    "pertemanan": ["rencana", "masalah", "kabar", "uang", "capek", "keputusan", "jujur", "waktu"],
    "kerja": ["rencana", "masalah", "tenggat", "uang", "capek", "keputusan", "jujur", "kritik"],
}

LEGACY_PAIR_QUESTION_IDS = ["rencana", "masalah", "kabar", "uang", "capek", "keputusan", "jujur", "waktu"]

PAIR_VERDICT_BANK = {
    "sejalan": [
        {"title": "Sefrekuensi", "note": "Cara pikir kalian searah dan bawaan shionya mendukung. Kalian jarang perlu menjelaskan diri panjang lebar."},
        {"title": "Satu Gelombang", "note": "Bawaan dan kebiasaan kalian sama-sama mengarah ke tempat yang sama. Kekuatannya di situ, dan titik butanya juga sama."},
    ],
    "beda_bawaan": [
        {"title": "Beda Akar, Satu Arah", "note": "Bawaan shio kalian bergesekan, tapi cara kalian menjalani hari justru searah. Kebiasaan yang kalian pilih sendiri ternyata lebih kuat dari bawaan."},
        {"title": "Cocok Karena Pilihan", "note": "Di atas kertas shio kalian kurang akur, tapi jawaban kalian banyak yang nyambung. Yang menyatukan kalian adalah cara hidup, bukan bawaan."},
    ],
    "beda_kebiasaan": [
        {"title": "Bawaan Klop, Kebiasaan Beda", "note": "Shio kalian saling mendukung, tapi kebiasaan harian kalian cukup berbeda. Modalnya ada, tinggal menyepakati cara sehari-hari."},
        {"title": "Potensi yang Belum Dipakai", "note": "Bawaan shio kalian cocok, sedangkan jawaban kalian sering berseberangan. Perbedaannya ada di cara, bukan di dasar."},
    ],
    "perlu_usaha": [
        {"title": "Butuh Penerjemah", "note": "Bawaan shio dan kebiasaan kalian sama-sama menarik ke arah berbeda. Kalau tetap mau jalan bareng, sepakati aturan main sejak awal."},
        {"title": "Kutub Berlawanan", "note": "Bawaan maupun kebiasaan kalian jarang searah. Itu bisa jadi sumber gesekan, bisa juga jadi cara saling belajar."},
    ],
}

GROUP_ROLE_BANK = {
    "perekat": [
        {"title": "Perekat Geng", "note": "Sebagian besar relasimu di geng ini harmonis. Kalau kamu absen, suasananya terasa beda."},
        {"title": "Lem Kosmik", "note": "Kamu nyambung dengan banyak orang di sini. Biasanya kamu yang tanpa sadar menyatukan obrolan."},
        {"title": "Titik Kumpul", "note": "Banyak orang di kelompok ini gampang akur denganmu. Kamu jembatan yang tidak kelihatan."},
    ],
    "pemicu": [
        {"title": "Pemantik", "note": "Relasimu di geng ini lebih banyak yang bergesekan. Bukan berarti kamu biang masalah, tapi kamu sering menggoyang zona nyaman."},
        {"title": "Sumber Percikan", "note": "Energimu sering bertabrakan dengan yang lain. Gesekan itu bikin kelompok ini tidak pernah membosankan."},
        {"title": "Penguji Batas", "note": "Kamu sering bikin kelompok ini berpikir ulang. Kadang melelahkan, sering juga perlu."},
    ],
    "jembatan": [
        {"title": "Jembatan Dua Kubu", "note": "Kamu punya ikatan harmonis dan benturan dalam jumlah seimbang. Posisimu pas untuk menengahi."},
        {"title": "Penghubung", "note": "Kamu akrab dengan sebagian dan bergesekan dengan sebagian lain. Karena itu kamu paham dua sisi."},
        {"title": "Penerjemah Kelompok", "note": "Kamu bisa masuk ke dua suasana sekaligus. Kelompok ini butuh orang seperti kamu saat ada salah paham."},
    ],
    "penyeimbang": [
        {"title": "Penyeimbang", "note": "Relasimu di kelompok ini kebanyakan netral. Kamu jarang terseret drama, jadi kepalamu paling dingin."},
        {"title": "Jangkar Tenang", "note": "Kamu tidak terlalu terikat dan tidak bentrok dengan siapa pun. Stabil, dan justru itu yang dibutuhkan."},
        {"title": "Pengamat Jernih", "note": "Kamu melihat dinamika kelompok ini dari jarak yang pas. Pendapatmu biasanya paling adil."},
    ],
}

GROUP_VERDICT_BANK = {
    "harmonis": [
        {"title": "Geng yang Klop", "note": "Ikatan harmonis jauh lebih banyak dari benturan. Kelompok ini gampang kompak, tinggal jaga supaya tetap terbuka pada orang baru."},
        {"title": "Satu Frekuensi", "note": "Kebanyakan dari kalian saling mengunci. Rencana bareng biasanya jalan, asal ada yang bertugas mengingatkan hal membosankan."},
        {"title": "Lingkaran Hangat", "note": "Kelompok ini terasa nyaman dari dalam. Risikonya cuma satu: terlalu nyaman sampai lupa saling menantang."},
    ],
    "bentrok": [
        {"title": "Geng Penuh Percikan", "note": "Benturan lebih banyak dari ikatan harmonis. Kelompok ini hidup dan berisik, dan butuh aturan main yang jelas."},
        {"title": "Arena Kosmik", "note": "Banyak di antara kalian saling berseberangan. Itu bisa jadi sumber ide terbaik, asal tidak berubah jadi saling menjatuhkan."},
        {"title": "Tim Anti Bosan", "note": "Energi kalian sering bertabrakan. Kelompok seperti ini paling kuat kalau punya satu tujuan yang disepakati bersama."},
    ],
    "campur": [
        {"title": "Geng Warna-warni", "note": "Ikatan dan benturan kurang lebih seimbang. Kelompok ini punya sub-lingkaran, dan itu wajar."},
        {"title": "Campuran Pas", "note": "Ada yang saling mengunci, ada yang saling menggesek, banyak juga yang netral. Kelompok ini fleksibel."},
        {"title": "Mosaik Kosmik", "note": "Tidak ada pola dominan di kelompok ini. Hasilnya lebih banyak ditentukan kebiasaan kalian daripada bawaan shio."},
    ],
}

GUESS_VERDICT_BANK = {
    "terbaca": [
        {"title": "Buku Terbuka", "note": "Teman-temanmu menebakmu dengan cepat. Kamu jadi dirimu sendiri di depan mereka, dan mereka memperhatikan."},
        {"title": "Gampang Dikenali", "note": "Sifatmu terbaca jelas oleh kelompok ini. Itu tanda kalian cukup dekat."},
    ],
    "sebagian": [
        {"title": "Setengah Misteri", "note": "Sebagian temanmu langsung tahu, sebagian perlu beberapa petunjuk. Ada sisi dirimu yang belum semua orang lihat."},
        {"title": "Butuh Petunjuk", "note": "Teman-temanmu mengenalmu, tapi tidak dari sifat-sifat ini. Mungkin yang mereka lihat justru sisi lain."},
    ],
    "misterius": [
        {"title": "Penuh Kejutan", "note": "Teman-temanmu paling susah menebakmu. Kamu lebih rumit dari yang kelihatan, atau mereka yang kurang memperhatikan."},
        {"title": "Tertutup Rapat", "note": "Sifat-sifat ini ternyata tidak cocok dengan gambaran mereka tentangmu. Menarik untuk diobrolkan setelah ini."},
    ],
}

QUIZ_MODE_BANK = {
    "pasangan": {
        "title": "Ramalan Pasangan",
        "tagline": "Berdua, isi tanggal lahir dan jawab 8 soal. Untuk pacar, sahabat, atau rekan kerja.",
        "icon": "fa-people-arrows",
    },
    "kelompok": {
        "title": "Ramalan Kelompok",
        "tagline": "3 sampai 8 orang. Lihat siapa perekat, siapa pemantik, dan pasangan mana yang paling klop.",
        "icon": "fa-people-group",
    },
    "tebak": {
        "title": "Tebak Shio Teman",
        "tagline": "3 sampai 8 orang. Tebak sifat-sifat ini milik teman yang mana.",
        "icon": "fa-user-secret",
    },
}

GUESS_FLAVOR_BANK = {
    "manis": {
        "label": "Manis",
        "note": "Petunjuk diambil dari sifat baik dan green flag. Aman untuk grup yang belum terlalu akrab.",
    },
    "pedas": {
        "label": "Pedas",
        "note": "Petunjuk diambil dari bank roasting. Hanya untuk teman yang sudah siap diledek.",
    },
}

GUESS_STOPWORDS = frozenset([
    "yang", "tidak", "orang", "tanpa", "saat", "kamu", "pada", "dari", "untuk",
    "dengan", "jadi", "bisa", "lebih", "sudah", "juga", "karena", "tapi", "sama",
    "lagi", "kalau", "buat", "nggak", "banget", "atau", "akan", "masih", "hanya",
    "cuma", "semua", "sering", "selalu", "terlalu", "sendiri", "mereka", "kalian",
    "harus", "perlu", "bikin", "biar", "dulu", "baru", "sampai", "setelah",
    "sebelum", "justru", "bahkan", "hari", "yg", "gitu", "kayak", "padahal",
])

GUESS_SIGNATURE_TRAITS = {
    "tikus": [
        "Selalu punya simpanan cadangan untuk hari yang tidak terduga",
        "Tahu harga termurah dan jalan pintas sebelum orang lain sadar",
    ],
    "kerbau": [
        "Menuntaskan pekerjaan maraton tanpa sekali pun mengeluh",
        "Paling sulit digoyahkan kalau sudah memutuskan sesuatu",
    ],
    "macan": [
        "Maju paling depan ketika yang lain masih ragu",
        "Punya aura pemimpin sejak pertama masuk ruangan",
    ],
    "kelinci": [
        "Rumahnya selalu wangi, rapi, dan enak dipakai berkumpul",
        "Menghindari keributan dengan cara yang elegan",
    ],
    "naga": [
        "Masuk ruangan dan semua mata langsung menoleh",
        "Punya rencana besar yang terdengar mustahil tapi sering berhasil",
    ],
    "ular": [
        "Membaca niat orang dari hal kecil yang tidak diucapkan",
        "Tampak tenang dan misterius, padahal pikirannya jalan terus",
    ],
    "kuda": [
        "Paling semangat diajak jalan dadakan ke tempat baru",
        "Tidak tahan diam lama di satu tempat",
    ],
    "kambing": [
        "Menemukan keindahan di hal-hal yang dilewatkan orang",
        "Paling tulus merawat teman yang sedang sakit",
    ],
    "monyet": [
        "Paling cepat menemukan cara cerdik keluar dari masalah",
        "Candaannya selalu pas dan bikin suasana cair",
    ],
    "ayam": [
        "Penampilannya selalu rapi dan terencana dari ujung kepala sampai kaki",
        "Punya daftar tugas untuk hampir semua hal",
    ],
    "anjing": [
        "Paling protektif pada orang-orang terdekatnya",
        "Waspada pada orang baru sampai terbukti bisa dipercaya",
    ],
    "babi": [
        "Paling menikmati makan enak dan kumpul santai",
        "Tuan rumah yang membuat tamu betah berlama-lama",
    ],
}

GUESS_EXTRA_TRAITS = {
    "tikus": [
        "Pandai berjejaring dan tahu siapa yang bisa dimintai tolong",
        "Hemat untuk diri sendiri tapi royal pada keluarga",
        "Menghitung untung rugi dalam hitungan detik",
    ],
    "kerbau": [
        "Lebih percaya hasil kerja daripada kata-kata manis",
        "Rutinitas paginya hampir tidak pernah bolong",
        "Menabung tenaga untuk tujuan yang masih jauh",
    ],
    "macan": [
        "Tidak suka diatur tapi rela mengatur demi kelompok",
        "Makin tertantang justru ketika diremehkan",
        "Melindungi yang lemah tanpa menunggu diminta",
    ],
    "kelinci": [
        "Pandai memilih kata supaya tidak ada yang tersinggung",
        "Lingkar pertemanannya kecil tapi sangat dijaga",
        "Memperhatikan estetika sampai ke detail kecil",
    ],
    "naga": [
        "Percaya diri berbicara di depan banyak orang",
        "Menyemangati tim dengan visi yang besar",
        "Suka tantangan yang membuat orang lain mundur",
    ],
    "ular": [
        "Hemat bicara, tapi setiap kalimatnya bermakna",
        "Memutuskan setelah semua informasi terkumpul",
        "Seleranya elegan dan tidak mencolok",
    ],
    "kuda": [
        "Bebas dan tidak suka dikekang aturan",
        "Energinya membuat suasana langsung hidup",
        "Menikmati keputusan spontan tanpa banyak menimbang",
    ],
    "kambing": [
        "Suka berkarya, dari memasak sampai menggambar",
        "Paling nyaman di tempat yang tenang dan hangat",
        "Mudah tersentuh oleh cerita hidup orang lain",
    ],
    "monyet": [
        "Pandai menirukan gaya orang lain dengan lucu",
        "Suka teka-teki, permainan, dan tantangan otak",
        "Punya jawaban kreatif untuk pertanyaan yang aneh",
    ],
    "ayam": [
        "Bangun paling pagi dan sudah menyelesaikan banyak hal",
        "Memberi masukan jujur supaya hasilnya lebih baik",
        "Bangga pada hasil kerja yang tertata",
    ],
    "anjing": [
        "Mengingatkan dengan tegas kalau ada yang curang",
        "Siap menemani sampai urusanmu selesai",
        "Mendahulukan kepentingan kelompok daripada diri sendiri",
    ],
    "babi": [
        "Gampang memaafkan dan melanjutkan hidup",
        "Membawa suasana santai di tengah orang yang tegang",
        "Suka berbagi makanan dan cerita dengan siapa saja",
    ],
}
