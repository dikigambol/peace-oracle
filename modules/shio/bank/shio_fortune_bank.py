HEAVENLY_STEMS = [
    ("Jia", "甲"), ("Yi", "乙"), ("Bing", "丙"), ("Ding", "丁"), ("Wu", "戊"),
    ("Ji", "己"), ("Geng", "庚"), ("Xin", "辛"), ("Ren", "壬"), ("Gui", "癸"),
]

EARTHLY_BRANCHES = [
    ("Zi", "子"), ("Chou", "丑"), ("Yin", "寅"), ("Mao", "卯"),
    ("Chen", "辰"), ("Si", "巳"), ("Wu", "午"), ("Wei", "未"),
    ("Shen", "申"), ("You", "酉"), ("Xu", "戌"), ("Hai", "亥"),
]

STEM_ELEMENTS = [
    "kayu", "kayu", "api", "api", "tanah",
    "tanah", "logam", "logam", "air", "air",
]

STEM_POLARITY = [
    "yang", "yin", "yang", "yin", "yang",
    "yin", "yang", "yin", "yang", "yin",
]

BRANCH_ELEMENTS = [
    "air", "tanah", "kayu", "kayu", "tanah", "api",
    "api", "tanah", "logam", "logam", "tanah", "air",
]

ELEMENT_LABELS = {
    "kayu": ("Kayu", "木"),
    "api": ("Api", "火"),
    "tanah": ("Tanah", "土"),
    "logam": ("Logam", "金"),
    "air": ("Air", "水"),
}

ELEMENT_GENERATES = {
    "kayu": "api",
    "api": "tanah",
    "tanah": "logam",
    "logam": "air",
    "air": "kayu",
}

ELEMENT_CONTROLS = {
    "kayu": "tanah",
    "tanah": "air",
    "air": "api",
    "api": "logam",
    "logam": "kayu",
}

HIDDEN_STEMS = [
    [9],
    [5, 9, 7],
    [0, 2, 4],
    [1],
    [4, 1, 9],
    [2, 4, 6],
    [3, 5],
    [5, 3, 1],
    [6, 8, 4],
    [7],
    [4, 7, 3],
    [8, 0],
]

HIDDEN_STEM_WEIGHTS = (1.0, 0.5, 0.3)

TEN_GODS_TABLE = {
    ("sama", True): "bi_jian",
    ("sama", False): "jie_cai",
    ("dm_menghidupi", True): "shi_shen",
    ("dm_menghidupi", False): "shang_guan",
    ("dm_mengekang", True): "pian_cai",
    ("dm_mengekang", False): "zheng_cai",
    ("mengekang_dm", True): "qi_sha",
    ("mengekang_dm", False): "zheng_guan",
    ("menghidupi_dm", True): "pian_yin",
    ("menghidupi_dm", False): "zheng_yin",
}

LIU_HE_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 1), (2, 11), (3, 10), (4, 9), (5, 8), (6, 7)]
)

LIU_PO_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 9), (1, 4), (2, 11), (3, 6), (5, 8), (7, 10)]
)

LIU_HAI_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(0, 7), (1, 6), (2, 5), (3, 4), (8, 11), (9, 10)]
)

XIANG_XING_PAIRS = frozenset(
    frozenset(pair)
    for pair in [(2, 5), (5, 8), (2, 8), (1, 10), (10, 7), (1, 7), (0, 3)]
)

ZI_XING_BRANCHES = frozenset([4, 6, 9, 11])

BRANCH_RELATION_META = {
    "liu_he": {"label": "Liu He (Jodoh Kosmik Sejati)", "code": "good", "band": (95, 99)},
    "san_he": {"label": "San He (Tiga Harmoni)", "code": "good", "band": (85, 90)},
    "ben_ming": {"label": "Ben Ming (Kembar Kosmik)", "code": "neutral", "band": (72, 78)},
    "netral": {"label": "Ping (Netral & Stabil)", "code": "neutral", "band": (58, 68)},
    "liu_po": {"label": "Liu Po (Perusakan)", "code": "bad", "band": (50, 57)},
    "zi_xing": {"label": "Zi Xing (Hukuman Diri)", "code": "bad", "band": (44, 49)},
    "liu_hai": {"label": "Liu Hai (Saling Menyakiti)", "code": "bad", "band": (37, 43)},
    "xiang_xing": {"label": "Xiang Xing (Hukuman)", "code": "bad", "band": (30, 36)},
    "chong": {"label": "Chong (Bentrokan Ekstrem)", "code": "bad", "band": (23, 29)},
}

JULIAN_DAY_OFFSET = 1721425


DAY_MASTER_BANK = {
    "jia": {
        "stem_cn": "甲",
        "stem_id": "Jia",
        "element": "kayu",
        "polarity": "yang",
        "title": "Pohon Besar yang Tumbuh Lurus",
        "personality": "Kamu punya arah yang jelas sejak awal dan tidak suka berbelok cuma karena keadaan berubah. Orang menaruh banyak hal padamu karena kamu terlihat sanggup menahan beban, dan sering kali kamu memang sanggup — sampai titik tertentu. Yang jarang terlihat: kamu butuh waktu lama untuk mengakui kalau arah yang kamu pilih ternyata salah. Kamu tumbuh ke atas, bukan ke samping; begitu terhalang, kamu cenderung menabrak daripada memutar.",
        "strengths": [
            "Punya prinsip yang tidak gampang ditawar",
            "Sanggup memikul tanggung jawab jangka panjang",
            "Jadi tempat orang bersandar tanpa perlu diminta",
            "Berpikir jauh ke depan, bukan cuma ke bulan depan",
            "Konsisten meski tidak ada yang mengawasi",
        ],
        "weaknesses": [
            "Sulit berbelok meski sudah jelas buntu",
            "Kaku pada cara yang terlanjur dipakai",
            "Menahan sendiri sampai patah, bukan minta tolong",
            "Gengsi mengakui keliru di depan orang",
            "Kurang peka pada hal yang tidak diucapkan",
        ],
        "when_strong": "甲 yang kuat jadi pohon terlalu rapat: kamu menutupi orang-orang di bawahmu tanpa sadar. Kamu justru butuh kapak — tenggat, tekanan, atau orang yang berani menentangmu — supaya bentukmu terbentuk.",
        "when_weak": "甲 yang lemah adalah bibit yang belum berakar: niatmu besar tapi tenaganya belum sampai. Cari tanah dan air dulu, lingkungan yang menopang dan ilmu yang cukup, sebelum menargetkan tinggi.",
        "nuance": {
            "karir": "Kamu cocok jadi orang yang memulai dan menegakkan, bukan yang merapikan detail di belakang.",
            "rezeki": "Uangmu tumbuh lambat tapi jarang runtuh sekaligus, karena kamu tidak pernah benar-benar bertaruh.",
            "asmara": "Kamu setia dengan cara yang tidak romantis: tetap ada, tetap menanggung, tanpa banyak dibicarakan.",
        },
    },
    "yi": {
        "stem_cn": "乙",
        "stem_id": "Yi",
        "element": "kayu",
        "polarity": "yin",
        "title": "Sulur yang Selalu Menemukan Jalan",
        "personality": "Kamu bertahan bukan dengan melawan, tapi dengan menyesuaikan diri sampai keadaan berpihak. Di tempat yang bikin orang lain menyerah, kamu justru menemukan celah. Kamu pandai membaca siapa yang bisa dijadikan sandaran dan tidak malu memakainya — itu bukan kelemahan, itu caramu tumbuh. Yang melelahkan: kamu jarang sekali menunjukkan bahwa kamu sedang kesulitan.",
        "strengths": [
            "Lentur tanpa kehilangan tujuan",
            "Pandai membaca suasana dan orang",
            "Tahan di situasi yang jauh dari ideal",
            "Bisa akrab dengan hampir semua kalangan",
            "Sabar menunggu waktu yang tepat",
        ],
        "weaknesses": [
            "Terlalu bergantung pada orang yang dianggap kuat",
            "Menghindari konflik sampai masalah menumpuk",
            "Sulit menyatakan mau sendiri secara terbuka",
            "Berubah pendirian mengikuti siapa yang sedang dekat",
            "Menyimpan kesal lama tanpa disampaikan",
        ],
        "when_strong": "乙 yang kuat merambat ke mana-mana sampai tidak jelas lagi mana akarnya sendiri. Tentukan satu hal yang tetap kamu pertahankan apa pun keadaannya.",
        "when_weak": "乙 yang lemah gampang terbawa siapa pun yang paling berisik di sekitarmu. Bangun satu keahlian yang membuatmu dicari, bukan cuma disukai.",
        "nuance": {
            "karir": "Kamu unggul di peran yang menghubungkan orang dan menembus pintu yang tertutup.",
            "rezeki": "Rezekimu sering lewat relasi, jadi merawat hubungan sama pentingnya dengan merawat pekerjaan.",
            "asmara": "Kamu melekat dalam-dalam, dan justru itu yang perlu dijaga supaya tidak berubah jadi kehilangan diri.",
        },
    },
    "bing": {
        "stem_cn": "丙",
        "stem_id": "Bing",
        "element": "api",
        "polarity": "yang",
        "title": "Matahari yang Tidak Bisa Setengah Bersinar",
        "personality": "Kamu hadir sepenuhnya atau tidak sama sekali. Suasana ruangan berubah saat kamu masuk, dan itu bukan sesuatu yang kamu usahakan. Kamu terbuka, cepat panas, cepat reda, dan hampir tidak menyimpan dendam — apa yang kamu rasakan hari ini sudah kamu keluarkan hari ini juga. Yang bikin repot: kamu sering lupa bahwa tidak semua orang butuh disinari sekeras itu.",
        "strengths": [
            "Menularkan semangat tanpa harus berusaha",
            "Jujur dan terbuka soal apa yang dirasakan",
            "Cepat memaafkan lalu melanjutkan",
            "Berani tampil dan mengambil panggung",
            "Melihat sisi baik orang lebih dulu",
        ],
        "weaknesses": [
            "Meledak duluan sebelum tahu duduk perkaranya",
            "Kurang tahan pada pekerjaan yang sepi dan panjang",
            "Boros tenaga untuk orang yang tidak memintanya",
            "Gampang bosan begitu sorotan pindah",
            "Menyepelekan detail yang tidak menarik",
        ],
        "when_strong": "丙 yang kuat membakar, bukan menghangatkan — orang mundur bukan karena tidak suka, tapi karena kepanasan. Pakai tenagamu untuk mengangkat satu orang, bukan menyilaukan sepuluh.",
        "when_weak": "丙 yang lemah seperti matahari di musim hujan: niat menolongmu ada, tapi tidak sampai. Kurangi jumlah orang yang kamu urus sampai tenagamu pulih.",
        "nuance": {
            "karir": "Peran yang menuntutmu terlihat dan bicara di depan orang cocok; kerja senyap perlahan menghabisimu.",
            "rezeki": "Uang datang saat namamu dikenal, jadi reputasi buatmu bukan pelengkap melainkan mesin.",
            "asmara": "Kamu mencintai terang-terangan dan berharap dibalas dengan kejelasan yang setara.",
        },
    },
    "ding": {
        "stem_cn": "丁",
        "stem_id": "Ding",
        "element": "api",
        "polarity": "yin",
        "title": "Lilin yang Menyala di Ruang yang Tepat",
        "personality": "Kamu tidak menerangi semua orang, hanya yang benar-benar butuh. Perhatianmu tajam dan terarah: kamu menangkap apa yang tidak diucapkan dan sering tahu duluan kalau ada yang sedang tidak baik-baik saja. Kamu bekerja paling baik dalam jangkauan kecil tapi dalam, bukan luas tapi dangkal. Yang jarang disadari orang: kamu menyala dengan cara membakar dirimu sendiri.",
        "strengths": [
            "Peka pada apa yang tidak dikatakan orang",
            "Telaten pada pekerjaan yang butuh ketelitian tinggi",
            "Setia pada lingkaran kecil yang sudah dipercaya",
            "Punya firasat yang sering terbukti benar",
            "Bisa bekerja lama tanpa perlu disorot",
        ],
        "weaknesses": [
            "Menyimpan perasaan sampai jadi beban sendiri",
            "Curiga pada niat orang tanpa bukti yang cukup",
            "Habis tenaga karena mengurusi orang lain",
            "Terlalu memikirkan ulang keputusan yang sudah diambil",
            "Sulit melepas orang yang sudah menyakiti",
        ],
        "when_strong": "丁 yang kuat jadi nyala yang tidak pernah padam sampai bahan bakarnya habis. Tetapkan jam berhenti, karena kamu tidak punya rem alami.",
        "when_weak": "丁 yang lemah mudah tertiup hal kecil — komentar satu orang bisa mengubah seluruh harimu. Bangun penyangga: rutinitas tetap dan satu orang yang bisa memeriksa isi pikiranmu.",
        "nuance": {
            "karir": "Bidang yang menuntut kedalaman dan kesabaran cocok; kamu menonjol lewat hasil, bukan lewat presentasi.",
            "rezeki": "Rezekimu stabil kalau kamu punya satu keahlian yang dalam, bukan banyak keahlian setengah jadi.",
            "asmara": "Kamu memberi perhatian yang sangat spesifik, dan paling kecewa kalau itu tidak dibaca.",
        },
    },
    "wu": {
        "stem_cn": "戊",
        "stem_id": "Wu",
        "element": "tanah",
        "polarity": "yang",
        "title": "Gunung yang Tidak Diminta Bergeser",
        "personality": "Kamu jadi tempat orang menaruh hal-hal berat, dan kamu menerimanya tanpa banyak komentar. Perubahan bukan musuhmu, tapi kamu butuh waktu lebih lama dari orang lain untuk ikut bergerak. Kamu menilai sesuatu dari seberapa tahan lama, bukan seberapa menarik. Yang sering terjadi: orang menganggap diammu sebagai setuju, padahal kamu cuma belum selesai berpikir.",
        "strengths": [
            "Stabil dan bisa diandalkan bertahun-tahun",
            "Tenang saat orang lain panik",
            "Menyimpan rahasia tanpa perlu diingatkan",
            "Adil saat menengahi perselisihan",
            "Tahan pada pekerjaan yang membosankan",
        ],
        "weaknesses": [
            "Lambat mengambil keputusan besar",
            "Menumpuk masalah yang tidak dibicarakan",
            "Susah melepas hal yang sudah tidak berguna",
            "Terlalu menahan diri sampai terlihat tidak peduli",
            "Keras kepala dengan cara yang tenang",
        ],
        "when_strong": "戊 yang kuat jadi tanah terlalu padat: tidak ada yang bisa tumbuh di atasnya, termasuk kamu sendiri. Biarkan ada yang menggali — pertanyaan, kritik, hal baru yang mengganggu.",
        "when_weak": "戊 yang lemah adalah tanah yang longsor begitu dibebani. Kurangi jumlah orang yang bergantung padamu sampai pijakanmu sendiri kokoh.",
        "nuance": {
            "karir": "Kamu cocok memegang hal yang tidak boleh goyah: operasional, aset, kepercayaan orang banyak.",
            "rezeki": "Kekayaanmu berbentuk sesuatu yang bisa dipegang dan bertahan, bukan angka yang berputar cepat.",
            "asmara": "Kamu menawarkan rasa aman, dan itu yang membuat orang betah lama di sisimu.",
        },
    },
    "ji": {
        "stem_cn": "己",
        "stem_id": "Ji",
        "element": "tanah",
        "polarity": "yin",
        "title": "Tanah Kebun yang Menumbuhkan Diam-diam",
        "personality": "Kamu memberi tempat pada hal dan orang untuk tumbuh, sering tanpa terlihat sedang melakukan apa pun. Kamu menyesuaikan diri pada apa yang ditanam di atasmu — itu membuatmu berguna di banyak tempat, sekaligus membuatmu sulit menjelaskan apa sebenarnya maumu. Kamu mengurus detail yang orang lain anggap remeh, dan biasanya justru hal-hal itu yang menentukan.",
        "strengths": [
            "Telaten mengurus hal yang tidak terlihat",
            "Mudah menerima orang apa adanya",
            "Fleksibel tanpa melepas tanggung jawab",
            "Pandai menyimpan dan mengelola",
            "Sabar pada proses yang lama",
        ],
        "weaknesses": [
            "Memendam kekhawatiran sampai jadi penyakit",
            "Sulit menolak permintaan orang",
            "Kurang percaya pada kemampuannya sendiri",
            "Terlalu banyak berpikir sebelum bertindak",
            "Memikul beban orang lain tanpa diminta",
        ],
        "when_strong": "己 yang kuat jadi tanah terlalu tebal — apa pun yang ditanam tenggelam, termasuk rencanamu sendiri. Bereskan satu hal sampai tuntas sebelum menerima yang berikutnya.",
        "when_weak": "己 yang lemah gampang hanyut begitu hujan datang. Bangun batas yang jelas soal siapa yang boleh menaruh bebannya padamu.",
        "nuance": {
            "karir": "Peran pendukung yang menentukan cocok denganmu: mengelola, merawat, memastikan semuanya tetap jalan.",
            "rezeki": "Uangmu bertahan karena kamu pandai menyimpan, bukan karena besar pemasukannya.",
            "asmara": "Kamu mengurus pasangan sampai ke hal terkecil, dan diam-diam berharap itu terlihat.",
        },
    },
    "geng": {
        "stem_cn": "庚",
        "stem_id": "Geng",
        "element": "logam",
        "polarity": "yang",
        "title": "Logam Mentah yang Ditempa Jadi Alat",
        "personality": "Kamu memangkas apa yang tidak perlu — di pekerjaan, di hubungan, di caramu bicara. Ketegasanmu membuat urusan cepat selesai dan sebagian orang tersinggung dalam prosesnya. Kamu lebih percaya pada apa yang terbukti daripada apa yang dijanjikan. Yang orang tidak tahu: kamu keras pada orang lain karena kamu jauh lebih keras pada dirimu sendiri.",
        "strengths": [
            "Tegas mengambil keputusan yang tidak enak",
            "Loyal pada orang yang sudah terbukti",
            "Berani memangkas yang sudah tidak berguna",
            "Tahan pada tekanan fisik maupun mental",
            "Jelas menyatakan di mana batasnya",
        ],
        "weaknesses": [
            "Kasar saat menyampaikan hal yang benar",
            "Kurang sabar pada orang yang lambat",
            "Menyelesaikan masalah dengan memutus, bukan memperbaiki",
            "Sulit menunjukkan sisi yang rapuh",
            "Terlalu cepat menilai orang dari satu kesalahan",
        ],
        "when_strong": "庚 yang kuat memotong hal yang sebenarnya masih hidup. Sebelum memutus hubungan atau pekerjaan, tunggu satu putaran musim penuh.",
        "when_weak": "庚 yang lemah adalah pisau tumpul: kamu tahu apa yang harus dipotong tapi tidak sanggup melakukannya. Latih dari keputusan kecil yang memang tidak enak.",
        "nuance": {
            "karir": "Bidang berstandar keras cocok: penegakan aturan, audit, teknik, keamanan, pengawasan mutu.",
            "rezeki": "Uangmu datang dari kerja yang berat dan terukur, bukan dari negosiasi yang manis.",
            "asmara": "Kamu melindungi lewat tindakan, dan perlu belajar bahwa sebagian orang butuh mendengar kalimatnya.",
        },
    },
    "xin": {
        "stem_cn": "辛",
        "stem_id": "Xin",
        "element": "logam",
        "polarity": "yin",
        "title": "Permata yang Menuntut Dipoles Benar",
        "personality": "Kamu punya standar tinggi soal rasa, bentuk, dan cara sesuatu dikerjakan — dan kamu tidak sanggup pura-pura tidak keberatan saat standar itu dilanggar. Kamu ingin diakui, dan itu bukan hal yang perlu kamu sembunyikan; pengakuan memang bahan bakarmu. Kamu memperhatikan penampilan bukan karena dangkal, tapi karena buatmu penampilan adalah bentuk penghormatan.",
        "strengths": [
            "Punya selera dan standar mutu yang tinggi",
            "Teliti pada detail yang menentukan kesan",
            "Menjaga citra dan kata-katanya",
            "Tajam menilai kualitas orang maupun barang",
            "Bekerja rapi tanpa perlu diperiksa ulang",
        ],
        "weaknesses": [
            "Gampang tersinggung oleh kritik yang tidak halus",
            "Menyimpan luka lama lebih lama dari perlunya",
            "Terlalu mementingkan bagaimana sesuatu terlihat",
            "Perfeksionis sampai pekerjaan tidak kunjung selesai",
            "Sinis pada orang yang dianggap tidak bermutu",
        ],
        "when_strong": "辛 yang kuat jadi terlalu tajam pada hal kecil sampai orang capek berurusan denganmu. Pilih mana yang benar-benar layak kamu koreksi.",
        "when_weak": "辛 yang lemah kehilangan kilaunya: kamu tahu apa yang bagus tapi ragu pada penilaianmu sendiri. Pegang satu bidang sampai kamu jadi rujukan di situ.",
        "nuance": {
            "karir": "Bidang yang menilai rasa dan presisi cocok: desain, hukum, mode, kurasi, komunikasi, perhiasan.",
            "rezeki": "Rezekimu naik seiring naiknya kelas pekerjaan yang kamu terima, jadi jangan bersaing di harga.",
            "asmara": "Kamu ingin dibanggakan, bukan cuma disayangi — dan itu sah untuk kamu katakan.",
        },
    },
    "ren": {
        "stem_cn": "壬",
        "stem_id": "Ren",
        "element": "air",
        "polarity": "yang",
        "title": "Arus Besar yang Tidak Berhenti",
        "personality": "Pikiranmu bergerak terus dan jarang berhenti di satu tempat, itu sebabnya kamu cepat menangkap gambaran besar sesuatu. Kamu tidak terikat pada satu bentuk; kamu mengisi wadah apa pun yang tersedia lalu melanjutkan. Orang mengira kamu santai, padahal kamu sedang menghitung banyak hal sekaligus. Yang sulit buatmu: berhenti cukup lama untuk menuntaskan satu hal.",
        "strengths": [
            "Cepat menangkap pola dan gambaran besar",
            "Luwes di lingkungan mana pun",
            "Berani mengubah rencana saat datanya berubah",
            "Punya jaringan yang luas dan beragam",
            "Tidak gampang panik di situasi baru",
        ],
        "weaknesses": [
            "Sulit menuntaskan apa yang sudah dimulai",
            "Berpindah minat sebelum satu hal matang",
            "Menghindari komitmen yang mengikat",
            "Bicara lebih cepat daripada eksekusinya",
            "Sulit dipegang janjinya soal waktu",
        ],
        "when_strong": "壬 yang kuat jadi banjir: yang kamu bawa justru merusak apa yang seharusnya kamu airi. Buat batas — tenggat, struktur, orang yang berani menagihmu.",
        "when_weak": "壬 yang lemah adalah air yang mengering di tengah jalan: idemu banyak tapi tidak sampai ke muara. Kurangi jumlah proyeknya, tambah kedalamannya.",
        "nuance": {
            "karir": "Bidang yang bergerak dan berjejaring cocok: perdagangan, logistik, media, perjalanan, strategi.",
            "rezeki": "Uangmu mengalir masuk dan keluar sama derasnya, jadi bendungan berupa tabungan terkunci itu wajib.",
            "asmara": "Kamu butuh kebebasan bergerak, dan pasangan perlu tahu itu bukan tanda kamu hendak pergi.",
        },
    },
    "gui": {
        "stem_cn": "癸",
        "stem_id": "Gui",
        "element": "air",
        "polarity": "yin",
        "title": "Embun yang Meresap Tanpa Suara",
        "personality": "Kamu masuk ke dalam sesuatu pelan-pelan, sampai orang baru sadar pengaruhmu setelah cukup lama. Kamu menyimpan lebih banyak dari yang kamu tunjukkan dan memilih dengan hati-hati kepada siapa isi kepalamu dibuka. Kamu menangkap hal halus — perubahan nada suara, jeda yang kelamaan — dan biasanya kamu benar soal itu. Kelemahannya: kamu memikirkan satu hal berulang-ulang jauh setelah hal itu lewat.",
        "strengths": [
            "Menangkap hal halus yang orang lain lewatkan",
            "Bertahan lewat cara yang tidak mencolok",
            "Bisa dipercaya memegang rahasia",
            "Punya daya bayang dan firasat yang kuat",
            "Sabar menunggu tanpa mengeluh",
        ],
        "weaknesses": [
            "Memendam sampai orang tidak tahu ada masalah",
            "Terlalu lama memikirkan hal yang sudah lewat",
            "Sulit mengambil sikap tegas di depan umum",
            "Merasa tidak dihargai tapi memilih diam",
            "Menarik diri justru saat seharusnya bicara",
        ],
        "when_strong": "癸 yang kuat jadi hujan yang tak berhenti — semua terasa kelabu dan kamu menarik orang lain ikut ke dalamnya. Keluar, bergerak, cari yang panas dan terang.",
        "when_weak": "癸 yang lemah adalah embun yang menguap sebelum sempat meresap. Simpan tenagamu untuk sedikit hal yang benar-benar kamu pedulikan.",
        "nuance": {
            "karir": "Bidang yang menuntut kepekaan dan kerahasiaan cocok: riset, psikologi, penulisan, analisis, konsultasi.",
            "rezeki": "Rezekimu datang dari hal yang kamu tekuni diam-diam bertahun-tahun, bukan dari yang ramai hari ini.",
            "asmara": "Kamu ingin dibaca tanpa harus menjelaskan, dan itu harapan yang sesekali perlu kamu turunkan.",
        },
    },
}


CHART_STRENGTH_BANK = {
    "cong_qiang": {
        "label": "Cong Qiang (Mengikuti Kekuatan)",
        "hanzi": "從強",
        "title": "Arus Tunggal yang Tak Terbendung",
        "summary": "Hampir seluruh isi chart-mu menopang satu arah yang sama. Tidak ada elemen yang cukup kuat untuk mengerem, jadi chart ini tidak dibaca dengan aturan seimbang. Yang berlaku di sini: ikuti arusnya, jangan dilawan.",
        "advice": "Perkuat elemen yang sudah dominan, bukan yang kosong. Kamu berkembang paling jauh saat mengambil jalur yang memang sudah jadi kekuatanmu sejak awal, bukan saat mencoba jadi serba bisa.",
        "caution": "Usaha menyeimbangkan diri justru yang paling berisiko buat chart seperti ini. Periode yang membawa elemen penentang biasanya terasa jauh lebih berat dari kelihatannya.",
    },
    "shen_qiang": {
        "label": "Shen Qiang (Diri Kuat)",
        "hanzi": "身強",
        "title": "Tenaga Berlebih yang Butuh Saluran",
        "summary": "Dukungan untuk dirimu berlimpah: elemen sejenis dan penopangnya sama-sama banyak. Kamu punya tenaga, keras kepala, dan daya tahan di atas rata-rata. Yang kurang bukan kekuatannya, tapi tempat menyalurkannya.",
        "advice": "Cari kerja, karya, dan tanggung jawab yang benar-benar menghabiskan tenagamu. Elemen yang mengeluarkan, menghasilkan, dan menertibkanmu adalah yang membawa keberuntungan — bukan yang menambah tenaga.",
        "caution": "Kalau tidak tersalurkan, tenaga ini berbalik jadi keras kepala dan gesekan dengan orang sekitar. Istirahat berlebihan tidak bikin kamu pulih, malah bikin gelisah.",
    },
    "zhong_he": {
        "label": "Zhong He (Seimbang)",
        "hanzi": "中和",
        "title": "Timbangan yang Nyaris Rata",
        "summary": "Tidak ada sisi yang terlalu berat di chart-mu. Kamu bisa menyesuaikan diri di banyak situasi tanpa harus banyak berubah. Keuntungannya nyata: kamu jarang hancur oleh satu peristiwa.",
        "advice": "Karena tidak ada elemen yang wajib dikejar, yang menentukan hidupmu adalah pilihan sadar, bukan bawaan chart. Manfaatkan tiap periode 大運 untuk mengambil arah, karena kamu cukup lentur untuk mengikutinya.",
        "caution": "Lentur bisa berubah jadi tidak punya pendirian kalau kamu tidak pernah memilih. Kemudahan menyesuaikan diri bikin kamu gampang menunda keputusan besar.",
    },
    "shen_ruo": {
        "label": "Shen Ruo (Diri Lemah)",
        "hanzi": "身弱",
        "title": "Akar yang Perlu Diperkuat Dulu",
        "summary": "Elemen yang sejenis denganmu dan yang menopangmu kalah jumlah dari yang menguras. Kamu peka pada lingkungan dan cepat terpengaruh suasana. Ini bukan soal lemahnya karakter — ini soal siapa yang menopangmu.",
        "advice": "Elemen yang menguatkan dirimu beserta penopangnya adalah yang membawa keberuntungan. Secara praktis: bangun dulu ilmu, kesehatan, dan lingkaran pendukung sebelum mengambil beban besar.",
        "caution": "Peluang besar yang datang terlalu awal bisa jadi yang paling menghabiskanmu. Periksa dulu penopangnya ada atau tidak sebelum bilang iya.",
    },
    "cong_ruo": {
        "label": "Cong Ruo (Mengikuti Kelemahan)",
        "hanzi": "從弱",
        "title": "Melepas Pegangan, Mengikuti Arus",
        "summary": "Penopang untuk dirimu hampir tidak ada, dan elemen yang menguras justru menguasai chart. Karena tidak ada yang bisa dipertahankan, chart ini tidak dibaca dengan aturan menguatkan diri. Aturannya berbalik: menyerah pada arus justru yang menyelamatkan.",
        "advice": "Ikuti elemen yang mendominasi, meski secara teori dialah yang menguras. Kamu berkembang lewat orang lain, lembaga, dan kesempatan dari luar, bukan lewat memaksakan kehendak sendiri.",
        "caution": "Usaha keras berdiri sendiri biasanya yang paling menguras chart seperti ini. Bantuan yang menguatkan dirimu justru bisa datang di waktu yang salah.",
    },
}


TEN_GODS_BANK = {
    "bi_jian": {
        "name_cn": "比肩",
        "name_id": "Saudara Sebaya",
        "essence": "Kamu tumbuh dengan prinsip berdiri di kaki sendiri. Bantuan orang lain kamu terima seperlunya, tapi keputusan akhir hampir selalu kamu pegang sendiri. Sisi lainnya: kamu susah mengakui saat sedang butuh ditolong.",
        "in_career": "Kamu paling produktif kalau punya wilayah kerja sendiri yang jelas batasnya. Struktur dengan terlalu banyak lapisan persetujuan bikin gairahmu cepat habis.",
        "in_wealth": "Uangmu tumbuh dari tenaga dan waktumu sendiri, bukan dari titipan siapa pun. Hati-hati pada patungan yang porsinya dibagi rata tapi kerjanya tidak.",
        "in_love": "Kamu butuh pasangan yang punya dunianya sendiri, bukan yang menempel terus. Yang sering jadi masalah bukan rasa sayangnya, tapi soal siapa yang mengalah.",
        "when_strong": "比肩 yang menumpuk bikin kamu keras kepala dan gampang merasa tersaingi oleh orang yang sebenarnya satu tim denganmu. Latih diri membagi kerja, bukan memborongnya.",
        "when_weak": "比肩 yang tipis bikin kamu gampang ikut arus dan kesulitan bilang tidak. Cari satu lingkaran kecil sebagai tempat berlatih bersikap.",
    },
    "jie_cai": {
        "name_cn": "劫財",
        "name_id": "Perampas Harta",
        "essence": "Kamu punya keberanian yang bikin orang betah di dekatmu, sekaligus kebiasaan melepas apa yang kamu punya terlalu cepat. Murah hati dan boros tumbuh dari akar yang sama. Kamu jarang menyesal, tapi sering kehabisan.",
        "in_career": "Kamu bersinar di pekerjaan yang butuh keberanian ambil risiko, dan orang sekitarmu ikut terbakar semangatnya. Yang rawan: kamu ambil alih tugas orang lain lalu kewalahan sendiri.",
        "in_wealth": "Pemasukanmu bisa besar, tapi bocornya lewat orang terdekat — pinjaman, traktiran, patungan yang tak pernah kembali. Pisahkan mana rekening yang boleh dipakai bersama dan mana yang tidak.",
        "in_love": "Kamu memberi banyak di awal hubungan, kadang lebih banyak dari yang diminta. Kalau tidak dibalas, kamu bisa berubah dingin mendadak tanpa menjelaskan apa-apa.",
        "when_strong": "劫財 berlimpah menarik persaingan dari lingkaran terdekat, bukan dari orang asing. Buat perjanjian tertulis justru untuk hal yang kamu anggap sepele karena sudah kenal.",
        "when_weak": "劫財 yang tipis bikin kamu terlalu berhitung sampai melewatkan kesempatan yang sebenarnya layak diambil. Sesekali putuskan tanpa menunggu semua datanya lengkap.",
    },
    "shi_shen": {
        "name_cn": "食神",
        "name_id": "Dewa Penikmat",
        "essence": "Kamu mengolah isi kepalamu jadi sesuatu yang bisa dinikmati orang lain — tulisan, masakan, rancangan, obrolan. Prosesnya kamu nikmati, bukan cuma hasilnya. Energi ini yang bikin hidupmu terasa lapang meski isinya biasa saja.",
        "in_career": "Bidang yang menuntut rasa dan kesabaran cocok denganmu: kuliner, desain, perawatan, apa pun yang hasilnya dirasakan langsung. Target yang dikejar tergesa justru menurunkan mutu kerjamu.",
        "in_wealth": "Rezekimu datang dari keahlian yang kamu asah pelan-pelan, bukan dari lompatan besar. Makin kamu dikenal karena satu hal spesifik, makin stabil pemasukanmu.",
        "in_love": "Kamu menunjukkan sayang lewat hal kecil yang dikerjakan konsisten, bukan lewat kata-kata besar. Pasangan yang tidak peka pada detail akan merasa kamu datar.",
        "when_strong": "食神 yang berlimpah bikin kamu terlalu betah di zona nyaman dan menunda apa pun yang tidak menyenangkan. Pasang tenggat dari luar, jangan dari dirimu sendiri.",
        "when_weak": "食神 yang tipis bikin kamu sulit menyalurkan apa yang kamu rasakan sampai menumpuk di dalam. Pilih satu saluran — apa pun bentuknya — lalu pakai rutin.",
    },
    "shang_guan": {
        "name_cn": "傷官",
        "name_id": "Pelukai Pejabat",
        "essence": "Kamu melihat celah yang orang lain lewatkan dan sulit menahan diri untuk tidak menyebutkannya. Bakatmu nyata, begitu juga gesekan yang kamu timbulkan. Aturan yang tidak masuk akal terasa seperti penghinaan pribadi buatmu.",
        "in_career": "Kamu cocok di tempat yang menghargai hasil di atas prosedur: kreatif, riset, analisis, apa pun yang dinilai dari mutunya. Atasan yang butuh dihormati tanpa alasan akan jadi sumber masalahmu.",
        "in_wealth": "Uangmu mengalir deras saat kemampuanmu diakui, dan berhenti mendadak saat kamu bertengkar dengan pemegang keputusan. Jaga hubungan dengan pintunya, bukan cuma dengan pekerjaannya.",
        "in_love": "Kamu jujur sampai ke titik yang menyakitkan dan menganggap itu bentuk penghormatan. Tidak semua orang membacanya begitu.",
        "when_strong": "傷官 berlebih bikin kamu membakar jembatan yang masih kamu butuhkan. Tahan satu hari sebelum mengirim kritik yang sudah tersusun rapi di kepalamu.",
        "when_weak": "傷官 yang tipis bikin kamu menelan pendapat sendiri demi suasana yang aman. Mulai dari menyampaikan satu ketidaksetujuan kecil tiap minggu.",
    },
    "pian_cai": {
        "name_cn": "偏財",
        "name_id": "Harta Tak Terduga",
        "essence": "Kamu punya penciuman tajam untuk peluang dan jaringan yang meluas tanpa perlu diusahakan keras. Uang datang dari arah yang tidak direncanakan. Yang sulit buatmu bukan mencarinya, tapi menahannya.",
        "in_career": "Penjualan, kemitraan, usaha sampingan — apa pun yang hasilnya diukur dari gerak, di situ kamu hidup. Meja yang sama selama bertahun-tahun akan mematikan sebagian dirimu.",
        "in_wealth": "Kamu bisa membaca kapan sesuatu sedang naik, tapi sering lupa kapan harus keluar. Tetapkan angka jual sebelum masuk, bukan sesudah.",
        "in_love": "Kamu murah hati dan gampang disukai, kadang lebih dari yang kamu sadari. Batas antara ramah dan memberi harapan perlu kamu gambar sendiri.",
        "when_strong": "偏財 berlimpah bikin kamu mengejar banyak hal sekaligus sampai tidak ada satu pun yang selesai. Pilih dua, lepaskan sisanya tanpa menyimpan penyesalan.",
        "when_weak": "偏財 yang tipis bikin peluang lewat karena kamu menunggu kepastian yang tidak pernah datang. Sediakan dana kecil yang memang disiapkan untuk dicoba dan boleh hilang.",
    },
    "zheng_cai": {
        "name_cn": "正財",
        "name_id": "Harta Sah",
        "essence": "Kamu percaya uang adalah hasil yang bisa dihitung dari kerja yang bisa dihitung. Kamu tidak silau pada jalan pintas, dan itu menyelamatkanmu berkali-kali. Sisi beratnya: kamu bisa terlalu lama bertahan di tempat yang aman tapi sudah habis.",
        "in_career": "Peran yang menuntut ketelitian dan tanggung jawab jangka panjang cocok denganmu — keuangan, operasional, apa pun yang salahnya mahal. Kamu dipercaya karena jarang meleset.",
        "in_wealth": "Kekayaanmu bertumpuk dari selisih kecil yang konsisten, bukan dari satu kemenangan besar. Itu lambat, dan justru di situ kekuatannya.",
        "in_love": "Kamu menunjukkan komitmen lewat hal yang bisa diandalkan: hadir tepat waktu, ingat janji, ikut menanggung. Hubungan yang menuntut kejutan terus-menerus bikin kamu kurang nyaman.",
        "when_strong": "正財 yang menumpuk bikin kamu menghitung segala sesuatu, termasuk yang seharusnya diberikan tanpa dihitung. Sediakan pos pengeluaran yang memang tidak perlu dipertanggungjawabkan.",
        "when_weak": "正財 yang tipis bikin pemasukanmu naik turun tanpa pola. Bangun satu sumber tetap dulu, sekecil apa pun, sebelum mengejar yang besar.",
    },
    "qi_sha": {
        "name_cn": "七殺",
        "name_id": "Tujuh Pembunuh",
        "essence": "Kamu tumbuh paling cepat saat sedang ditekan. Situasi yang bikin orang lain beku justru menajamkan caramu berpikir. Masalahnya, kamu jadi terbiasa mencari tekanan itu bahkan saat tidak diperlukan.",
        "in_career": "Kamu berguna di tempat yang sedang berantakan: pembenahan, penanganan krisis, tim yang perlu dirapikan. Di situasi yang sudah tenang, kamu bisa tanpa sadar menciptakan keributannya sendiri.",
        "in_wealth": "Pemasukan besarmu biasanya datang dari pekerjaan yang orang lain hindari karena berat. Pastikan risikonya kamu ambil dengan sadar, bukan karena dorongan adrenalin.",
        "in_love": "Kamu intens dan protektif. Itu bisa terasa seperti dilindungi atau seperti dikurung, tergantung siapa yang menerimanya — tanyakan yang mana yang dirasakan pasanganmu.",
        "when_strong": "七殺 berlebih membuat hidupmu berjalan dari satu keadaan darurat ke darurat berikutnya sampai badanmu yang menagih. Jadwalkan istirahat sebagai kewajiban, bukan hadiah.",
        "when_weak": "七殺 yang tipis bikin kamu menghindari konfrontasi sampai masalah kecil membesar sendiri. Selesaikan satu hal yang sudah kamu tunda, minggu ini juga.",
    },
    "zheng_guan": {
        "name_cn": "正官",
        "name_id": "Pejabat Sah",
        "essence": "Kamu nyaman di dalam aturan yang jelas dan terganggu saat ada yang menyerobot. Nama baik buatmu bukan gengsi, tapi modal kerja. Kamu menahan diri di banyak hal karena memikirkan bagaimana itu akan terbaca orang.",
        "in_career": "Jalur berjenjang cocok denganmu: institusi, pemerintahan, korporasi, profesi berlisensi. Kamu naik pelan tapi jarang turun.",
        "in_wealth": "Uangmu terikat pada posisi dan reputasi, jadi menjaga keduanya sama dengan menjaga pemasukan. Jangan taruh seluruh masa depanmu di satu jabatan.",
        "in_love": "Kamu serius sejak awal dan tidak suka hubungan yang statusnya menggantung. Pasangan yang santai soal kepastian bikin kamu diam-diam gelisah.",
        "when_strong": "正官 yang menumpuk bikin kamu mengikat diri pada standar yang bahkan tidak ada yang menuntut. Periksa mana aturan yang nyata dan mana yang kamu buat sendiri.",
        "when_weak": "正官 yang tipis bikin kamu sulit konsisten pada komitmen yang sudah kamu buat. Kurangi jumlah janjinya, bukan mutu menepatinya.",
    },
    "pian_yin": {
        "name_cn": "偏印",
        "name_id": "Penopang Miring",
        "essence": "Kamu belajar dengan cara yang tidak biasa dan sering paham sebelum bisa menjelaskan kenapa. Ketertarikanmu jatuh ke hal yang orang lain anggap terlalu dalam atau terlalu aneh. Kamu betah sendirian jauh lebih lama dari kebanyakan orang.",
        "in_career": "Riset, spesialisasi sempit, bidang teknis atau spiritual — di situ caramu berpikir jadi nilai lebih. Pekerjaan yang menuntut basa-basi terus-menerus menguras energimu.",
        "in_wealth": "Rezekimu datang dari pengetahuan yang sedikit orang punya, bukan dari banyaknya pelanggan. Beranikan diri memasang harga sesuai kelangkaannya.",
        "in_love": "Kamu butuh ruang, dan orang sering salah membacanya sebagai tidak tertarik. Sampaikan kebutuhan itu di awal, sebelum jadi salah paham yang panjang.",
        "when_strong": "偏印 berlebih bikin kamu berpikir terus tanpa pernah masuk ke tindakan, dan makin lama makin menjauh dari orang. Tetapkan satu hal yang harus keluar dari kepalamu jadi nyata minggu ini.",
        "when_weak": "偏印 yang tipis bikin kamu mudah percaya penjelasan pertama yang kamu dengar. Biasakan mencari satu sumber pembanding sebelum mengambil sikap.",
    },
    "zheng_yin": {
        "name_cn": "正印",
        "name_id": "Penopang Sah",
        "essence": "Kamu punya sandaran — orang, ilmu, atau keyakinan — yang bikin kamu tidak gampang goyah. Merawat sesuatu terasa alami buatmu. Yang perlu diwaspadai: sandaran yang terlalu nyaman bisa jadi alasan untuk tidak pernah berangkat.",
        "in_career": "Pendidikan, kesehatan, penelitian, pendampingan — bidang yang inti kerjanya menumbuhkan orang lain. Pengakuan datang lambat tapi bertahan lama.",
        "in_wealth": "Kamu jarang kekurangan karena selalu ada yang menopang, dan justru itu yang bikin kamu menunda mandiri secara finansial. Hitung berapa lama kamu sanggup bertahan tanpa bantuan siapa pun.",
        "in_love": "Kamu merawat pasangan seperti merawat rumah: telaten dan tanpa banyak diminta. Hati-hati memposisikan diri sebagai orang tua, bukan sebagai pasangan.",
        "when_strong": "正印 yang menumpuk bikin kamu terlalu lama bersiap dan tidak pernah merasa cukup ilmu untuk mulai. Tetapkan tanggal mulai sebelum merasa siap.",
        "when_weak": "正印 yang tipis bikin kamu berjalan tanpa penopang dan cepat habis. Cari satu orang yang bisa kamu hubungi saat buntu, lalu benar-benar hubungi.",
    },
}


WUXING_ANALYSIS_BANK = {
    ("kayu", "dominan"): {
        "status_label": "Kayu Mendominasi 🌳",
        "impact": "Dorongan untuk tumbuh dan memulai ada terus di kepalamu, sampai yang sudah berjalan kurang kamu rawat. Kamu membuka banyak hal dan meninggalkan sebagiannya setengah jadi.",
        "remedy": "Logam yang memangkas dan Api yang menyalurkan adalah pereda alaminya: tetapkan batas, potong yang tidak jalan, lalu keluarkan sisanya jadi karya.",
    },
    ("kayu", "lemah"): {
        "status_label": "Kayu Menipis 🌱",
        "impact": "Kamu punya rencana tapi tenaganya cepat habis sebelum jadi. Keberanian memulai sesuatu yang benar-benar baru terasa mahal buatmu.",
        "remedy": "Air menghidupi Kayu: tambah bacaan, guru, dan lingkungan yang menantangmu berpikir. Mulai dari target kecil yang punya tenggat jelas.",
    },
    ("kayu", "kosong"): {
        "status_label": "Kayu Tidak Muncul 🍂",
        "impact": "Tidak ada dorongan alami untuk melangkah ke hal yang belum pasti; kamu menunggu semuanya jelas dulu. Pertumbuhan datang dari luar, bukan dari dalam dirimu.",
        "remedy": "Titipkan pertumbuhanmu pada struktur: kelas berjadwal, mentor, komunitas yang memaksa gerak. Warna hijau, arah timur, dan ruang berpohon membantu di tingkat kebiasaan.",
    },
    ("kayu", "seimbang"): {
        "status_label": "Kayu Seimbang 🌿",
        "impact": "Dorongan untuk tumbuh muncul tanpa perlu dipancing, dan kamu masih sanggup merawat yang sudah berjalan. Hal baru kamu buka dengan takaran yang tidak mengorbankan yang lama.",
        "remedy": "Tidak ada yang perlu ditambal. Jaga iramanya: satu hal baru dalam satu waktu, dan pastikan yang lama sudah bisa berdiri sendiri sebelum kamu membuka berikutnya.",
    },
    ("api", "dominan"): {
        "status_label": "Api Mendominasi 🔥",
        "impact": "Kamu cepat terbakar oleh hal baru dan sama cepatnya kehilangan minat. Emosimu terbaca jelas dari luar, termasuk saat kamu tidak ingin terbaca.",
        "remedy": "Air menyeimbangkan Api: tidur cukup, hening yang dijadwalkan, dan orang yang berani meredammu. Tanah juga menyerap — salurkan panasnya ke pekerjaan yang butuh ketekunan.",
    },
    ("api", "lemah"): {
        "status_label": "Api Meredup 🕯️",
        "impact": "Gairahmu naik turun dan sulit dipanggil saat dibutuhkan. Kamu tahu apa yang harus dikerjakan, tapi dorongannya tidak kunjung datang.",
        "remedy": "Kayu menghidupi Api: cari alasan yang lebih besar dari sekadar target. Olahraga pagi, cahaya matahari, dan lingkaran orang bersemangat menaikkannya cepat.",
    },
    ("api", "kosong"): {
        "status_label": "Api Tidak Muncul 🌫️",
        "impact": "Kamu sulit menunjukkan antusiasme meski sebenarnya tertarik, dan orang salah membacanya sebagai tidak peduli. Pengakuan jarang datang karena kamu tidak terlihat.",
        "remedy": "Bangun dari luar: satu kegiatan rutin yang menempatkanmu di depan orang. Warna merah, arah selatan, dan kehangatan fisik membantu mengganjalnya.",
    },
    ("api", "seimbang"): {
        "status_label": "Api Seimbang 🔥",
        "impact": "Semangatmu bisa dipanggil saat dibutuhkan dan mereda saat tidak. Orang membaca perasaanmu secukupnya — cukup untuk dipercaya, tidak sampai kamu kehilangan ruang pribadi.",
        "remedy": "Rawat lewat hal sederhana: jam tidur yang teratur dan satu kegiatan yang kamu kerjakan karena suka, bukan karena target. Api yang stabil lebih sulit dijaga daripada dinyalakan.",
    },
    ("tanah", "dominan"): {
        "status_label": "Tanah Mendominasi ⛰️",
        "impact": "Kamu memikul terlalu banyak dan sulit melepaskan, sampai gerakmu melambat. Rasa tanggung jawab yang berlebih bikin kamu menunda hal yang kamu inginkan sendiri.",
        "remedy": "Kayu menembus Tanah: masukkan hal baru yang sengaja mengganggu rutinitasmu. Logam menguras kelebihannya — ubah beban jadi hasil yang bisa diserahkan.",
    },
    ("tanah", "lemah"): {
        "status_label": "Tanah Menipis 🏜️",
        "impact": "Pijakanmu goyah: rencana berubah, tempat berubah, rasa amanmu ikut naik turun. Kamu sulit menahan sesuatu dalam waktu lama.",
        "remedy": "Api menghidupi Tanah: satu tujuan yang benar-benar kamu percayai akan memadatkan pijakanmu. Rutinitas harian yang sama tiap hari bekerja lebih baik daripada rencana besar.",
    },
    ("tanah", "kosong"): {
        "status_label": "Tanah Tidak Muncul 🌪️",
        "impact": "Tidak ada penahan alami di chart-mu, jadi apa yang masuk gampang juga keluar. Komitmen jangka panjang terasa lebih berat buatmu dibanding orang lain.",
        "remedy": "Bangun penahan di luar dirimu: kontrak, jadwal tetap, tempat tinggal yang tidak berpindah. Warna cokelat, arah tengah, dan kebiasaan yang diulang membentuk apa yang tidak ada di bawaanmu.",
    },
    ("tanah", "seimbang"): {
        "status_label": "Tanah Seimbang ⛰️",
        "impact": "Kamu bisa diandalkan tanpa berakhir menanggung semuanya. Yang kamu janjikan biasanya ditepati, dan kamu masih tahu kapan harus menolak.",
        "remedy": "Kuncinya menjaga batas tetap jelas: catat apa yang kamu sanggupi, bukan apa yang ingin kamu sanggupi. Tanah yang cukup mudah bertambah diam-diam kalau kamu terus mengiyakan.",
    },
    ("logam", "dominan"): {
        "status_label": "Logam Mendominasi ⚙️",
        "impact": "Kamu memangkas terlalu cepat — orang, rencana, kemungkinan — sebelum sempat matang. Standarmu tinggi dan itu bikin lingkaranmu menyempit sendiri.",
        "remedy": "Api melunakkan Logam: masukkan hal yang menghangatkan dan tidak perlu diukur. Air menyalurkan ketajamanmu — pakai untuk menganalisis, bukan untuk menghakimi.",
    },
    ("logam", "lemah"): {
        "status_label": "Logam Menumpul 🔩",
        "impact": "Kamu sulit menetapkan batas dan menunda keputusan yang tidak enak. Pekerjaan yang butuh ketegasan terasa lebih berat dari yang seharusnya.",
        "remedy": "Tanah menghasilkan Logam: kumpulkan dulu fakta dan pengalaman sampai kamu punya dasar untuk bersikap. Latih menolak satu permintaan tiap minggu.",
    },
    ("logam", "kosong"): {
        "status_label": "Logam Tidak Muncul 🫧",
        "impact": "Struktur dan ketegasan tidak datang sendiri buatmu; semuanya terasa masih bisa dinegosiasi. Kamu bertahan pada hal yang sebenarnya sudah selesai.",
        "remedy": "Pinjam ketegasan dari sistem: aturan tertulis, tenggat yang tidak bisa digeser, orang yang berani menagih. Warna putih, arah barat, dan ruang yang rapi memperkuatnya.",
    },
    ("logam", "seimbang"): {
        "status_label": "Logam Seimbang ⚔️",
        "impact": "Kamu sanggup memutuskan dan memangkas tanpa menjadi kaku. Standarmu jelas, tapi masih tersisa ruang untuk orang yang belum sampai ke sana.",
        "remedy": "Yang menjaganya tetap pas adalah kebiasaan meninjau ulang aturan yang kamu buat sendiri. Logam yang tak pernah diasah jadi tumpul, yang diasah terus-menerus jadi melukai.",
    },
    ("air", "dominan"): {
        "status_label": "Air Mendominasi 🌊",
        "impact": "Pikiranmu jalan terus dan sulit dihentikan, termasuk saat kamu ingin tidur. Kamu melihat terlalu banyak kemungkinan sampai memilih jadi pekerjaan tersendiri.",
        "remedy": "Tanah membendung Air: buat batas yang jelas — daftar pendek, satu prioritas, jam kerja yang ditutup. Kayu menyalurkan — ubah pikiran jadi karya yang bisa dilihat orang.",
    },
    ("air", "lemah"): {
        "status_label": "Air Menyusut 💧",
        "impact": "Kamu cepat kering: ide macet, badan capek, kelenturan berpikirmu berkurang. Situasi tak terduga bikin kamu lebih kaku dari biasanya.",
        "remedy": "Logam menghasilkan Air: rapikan dulu yang berantakan supaya ada ruang untuk berpikir. Tidur, air minum, dan waktu sendiri bukan kemewahan buat chart-mu.",
    },
    ("air", "kosong"): {
        "status_label": "Air Tidak Muncul 🏺",
        "impact": "Kamu jalan lurus tanpa banyak menimbang alternatif, dan itu bisa berarti tegas atau berarti kaku. Berhadapan dengan hal yang tidak pasti terasa tidak nyaman.",
        "remedy": "Cari kelenturan dari luar: orang yang berpikir beda, perjalanan, bacaan di luar bidangmu. Warna hitam atau biru tua, arah utara, dan dekat air membantu.",
    },
    ("air", "seimbang"): {
        "status_label": "Air Seimbang 💧",
        "impact": "Kamu berpikir dulu sebelum bergerak tanpa tenggelam di dalamnya. Menyerap hal baru terasa wajar, dan kamu masih bisa berhenti menimbang saat waktunya bertindak.",
        "remedy": "Jaga alirannya dengan mengeluarkan, bukan cuma menyerap: ajarkan, tuliskan, atau ceritakan apa yang kamu pelajari. Air yang tidak mengalir keluar berakhir menggenang.",
    },
}


WUXING_ROLE_BANK = {
    ("dominan", "menguntungkan"): {
        "verdict": "Elemen ini menumpuk, dan kebetulan memang inilah yang kamu butuhkan.",
        "action": "Sandarkan keputusan besarmu ke sini: pilihan karir, arah belajar, sampai lingkungan tempat tinggal. Yang perlu dijaga cuma satu — jangan sampai ini jadi satu-satunya yang kamu punya.",
    },
    ("dominan", "merugikan"): {
        "verdict": "Elemen ini paling banyak di chart-mu, tapi justru inilah yang membebani.",
        "action": "Kurangi paparannya di hal yang masih bisa kamu atur, lalu perkuat elemen yang mengekangnya. Menambah lagi yang sudah berlebih cuma memperbesar tekanannya.",
    },
    ("lemah", "menguntungkan"): {
        "verdict": "Elemen yang paling kamu butuhkan ternyata yang paling tipis — ini titik paling layak dibenahi.",
        "action": "Jadikan prioritas nomor satu: tambah lewat warna, arah, kebiasaan, dan pilihan lingkungan. Kenaikan kecil di sini terasa lebih besar dibanding perbaikan mana pun.",
    },
    ("lemah", "merugikan"): {
        "verdict": "Elemen yang membebanimu kebetulan memang tipis, jadi tidak perlu diapa-apakan.",
        "action": "Biarkan apa adanya dan jangan tergoda melengkapi chart supaya kelihatan rapi. Alihkan tenaganya ke elemen yang menguntungkan.",
    },
    ("kosong", "menguntungkan"): {
        "verdict": "Elemen yang kamu butuhkan sama sekali tidak muncul di empat pilarmu.",
        "action": "Inilah yang paling menentukan: bangun dari luar chart — lingkungan, pasangan, bidang kerja, kebiasaan harian. Periode 大運 yang membawa elemen ini biasanya jadi titik balik hidupmu.",
    },
    ("kosong", "merugikan"): {
        "verdict": "Elemen ini tidak ada sama sekali, dan itu justru melegakan — dia bukan sekutumu.",
        "action": "Tidak ada yang perlu dikejar di sini. Kosong bukan berarti kurang; dalam kasusmu, itu satu beban yang tidak perlu kamu pikul.",
    },
    ("seimbang", "menguntungkan"): {
        "verdict": "Elemen yang kamu butuhkan hadir dalam takaran yang pas — ini kondisi paling enak yang bisa dimiliki sebuah chart.",
        "action": "Tugasmu cuma menjaganya. Kenali kebiasaan dan lingkungan yang membuatnya stabil, lalu jangan diubah tanpa alasan yang kuat.",
    },
    ("seimbang", "merugikan"): {
        "verdict": "Elemen ini termasuk yang membebanimu, tapi jumlahnya masih terkendali.",
        "action": "Belum perlu tindakan khusus. Cukup awasi supaya tidak menumpuk, terutama saat periode 大運 kebetulan menambah elemen ini.",
    },
    ("seimbang", "netral"): {
        "verdict": "Elemen ini ada secukupnya dan tidak menarik chart-mu ke arah mana pun.",
        "action": "Tidak ada yang perlu ditambah maupun dikurangi. Biarkan jadi latar; tenagamu lebih berguna di elemen yang jelas menguntungkan atau jelas membebani.",
    },
    ("dominan", "netral"): {
        "verdict": "Elemen ini paling banyak di chart-mu, tapi tidak masuk hitungan yang menguntungkan maupun yang membebani.",
        "action": "Anggap ini watak bawaan, bukan masalah yang harus dibereskan. Yang perlu diawasi satu saja: jangan sampai porsinya yang besar menyisihkan elemen yang benar-benar kamu butuhkan.",
    },
    ("lemah", "netral"): {
        "verdict": "Elemen ini tipis, dan kebetulan memang bukan penentu arah chart-mu.",
        "action": "Biarkan apa adanya. Melengkapi yang tipis cuma karena terlihat kurang adalah cara tercepat menghabiskan tenaga untuk sesuatu yang tidak mengubah apa pun.",
    },
    ("kosong", "netral"): {
        "verdict": "Elemen ini tidak muncul sama sekali, dan ketiadaannya tidak menguntungkan maupun merugikanmu.",
        "action": "Tidak ada yang perlu dikejar di sini. Kalau suatu saat elemen ini datang lewat 大運 atau lingkungan baru, terima sebagai warna tambahan, bukan sebagai perbaikan.",
    },
}


DESTINY_CAREER_BANK = {
    "bi_jian": {
        "archetype": "Sang Pekerja Mandiri",
        "ideal_fields": [
            "Usaha sendiri berskala kecil sampai menengah",
            "Profesi lepas dengan klien langsung",
            "Olahraga dan bidang yang dinilai dari performa",
            "Pekerjaan teknis yang dikerjakan sendirian",
            "Kemitraan dengan porsi yang dipisah jelas",
            "Pelatihan dan pendampingan satu lawan satu",
        ],
        "work_style": "Kamu bekerja paling cepat saat batas wewenangmu jelas dan tidak ada yang mengintip tiap langkah. Laporan berlapis dan rapat yang tidak memutuskan apa-apa menguras semangatmu lebih cepat daripada bebannya sendiri.",
        "warning": "Kamu mudah menganggap rekan setara sebagai pesaing, padahal justru dialah yang bisa meringankan. Bedakan mana persaingan sungguhan dan mana cuma ego.",
    },
    "jie_cai": {
        "archetype": "Sang Penggerak Bermodal Nekat",
        "ideal_fields": [
            "Usaha rintisan yang perputarannya cepat",
            "Penjualan lapangan dengan target agresif",
            "Hiburan dan penyelenggaraan acara",
            "Perdagangan yang menuntut berani ambil stok",
            "Olahraga tim dan manajemen atlet",
            "Pekerjaan lapangan yang penuh ketidakpastian",
        ],
        "work_style": "Kamu berangkat duluan lalu memikirkan detailnya di jalan, dan cukup sering itu berhasil. Orang ikut karena kamu terlihat yakin, bahkan di saat kamu sendiri belum yakin.",
        "warning": "Uang dan wewenang yang dipegang bareng teman adalah titik rawan terbesarmu. Hitam di atas putih sejak awal, sebelum ada yang perlu dipersoalkan.",
    },
    "shi_shen": {
        "archetype": "Sang Pengolah Rasa",
        "ideal_fields": [
            "Kuliner dan pengolahan makanan",
            "Desain produk dan kemasan",
            "Penulisan santai dan konten harian",
            "Perawatan tubuh dan kebugaran",
            "Pendidikan anak usia dini",
            "Kerajinan tangan dan produk buatan sendiri",
        ],
        "work_style": "Kamu butuh ruang untuk mengerjakan sesuatu sampai rasanya pas, bukan sampai tenggatnya lewat. Mutu kerjamu naik tajam saat kamu menikmati prosesnya dan turun tajam saat dipaksa.",
        "warning": "Kamu bisa terlalu lama di tempat yang nyaman sampai nilai pasarmu tertinggal. Periksa tiap tahun: kamu masih tumbuh, atau cuma betah?",
    },
    "shang_guan": {
        "archetype": "Sang Pembongkar Aturan",
        "ideal_fields": [
            "Industri kreatif dan periklanan",
            "Jurnalisme dan penulisan opini",
            "Riset yang menantang kesimpulan lama",
            "Pertunjukan, komedi, dan panggung",
            "Konsultan yang memang dibayar untuk mengkritik",
            "Pengembangan produk yang pasarnya belum ada",
        ],
        "work_style": "Kamu bekerja demi hasil yang bisa kamu banggakan, bukan demi prosedur yang bisa dipertanggungjawabkan. Begitu dipercaya penuh, hasilmu sering jauh di atas rata-rata.",
        "warning": "Karirmu lebih sering terhenti oleh gesekan dengan atasan daripada oleh kurangnya kemampuan. Simpan satu orang di dalam sistem yang bisa jadi penerjemahmu.",
    },
    "pian_cai": {
        "archetype": "Sang Pemburu Peluang",
        "ideal_fields": [
            "Perdagangan dan distribusi",
            "Properti dan aset yang bisa diputar",
            "Kemitraan bisnis lintas bidang",
            "Pemasaran dan pembukaan pasar baru",
            "Usaha sampingan yang berjalan paralel",
            "Pengelolaan modal dan investasi",
        ],
        "work_style": "Kamu menangkap peluang lebih cepat dari orang di sekitarmu dan tidak keberatan menjalankan beberapa hal sekaligus. Gaji tetap terasa membatasi buatmu, bukan mengamankan.",
        "warning": "Yang menjatuhkanmu bukan kurangnya peluang, tapi tidak tahu kapan berhenti. Tentukan batas rugi sebelum masuk, bukan sesudah.",
    },
    "zheng_cai": {
        "archetype": "Sang Penjaga Neraca",
        "ideal_fields": [
            "Akuntansi dan keuangan",
            "Operasional dan rantai pasok",
            "Perbankan dan asuransi",
            "Administrasi yang menuntut ketelitian",
            "Pengadaan dan pengendalian biaya",
            "Usaha keluarga yang diteruskan",
        ],
        "work_style": "Kamu mengerjakan sesuatu sampai angkanya benar-benar cocok, bukan sampai kelihatan cocok. Orang menaruh hal penting padamu karena kamu jarang bikin kejutan.",
        "warning": "Kamu bisa bertahan bertahun-tahun di tempat yang sudah berhenti menumbuhkanmu demi rasa aman. Aman dan mandek beda tipis — periksa tiap dua tahun.",
    },
    "qi_sha": {
        "archetype": "Sang Pembenah Keadaan",
        "ideal_fields": [
            "Penanganan krisis dan pemulihan usaha",
            "Keamanan, kemiliteran, dan penegakan hukum",
            "Bedah dan kedokteran gawat darurat",
            "Manajemen proyek berisiko tinggi",
            "Negosiasi keras dan penagihan",
            "Usaha di pasar yang sudah padat",
        ],
        "work_style": "Kamu jalan paling kencang saat ada yang harus diselamatkan dan waktunya mepet. Keadaan yang tenang justru bikin fokusmu buyar.",
        "warning": "Kamu cenderung menerima beban melebihi yang sanggup ditanggung badanmu. Batas fisik itu nyata, dan biasanya dia menagih di waktu paling buruk.",
    },
    "zheng_guan": {
        "archetype": "Sang Pemangku Jabatan",
        "ideal_fields": [
            "Pemerintahan dan pelayanan publik",
            "Korporasi dengan jenjang karir yang jelas",
            "Hukum dan kepatuhan",
            "Pendidikan formal dan dunia akademik",
            "Profesi berlisensi",
            "Tata kelola dan audit internal",
        ],
        "work_style": "Kamu bekerja sesuai aturan main dan berharap orang lain begitu juga. Kenaikanmu pelan tapi jarang terputus, karena reputasimu ikut naik bersamanya.",
        "warning": "Kalau seluruh hidupmu menempel pada satu jabatan, kehilangan jabatan terasa seperti kehilangan diri. Bangun sesuatu di luar kantor sejak sekarang.",
    },
    "pian_yin": {
        "archetype": "Sang Pendalam Bidang Sempit",
        "ideal_fields": [
            "Riset dan pengembangan",
            "Bidang teknis yang sangat khusus",
            "Psikologi, konseling, dan terapi",
            "Kajian agama, filsafat, dan metafisika",
            "Pengarsipan, sejarah, dan kurasi",
            "Analisis data dan investigasi",
        ],
        "work_style": "Kamu butuh waktu sendiri yang panjang untuk sampai ke kesimpulan yang berbobot. Rapat beruntun dan basa-basi justru memotong bagian paling produktif dari harimu.",
        "warning": "Kamu bisa terus bersiap tanpa pernah merilis apa pun. Tetapkan bentuk keluaran dan tanggalnya sejak awal, bahkan sebelum risetnya tuntas.",
    },
    "zheng_yin": {
        "archetype": "Sang Penumbuh Orang",
        "ideal_fields": [
            "Pendidikan dan pelatihan",
            "Kesehatan dan perawatan",
            "Sumber daya manusia dan pengembangan tim",
            "Lembaga sosial dan yayasan",
            "Penerbitan dan penyuntingan",
            "Pendampingan dan supervisi",
        ],
        "work_style": "Kamu mengukur keberhasilan dari seberapa berkembang orang di sekitarmu, bukan dari angka di namamu sendiri. Itu bikin kamu dipercaya, sekaligus bikin kamu sering tidak terlihat.",
        "warning": "Kamu terlalu lama merasa belum cukup ilmu untuk naik ke peran yang lebih besar. Ambil dulu, ilmunya menyusul di jalan.",
    },
}


DESTINY_WEALTH_BANK = {
    "bi_jian": {
        "wealth_type": "Rezeki Hasil Keringat Sendiri",
        "investment_advice": "Taruh uangmu di hal yang kamu pahami dan bisa kamu kendalikan sendiri — alat kerja, keahlian, usaha yang kamu jalankan. Produk yang pengelolaannya diserahkan penuh ke orang lain jarang cocok dengan caramu.",
        "financial_trap": "Patungan dengan teman yang porsinya dibagi sama rata tapi kerjanya tidak. Itu yang paling sering menguras uang sekaligus hubungannya.",
        "lucky_period": "Periode 大運 yang membawa elemen penyalur — tenagamu akhirnya menemukan muaranya jadi uang.",
    },
    "jie_cai": {
        "wealth_type": "Rezeki Deras yang Bocor Halus",
        "investment_advice": "Kunci dulu sebagian di tempat yang tidak bisa kamu cairkan sewaktu-waktu, baru sisanya boleh diputar. Tanpa penguncian, apa pun yang masuk akan menemukan jalan keluarnya.",
        "financial_trap": "Meminjamkan karena tidak enak hati lalu tidak berani menagih. Coba hitung semua pinjaman yang kamu berikan tahun lalu — angkanya biasanya mengejutkan.",
        "lucky_period": "Saat elemen penertib menguat, kebocoranmu berhenti sendiri tanpa kamu harus berhemat mati-matian.",
    },
    "shi_shen": {
        "wealth_type": "Rezeki dari Karya yang Diasah",
        "investment_advice": "Modal terbaikmu adalah memperbaiki mutu lalu menaikkan harga, bukan memperbanyak jumlah. Satu produk yang sangat bagus mengalahkan lima yang biasa saja.",
        "financial_trap": "Memasang harga kemurahan karena sungkan, padahal hasilnya jelas di atas pasaran. Kamu menyubsidi pelanggan tanpa menyadarinya.",
        "lucky_period": "Begitu elemen harta masuk ke periodemu, karya yang selama ini cuma dipuji mulai dibeli.",
    },
    "shang_guan": {
        "wealth_type": "Rezeki Melonjak Saat Diakui",
        "investment_advice": "Bangun aset yang menempel pada namamu sendiri — karya, merek, portofolio — bukan yang menempel pada satu pemberi kerja. Penghasilanmu melonjak begitu namamu dikenal.",
        "financial_trap": "Pemasukanmu berhenti mendadak tiap kali kamu bergesekan dengan pemegang keputusan. Siapkan dana cadangan enam bulan, bukan tiga.",
        "lucky_period": "Fase harta adalah titik balikmu: bakat yang tadinya bikin ribut berubah jadi nilai jual.",
    },
    "pian_cai": {
        "wealth_type": "Rezeki Musiman dalam Jumlah Besar",
        "investment_advice": "Kamu boleh mengambil risiko, asal ukurannya ditetapkan di awal dan tidak digeser di tengah jalan. Pisahkan modal spekulasi dari dana hidup — sungguhan beda rekening.",
        "financial_trap": "Menahan posisi yang sudah untung karena merasa masih bisa naik lagi. Sebagian besar kerugianmu berawal dari keuntungan yang tidak diambil.",
        "lucky_period": "Periode yang menguatkan dirimu, karena harta sebesar itu butuh orang yang sanggup memegangnya.",
    },
    "zheng_cai": {
        "wealth_type": "Rezeki Tetap yang Menumpuk Pelan",
        "investment_advice": "Setoran rutin ke instrumen yang membosankan adalah senjata terkuatmu, justru karena kamu sanggup menjalaninya bertahun-tahun tanpa bosan. Jangan tergoda pindah ke yang serba cepat.",
        "financial_trap": "Terlalu hemat sampai melewatkan pengeluaran yang sebenarnya investasi: kesehatan, ilmu, dan alat kerja yang layak.",
        "lucky_period": "Fase yang menambah tenagamu sendiri — kemampuan menahan dan menumbuhkan harta ikut naik bersamanya.",
    },
    "qi_sha": {
        "wealth_type": "Rezeki dari Pekerjaan Berat",
        "investment_advice": "Ambil yang sepadan dengan risikonya, dan pastikan kamu paham risiko itu sampai ke dasarnya. Kamu tahan bertaruh, jadi yang perlu dijaga takarannya, bukan keberaniannya.",
        "financial_trap": "Memikul beban besar demi hasil cepat lalu membayarnya dengan kesehatan. Hitung ongkos badan sebagai bagian dari ongkos proyek.",
        "lucky_period": "Periode yang menopang dirimu; tekanan yang sama menghasilkan lebih banyak karena kamu jauh lebih tahan.",
    },
    "zheng_guan": {
        "wealth_type": "Rezeki yang Menempel pada Posisi",
        "investment_advice": "Bangun penghasilan yang tetap jalan meski jabatanmu tidak ada — sewa, dividen, atau usaha yang tidak menuntut kehadiranmu. Kedisiplinanmu sudah cukup, tinggal mulai.",
        "financial_trap": "Gaya hidup yang naik mengikuti jabatan, sehingga tabunganmu tidak pernah ikut naik. Kunci kenaikan gaji ke tabungan sebelum uangnya masuk rekening harian.",
        "lucky_period": "Biasanya berbarengan dengan naiknya posisi, saat elemen harta dan penopang diri datang bersamaan.",
    },
    "pian_yin": {
        "wealth_type": "Rezeki dari Keahlian Langka",
        "investment_advice": "Investasi terbaikmu adalah mendalami satu bidang sampai sedikit orang yang bisa menggantikanmu. Di titik itu, kamu yang menentukan harganya.",
        "financial_trap": "Memasang harga terlalu rendah karena menganggap yang kamu kuasai itu biasa saja. Bandingkan dengan pasar, bukan dengan perasaanmu sendiri.",
        "lucky_period": "Fase penyalur adalah panenmu — ilmu yang menumpuk bertahun-tahun keluar jadi karya yang dibayar.",
    },
    "zheng_yin": {
        "wealth_type": "Rezeki yang Selalu Ada Penopangnya",
        "investment_advice": "Mulai dari memisahkan uangmu dari uang keluarga, sekecil apa pun jumlahnya. Kemandirian finansialmu tertunda bukan karena tidak mampu, tapi karena tidak pernah terpaksa.",
        "financial_trap": "Terus-menerus menyubsidi orang lain sampai rencanamu sendiri tidak pernah kebagian dana. Tetapkan pagu bantuan per bulan.",
        "lucky_period": "Periode penyalur menandai saat kamu mulai menghasilkan sendiri, bukan lagi ditopang.",
    },
}


DESTINY_LOVE_BANK = {
    "bi_jian": {
        "love_type": "Cinta Dua Orang Mandiri",
        "ideal_partner_desc": "Orang yang punya pekerjaan, lingkaran, dan pendapat sendiri, sehingga tidak menuntut kamu mengisi seluruh harinya. Kamu justru makin sayang pada pasangan yang sesekali sibuk sendiri.",
        "red_flag": "Kamu bersaing dengan pasangan soal siapa yang lebih benar, padahal tidak ada yang sedang bertanding.",
        "peach_blossom_note": "Kamu menarik orang yang menghargai kemandirian, bukan yang sedang mencari tempat bersandar.",
    },
    "jie_cai": {
        "love_type": "Cinta yang Panas dan Cepat",
        "ideal_partner_desc": "Orang yang berani mengimbangi keberanianmu sekaligus cukup tenang untuk menahanmu. Kamu butuh yang bisa bilang tidak tanpa membuatmu merasa ditolak.",
        "red_flag": "Kamu memberi berlebihan di awal lalu menarik diri mendadak begitu merasa tidak dibalas.",
        "peach_blossom_note": "Kamu mudah didekati, dan sebagian datang karena keramaian yang kamu bawa, bukan karena kamu.",
    },
    "shi_shen": {
        "love_type": "Cinta yang Tumbuh Lewat Kebiasaan",
        "ideal_partner_desc": "Orang yang memperhatikan hal kecil dan mau tinggal cukup lama untuk melihat polanya. Kamu tidak cocok dengan yang mengejar intensitas terus-menerus.",
        "red_flag": "Kamu menghindari pembicaraan yang tidak enak demi menjaga suasana, sampai masalahnya terlalu tua untuk dibahas.",
        "peach_blossom_note": "Daya tarikmu tumbuh seiring waktu; orang jatuh hati setelah mengenal, bukan pada pandangan pertama.",
    },
    "shang_guan": {
        "love_type": "Cinta yang Jujurnya Tajam",
        "ideal_partner_desc": "Orang yang tidak gampang tersinggung dan bisa membalas argumenmu tanpa merasa diserang. Kamu perlu pasangan yang menganggap perdebatan sebagai bentuk perhatian.",
        "red_flag": "Kamu mengoreksi pasangan di depan orang lain dan menganggap itu hal yang biasa saja.",
        "peach_blossom_note": "Kamu menarik karena berani berkata apa adanya, dan alasan yang sama bikin sebagian orang menjauh.",
    },
    "pian_cai": {
        "love_type": "Cinta yang Ramah dan Luas",
        "ideal_partner_desc": "Orang yang percaya diri dan tidak gampang cemburu pada jaringan pertemananmu yang lebar. Kamu butuh kepercayaan yang tidak perlu dibuktikan ulang tiap hari.",
        "red_flag": "Kamu menyenangkan banyak orang sampai batasnya kabur, lalu heran kenapa pasanganmu curiga.",
        "peach_blossom_note": "Kesempatan datang lebih sering ke chart ini daripada rata-rata; yang menentukan bukan kesempatannya, tapi pilihanmu.",
    },
    "zheng_cai": {
        "love_type": "Cinta yang Dibangun Seperti Rumah",
        "ideal_partner_desc": "Orang yang serius soal rencana jangka panjang dan tidak menganggap kestabilan sebagai hal membosankan. Kamu nyaman dengan yang sepakat soal arah, bukan cuma soal rasa.",
        "red_flag": "Kamu menghitung siapa memberi apa sampai hubungan terasa seperti pembukuan.",
        "peach_blossom_note": "Kamu menarik orang yang sedang mencari kepastian, dan memang di situ kekuatan terbesarmu.",
    },
    "qi_sha": {
        "love_type": "Cinta yang Intens dan Menjaga",
        "ideal_partner_desc": "Orang yang tahan pada intensitasmu dan cukup kuat untuk tidak langsung mengalah. Pasangan yang terlalu penurut justru bikin kamu makin mendominasi tanpa sadar.",
        "red_flag": "Melindungi dan mengendalikan terasa sama saja dari dalam kepalamu, padahal tidak sama dari sisi pasanganmu.",
        "peach_blossom_note": "Kamu menarik karena terasa bisa diandalkan justru saat keadaan sedang genting.",
    },
    "zheng_guan": {
        "love_type": "Cinta dengan Status yang Jelas",
        "ideal_partner_desc": "Orang yang sama seriusnya soal komitmen dan tidak keberatan hubungan berjalan bertahap. Kamu tidak cocok dengan yang menggantungkan status tanpa alasan jelas.",
        "red_flag": "Kamu menahan banyak hal demi menjaga bagaimana hubunganmu terlihat dari luar.",
        "peach_blossom_note": "Kamu dianggap pilihan yang aman, dan sebagian orang mendekat justru karena alasan itu.",
    },
    "pian_yin": {
        "love_type": "Cinta yang Butuh Ruang Sunyi",
        "ideal_partner_desc": "Orang yang tidak panik saat kamu diam dan tidak membaca ruang sebagai penolakan. Kamu butuh yang punya kesibukan sendiri dan nyaman dengan keheningan.",
        "red_flag": "Kamu menarik diri saat sedang berat, persis di saat pasanganmu paling perlu tahu apa yang terjadi.",
        "peach_blossom_note": "Kamu menarik orang yang penasaran, karena kamu jarang membuka semuanya sekaligus.",
    },
    "zheng_yin": {
        "love_type": "Cinta yang Merawat",
        "ideal_partner_desc": "Orang yang bisa menerima perhatianmu tanpa jadi bergantung, dan sesekali balik merawatmu. Kamu perlu pasangan yang mengingatkan bahwa kamu juga boleh dilayani.",
        "red_flag": "Kamu memperlakukan pasangan seperti orang yang perlu dibimbing, bukan sebagai orang dewasa yang setara.",
        "peach_blossom_note": "Kamu menarik orang yang sedang lelah dan butuh tempat pulih — pastikan mereka tetap tinggal setelah pulih.",
    },
}


DESTINY_HEALTH_DAYMASTER = {
    "jia": {
        "energy_type": "Energi Batang Keras — kuat menahan, kurang lentur",
        "exercise_advice": "Latihan beban dan kegiatan luar ruang cocok karena tubuhmu minta dipakai, bukan dijaga. Tambahkan peregangan, sebab kekakuanmu biasanya muncul duluan di punggung dan leher.",
        "taboo": "Menahan kerja sampai tuntas padahal badan sudah minta berhenti. Kamu cenderung baru berhenti saat sudah patah, bukan saat capek.",
    },
    "yi": {
        "energy_type": "Energi Lentur — cepat pulih, gampang terpengaruh",
        "exercise_advice": "Yoga, jalan kaki jauh, dan berenang cocok karena tubuhmu lebih suka gerakan terus-menerus daripada beban berat. Konsistensi lebih penting buatmu daripada intensitas.",
        "taboo": "Begadang dan makan tidak teratur cepat terlihat di kondisimu. Tubuhmu memaafkan, tapi tidak melupakan.",
    },
    "bing": {
        "energy_type": "Energi Menyala — meledak besar, habis cepat",
        "exercise_advice": "Olahraga intens berdurasi pendek cocok: lari cepat, olahraga tim, latihan sirkuit. Yang justru perlu kamu tambah adalah pendinginan, bukan pemanasan.",
        "taboo": "Kurang tidur karena merasa masih bersemangat. Panas yang tidak diredam biasanya keluar jadi tekanan darah dan tidur yang berantakan.",
    },
    "ding": {
        "energy_type": "Energi Nyala Kecil — stabil tapi tipis cadangannya",
        "exercise_advice": "Latihan ringan yang rutin lebih cocok daripada sesi berat sesekali. Pernapasan dan peregangan malam membantu menurunkan pikiran yang masih menyala.",
        "taboo": "Memendam pikiran sampai jam tidurmu mundur terus. Sebagian keluhan fisikmu berawal dari kepala, bukan dari badan.",
    },
    "wu": {
        "energy_type": "Energi Padat — tahan lama, lambat bergerak",
        "exercise_advice": "Jalan cepat, naik bukit, dan latihan beban sedang cocok. Yang menentukan buatmu bukan beratnya, tapi tidak berhenti berminggu-minggu.",
        "taboo": "Duduk terlalu lama dan makan berlebih saat sedang banyak pikiran. Berat badan naik diam-diam justru di fase kamu paling sibuk.",
    },
    "ji": {
        "energy_type": "Energi Lembap — hangat tapi gampang lembek",
        "exercise_advice": "Gerakan ringan tiap hari lebih berguna daripada olahraga berat di akhir pekan. Pagi hari adalah waktu terbaikmu untuk bergerak.",
        "taboo": "Makan sambil memikirkan masalah. Pencernaanmu ikut menanggung apa yang kamu tahan di kepala.",
    },
    "geng": {
        "energy_type": "Energi Keras — kuat menghantam, mudah cedera",
        "exercise_advice": "Latihan kekuatan dan bela diri cocok dengan tabiatmu. Tambah pemanasan yang serius, karena kamu cenderung langsung menghantam tanpa persiapan.",
        "taboo": "Memaksa terus saat sudah ada nyeri. Cedera lamamu biasanya bukan karena bebannya berat, tapi karena tidak diberi waktu pulih.",
    },
    "xin": {
        "energy_type": "Energi Halus — presisi tinggi, ambang toleransi rendah",
        "exercise_advice": "Pilates, latihan postur, dan olahraga yang memperhatikan bentuk gerakan cocok. Mutu gerakan lebih berpengaruh buatmu daripada jumlahnya.",
        "taboo": "Mengabaikan gangguan kecil di pernapasan dan kulit karena dianggap sepele. Untuk chart ini, yang kecil biasanya sinyal awal.",
    },
    "ren": {
        "energy_type": "Energi Mengalir — stamina panjang, sulit berhenti",
        "exercise_advice": "Berenang, bersepeda jauh, dan olahraga ketahanan cocok. Tubuhmu senang bergerak lama asal pemandangannya berganti.",
        "taboo": "Pikiran yang tidak pernah dimatikan sampai larut. Istirahat buatmu bukan berbaring, tapi berhenti berpikir.",
    },
    "gui": {
        "energy_type": "Energi Menyerap — peka, cadangannya perlu dijaga",
        "exercise_advice": "Gerakan lembut yang teratur: berenang santai, jalan pagi, peregangan. Hindari menguras diri habis-habisan lalu memulihkannya dengan tidur seharian.",
        "taboo": "Mengurangi tidur dan minum saat sedang sibuk. Dari semua Day Master, chart-mu yang paling cepat terasa saat kekurangan keduanya.",
    },
}

DESTINY_HEALTH_ELEMENT = {
    "kayu": {
        "vulnerable_organ": "Hati dan kantung empedu",
        "symptoms": "Mudah pegal di sisi tubuh, mata cepat lelah, dan emosi yang naik tanpa sebab yang jelas.",
        "prevention": "Kurangi begadang dan alkohol, karena keduanya menekan organ ini paling duluan. Gerakan yang membuka dada dan pinggang membantu melancarkannya.",
    },
    "api": {
        "vulnerable_organ": "Jantung dan usus kecil",
        "symptoms": "Jantung berdebar saat cemas, tangan dan kaki dingin, serta tidur yang gampang terputus.",
        "prevention": "Jaga irama tidur dan kurangi kafein di atas jam tiga sore. Kardio ringan yang rutin lebih menolong daripada sesekali yang berat.",
    },
    "tanah": {
        "vulnerable_organ": "Limpa dan lambung",
        "symptoms": "Perut kembung, nafsu makan naik turun, dan badan terasa berat setelah makan.",
        "prevention": "Makan di jam yang tetap dan kurangi makanan dingin serta yang terlalu manis. Berjalan sebentar setelah makan menolong lebih banyak dari yang kelihatannya.",
    },
    "logam": {
        "vulnerable_organ": "Paru-paru dan usus besar",
        "symptoms": "Napas terasa pendek, kulit kering, dan gampang kena batuk pilek saat cuaca berubah.",
        "prevention": "Latihan pernapasan dalam dan udara yang bersih penting untuk chart ini. Jaga kelembapan ruangan tempatmu tidur.",
    },
    "air": {
        "vulnerable_organ": "Ginjal dan kandung kemih",
        "symptoms": "Pinggang pegal, cepat lelah menjelang sore, dan telinga berdenging saat kurang istirahat.",
        "prevention": "Cukupkan minum dan tidur sebelum tengah malam, karena organ ini paling dipengaruhi keduanya. Hangatkan area pinggang saat cuaca dingin.",
    },
}


SHEN_SHA_BANK = {
    "tian_yi": {
        "name_cn": "天乙貴人",
        "name_id": "Bintang Penolong Mulia",
        "icon": "⭐",
        "category": "auspicious",
        "description": "Bintang paling dihormati di seluruh 神煞. Menandakan ada orang yang datang membantu di saat paling genting, sering tanpa kamu minta dan tanpa sempat kamu balas setimpal.",
        "life_impact": "Masalah besarmu cenderung selesai lewat perantara, bukan lewat perjuangan sendirian. Rawat hubungan dengan orang yang lebih senior — di situ pintunya.",
    },
    "wen_chang": {
        "name_cn": "文昌星",
        "name_id": "Bintang Ilmu",
        "icon": "📚",
        "category": "auspicious",
        "description": "Bintang belajar dan tulisan. Menandakan kepala yang mudah menyerap dan tangan yang enak dipakai untuk merumuskan.",
        "life_impact": "Ujian, sertifikasi, dan pekerjaan yang menuntut menulis atau menjelaskan jadi jalur yang menguntungkanmu. Uang yang kamu taruh di pendidikan hampir selalu kembali.",
    },
    "tao_hua": {
        "name_cn": "桃花星",
        "name_id": "Bintang Pesona",
        "icon": "🌸",
        "category": "neutral",
        "description": "Bintang daya tarik. Orang mudah tertarik padamu, kadang lebih cepat dari yang kamu inginkan.",
        "life_impact": "Cocok untuk pekerjaan yang perlu disukai orang: penjualan, hiburan, layanan, panggung. Repotnya saat perhatian datang dari arah yang tidak kamu cari — batasnya kamu sendiri yang harus pasang.",
    },
    "yi_ma": {
        "name_cn": "驛馬星",
        "name_id": "Bintang Perjalanan",
        "icon": "🐎",
        "category": "neutral",
        "description": "Bintang gerak dan perpindahan. Hidupmu jarang berhenti lama di satu titik, entah tempat, pekerjaan, atau lingkaran pertemanan.",
        "life_impact": "Perpindahan lokasi sering jadi titik naikmu, bukan gangguan. Yang perlu dijaga: satu akar yang tetap, supaya gerak tidak berubah jadi kabur.",
    },
    "lu_shen": {
        "name_cn": "祿神",
        "name_id": "Bintang Rezeki Tetap",
        "icon": "💰",
        "category": "auspicious",
        "description": "Bintang penghidupan. Menandakan sumber pemasukan yang menempel pada dirimu sendiri, bukan pada keberuntungan.",
        "life_impact": "Kamu jarang benar-benar kehabisan karena keahlianmu selalu ada yang membutuhkan. Menambah kedalaman keahlian lebih menguntungkan daripada mengejar peluang baru.",
    },
    "yang_ren": {
        "name_cn": "羊刃",
        "name_id": "Bintang Mata Pedang",
        "icon": "⚔️",
        "category": "inauspicious",
        "description": "Bintang ketajaman yang berlebih. Tenaganya besar dan tidak sabar — bagus untuk menerjang, gampang melukai, termasuk melukai yang memegangnya.",
        "life_impact": "Kamu berani mengambil langkah yang orang lain hindari, dan sesekali membayarnya mahal. Salurkan ke pekerjaan yang memang menuntut ketegasan, jangan ke urusan pribadi.",
    },
    "hua_gai": {
        "name_cn": "華蓋星",
        "name_id": "Bintang Payung Langit",
        "icon": "🛡️",
        "category": "neutral",
        "description": "Bintang kesunyian dan kedalaman. Menandakan ketertarikan pada hal yang tidak ramai: seni, filsafat, spiritual, ilmu yang sepi peminat.",
        "life_impact": "Kamu berkembang paling jauh di bidang yang butuh perenungan, dan cenderung merasa sepi justru di keramaian. Itu bukan sesuatu yang perlu disembuhkan, cuma perlu diberi ruang.",
    },
    "tian_de": {
        "name_cn": "天德貴人",
        "name_id": "Bintang Kebajikan Langit",
        "icon": "🌟",
        "category": "auspicious",
        "description": "Bintang perlindungan. Menandakan ada yang meredam saat keadaan memburuk, sehingga akibatnya jarang sampai ke titik paling parah.",
        "life_impact": "Kamu sering lolos dari hal yang seharusnya jauh lebih berat. Perlindungan ini menguat saat kamu memang berbuat baik, bukan saat kamu mengandalkannya.",
    },
    "yue_de": {
        "name_cn": "月德貴人",
        "name_id": "Bintang Kebajikan Bulan",
        "icon": "🌙",
        "category": "auspicious",
        "description": "Sepasang dengan 天德 tapi bekerja dari dalam: menandakan watak yang cenderung tidak tega dan sulit berbuat curang.",
        "life_impact": "Orang mempercayaimu lebih cepat dari rata-rata, dan itu modal yang lebih mahal daripada uang. Waspadai orang yang justru memanfaatkan sifat ini.",
    },
    "jin_yu": {
        "name_cn": "金輿星",
        "name_id": "Bintang Kereta Emas",
        "icon": "🏆",
        "category": "auspicious",
        "description": "Bintang kenyamanan. Menandakan akses ke hidup yang layak — lewat keluarga, pasangan, atau posisi — tanpa harus berjuang sekeras orang lain.",
        "life_impact": "Kemudahan materi dan pasangan yang menopang lebih sering datang ke chart ini. Yang perlu dijaga: jangan sampai kenyamanan bikin kamu berhenti mengasah diri.",
    },
    "gu_chen": {
        "name_cn": "孤辰",
        "name_id": "Bintang Kesendirian",
        "icon": "🌑",
        "category": "inauspicious",
        "description": "Bintang jarak. Menandakan kecenderungan berdiri agak jauh dari keramaian, bahkan saat sedang berada di tengahnya.",
        "life_impact": "Kamu butuh waktu sendiri lebih banyak dari kebanyakan orang, dan hubungan yang menuntut kehadiran terus-menerus cepat menguras. Bukan berarti kamu ditakdirkan sendirian — kamu cuma perlu orang yang tidak takut pada ruang kosong.",
    },
    "gua_su": {
        "name_cn": "寡宿",
        "name_id": "Bintang Ruang Sunyi",
        "icon": "🥀",
        "category": "inauspicious",
        "description": "Di naskah lama namanya harfiah berarti kejandaan. Dalam pembacaan sekarang bintang ini dibaca sebagai kecenderungan energi menyendiri, bukan sebagai ramalan tentang nasib pasanganmu.",
        "life_impact": "Kamu bisa merasa sendirian bahkan di dekat orang yang menyayangimu, terutama saat sedang berat. Yang menolong bukan menambah keramaian, tapi satu hubungan yang cukup dalam untuk diajak diam bersama.",
    },
}


TIAN_YI_BY_STEM = [
    [1, 7], [0, 8], [11, 9], [11, 9], [1, 7],
    [0, 8], [1, 7], [6, 2], [3, 5], [3, 5],
]

WEN_CHANG_BY_STEM = [5, 6, 8, 9, 8, 9, 11, 0, 2, 3]

LU_SHEN_BY_STEM = [2, 3, 5, 6, 5, 6, 8, 9, 11, 0]

YANG_REN_BY_STEM = [3, 2, 6, 5, 6, 5, 9, 8, 0, 11]

JIN_YU_BY_STEM = [4, 5, 7, 8, 7, 8, 10, 11, 1, 2]

SAN_HE_GROUP = {
    8: "shen", 0: "shen", 4: "shen",
    2: "yin", 6: "yin", 10: "yin",
    5: "si", 9: "si", 1: "si",
    11: "hai", 3: "hai", 7: "hai",
}

TAO_HUA_BY_GROUP = {"shen": 9, "yin": 3, "si": 6, "hai": 0}

YI_MA_BY_GROUP = {"shen": 2, "yin": 8, "si": 11, "hai": 5}

HUA_GAI_BY_GROUP = {"shen": 4, "yin": 10, "si": 1, "hai": 7}

YUE_DE_BY_GROUP = {"yin": 2, "shen": 8, "hai": 0, "si": 6}

TIAN_DE_BY_MONTH = {
    2: ("stem", 3), 3: ("branch", 8), 4: ("stem", 8), 5: ("stem", 7),
    6: ("branch", 11), 7: ("stem", 0), 8: ("stem", 9), 9: ("branch", 2),
    10: ("stem", 2), 11: ("stem", 1), 0: ("branch", 5), 1: ("stem", 6),
}

GU_GUA_BY_YEAR = {
    11: (2, 10), 0: (2, 10), 1: (2, 10),
    2: (5, 1), 3: (5, 1), 4: (5, 1),
    5: (8, 4), 6: (8, 4), 7: (8, 4),
    8: (11, 7), 9: (11, 7), 10: (11, 7),
}


ELEMENT_REMEDY_BANK = {
    "kayu": {
        "colors": ["Hijau", "Hijau tua", "Cokelat muda"],
        "directions": ["Timur", "Tenggara"],
        "numbers": [3, 4],
        "crystals": ["Giok hijau", "Malachite", "Green aventurine"],
        "food_elements": ["Sayuran hijau", "Tunas dan kecambah", "Teh hijau", "Buah yang masam"],
        "ritual_advice": "Rawat satu tanaman hidup yang kamu urus sendiri, bukan yang diurus orang lain. Luangkan waktu di ruang terbuka berpohon minimal sekali seminggu, dan mulai harimu menghadap timur.",
    },
    "api": {
        "colors": ["Merah", "Oranye", "Ungu terang"],
        "directions": ["Selatan"],
        "numbers": [9],
        "crystals": ["Batu delima", "Carnelian", "Amethyst"],
        "food_elements": ["Masakan panggang", "Rempah yang menghangatkan", "Kopi secukupnya", "Sayuran berwarna merah"],
        "ritual_advice": "Pastikan kamu kena cahaya matahari pagi setiap hari, bukan sekadar lewat jendela. Nyalakan lampu hangat di ruang kerjamu, dan ambil kegiatan yang menempatkanmu di depan orang.",
    },
    "tanah": {
        "colors": ["Cokelat", "Kuning tanah", "Krem"],
        "directions": ["Barat daya", "Timur laut", "Tengah"],
        "numbers": [2, 5, 8],
        "crystals": ["Citrine", "Tiger eye", "Akik cokelat"],
        "food_elements": ["Umbi-umbian", "Biji-bijian utuh", "Makanan bertekstur padat", "Masakan yang dimasak lama"],
        "ritual_advice": "Tetapkan satu rutinitas harian yang tidak kamu geser apa pun keadaannya. Rapikan bagian tengah rumahmu dan isi dengan benda dari keramik atau batu.",
    },
    "logam": {
        "colors": ["Putih", "Perak", "Abu-abu"],
        "directions": ["Barat", "Barat laut"],
        "numbers": [6, 7],
        "crystals": ["Kuarsa bening", "Hematit", "Pirit"],
        "food_elements": ["Makanan berwarna putih", "Lobak dan bawang", "Makanan yang renyah", "Pedas yang ringan"],
        "ritual_advice": "Bereskan satu ruangan sampai benar-benar bersih dari barang yang tidak terpakai. Pakai benda logam di meja kerjamu, dan tutup hari dengan mencatat apa saja yang sudah selesai.",
    },
    "air": {
        "colors": ["Hitam", "Biru tua", "Biru laut"],
        "directions": ["Utara"],
        "numbers": [1],
        "crystals": ["Obsidian", "Batu bulan", "Lapis lazuli"],
        "food_elements": ["Makanan laut", "Kacang hitam", "Sup dan kaldu", "Asin yang wajar"],
        "ritual_advice": "Sediakan waktu hening tanpa layar sebelum tidur, sesingkat apa pun itu. Letakkan wadah berisi air di sisi utara ruanganmu, dan jaga jam tidurmu tetap sebelum tengah malam.",
    },
}


LIFE_PHASE_BANK = {
    "bi_jian": {
        "phase_name": "Fase Berdiri Sendiri",
        "description": "Sepuluh tahun yang mendorongmu mengurus sendiri apa yang selama ini dibantu orang. Teman sebaya dan saudara lebih sering muncul di ceritamu — kadang menolong, kadang menyaingi. Pengeluaran cenderung untuk hal yang kamu putuskan sendiri, tanpa banyak minta persetujuan.",
        "advice": "Pakai fase ini untuk membangun sesuatu yang benar-benar atas namamu. Jangan menunggu dukungan gratis, karena di periode ini ia memang jarang datang.",
    },
    "jie_cai": {
        "phase_name": "Fase Berbagi dan Berebut",
        "description": "Uang dan kesempatan lebih sering lewat tanganmu tapi lebih jarang mengendap. Orang di sekitarmu jadi faktor besar: ada yang membuka jalan, ada yang ikut menikmati tanpa ikut menanggung. Keputusan cepat lebih sering terjadi di fase ini dibanding biasanya.",
        "advice": "Perjelas hitam putih di setiap urusan uang bersama, sejak sebelum urusannya berjalan. Fase ini murah hati pada keberanianmu dan galak pada kelalaianmu.",
    },
    "shi_shen": {
        "phase_name": "Fase Berkarya dengan Tenang",
        "description": "Tekanan mengendur dan kamu punya ruang mengerjakan sesuatu yang kamu sukai sampai bentuknya bagus. Kesehatan dan suasana hati biasanya ikut membaik di periode ini. Hasil kerjamu mulai dikenali lewat mutunya, bukan lewat promosinya.",
        "advice": "Manfaatkan untuk menghasilkan sesuatu yang tetap ada setelah fase ini lewat. Kenikmatan periode ini gampang bikin lupa bahwa dia punya batas waktu.",
    },
    "shang_guan": {
        "phase_name": "Fase Melawan Arus",
        "description": "Kamu jadi lebih berani bersuara dan lebih sulit menelan hal yang dulu kamu diamkan. Bakat yang selama ini terpendam sering justru keluar di periode ini. Gesekan dengan atasan, aturan, atau institusi ikut naik.",
        "advice": "Salurkan ke karya, jangan ke perdebatan. Fase ini memberi panggung kalau kamu punya hasil, dan memberi masalah kalau kamu cuma punya pendapat.",
    },
    "pian_cai": {
        "phase_name": "Fase Peluang Berdatangan",
        "description": "Pintu terbuka dari arah yang tidak kamu rencanakan: kenalan baru, tawaran sampingan, kesempatan yang lewat tanpa diminta. Perputaran uang naik, begitu juga godaan mengambil semuanya sekaligus. Jaringanmu meluas lebih cepat dari biasanya.",
        "advice": "Pilih dua atau tiga yang benar-benar kamu kerjakan, tolak sisanya tanpa rasa bersalah. Yang bikin fase ini sia-sia bukan kurangnya peluang, tapi tidak ada yang selesai.",
    },
    "zheng_cai": {
        "phase_name": "Fase Mengendap dan Menumpuk",
        "description": "Pemasukan jadi lebih teratur dan banyak hal mulai punya bentuk tetap: pekerjaan, tempat tinggal, komitmen. Apa yang kamu bangun di fase ini cenderung bertahan lama. Kejutan berkurang, dan memang itu yang kamu butuhkan.",
        "advice": "Kunci apa yang sudah stabil jadi aset, jangan dibiarkan cuma jadi arus kas. Ini periode paling cocok untuk membeli sesuatu yang sanggup kamu tahan bertahun-tahun.",
    },
    "qi_sha": {
        "phase_name": "Fase Ditempa Tekanan",
        "description": "Beban datang lebih besar dari yang kamu siapkan — tanggung jawab baru, persaingan keras, atau keadaan yang memaksa berubah. Kamu tumbuh cepat di fase ini, tapi ongkosnya terasa di badan dan jam tidur. Orang melihatmu jadi jauh lebih tegas setelah periode ini lewat.",
        "advice": "Terima bebannya, tapi tentukan mana yang kamu pikul dan mana yang kamu serahkan. Rawat kesehatan seperti merawat alat kerja, karena di fase ini memang itu fungsinya.",
    },
    "zheng_guan": {
        "phase_name": "Fase Naik Jenjang",
        "description": "Posisi, tanggung jawab, dan pengakuan resmi lebih mudah datang di periode ini. Bersamaan dengan itu ruang gerakmu menyempit karena makin banyak yang memperhatikan. Reputasi berubah jadi mata uang utamamu.",
        "advice": "Ambil jenjang yang tersedia, tapi siapkan sesuatu yang tetap milikmu di luar jabatan. Fase ini memberi banyak selama namamu terjaga, dan menarik cepat begitu namamu tergores.",
    },
    "pian_yin": {
        "phase_name": "Fase Menyepi dan Mendalam",
        "description": "Minatmu bergeser ke hal yang lebih dalam dan lebih sepi — ilmu khusus, perenungan, bidang yang sedikit peminatnya. Kamu jadi lebih pemilih soal siapa yang boleh dekat. Dari luar terlihat melambat, padahal yang terjadi di dalam justru banyak.",
        "advice": "Pakai untuk menguasai sesuatu yang memang tidak bisa diburu-buru. Tetapkan satu hasil nyata yang harus keluar, supaya fase ini tidak habis jadi renungan saja.",
    },
    "zheng_yin": {
        "phase_name": "Fase Ditopang dan Menopang",
        "description": "Bantuan lebih mudah datang: guru, atasan, keluarga, atau kesempatan belajar yang tidak kamu cari. Kamu juga lebih sering jadi tempat orang lain belajar. Periode ini terasa aman, kadang terlalu aman.",
        "advice": "Ambil ilmunya sebanyak mungkin lalu segera dipakai. Kenyamanan di fase ini gampang berubah jadi alasan menunda hal yang seharusnya sudah kamu mulai.",
    },
}


PILLAR_POSITION_BANK = {
    "year": {
        "hanzi": "年柱",
        "label": "Pilar Tahun",
        "domain": "Leluhur, orang tua jauh, dan lingkungan tempat kamu dibesarkan.",
        "age_range": "0–16 tahun",
        "reading_note": "Dewa yang jatuh di sini menceritakan modal awal yang kamu bawa dari rumah, bukan hasil pilihanmu sendiri. Ini juga wajah yang orang lihat pertama kali sebelum benar-benar mengenalmu.",
    },
    "month": {
        "hanzi": "月柱",
        "label": "Pilar Bulan",
        "domain": "Orang tua, saudara, karir, dan gerbang rezeki.",
        "age_range": "16–30 tahun",
        "reading_note": "Pilar paling berpengaruh di seluruh chart karena dialah yang menentukan musim kelahiranmu. Dewa di sini biasanya jadi tema besar pekerjaanmu dan caramu berhadapan dengan otoritas.",
    },
    "day": {
        "hanzi": "日柱",
        "label": "Pilar Hari",
        "domain": "Diri sendiri di batangnya, pasangan di cabangnya.",
        "age_range": "30–45 tahun",
        "reading_note": "Batang hari adalah Day Master, titik acuan seluruh pembacaan. Cabangnya disebut 日支 dan dibaca sebagai ruang paling pribadimu: siapa yang kamu pilih dan bagaimana kamu saat sedang berdua.",
    },
    "hour": {
        "hanzi": "時柱",
        "label": "Pilar Jam",
        "domain": "Anak, murid, warisan, dan masa tua.",
        "age_range": "45 tahun ke atas",
        "reading_note": "Dewa di sini menunjukkan apa yang kamu tinggalkan dan bagaimana kerjamu berbuah di penghujung. Tanpa jam lahir, seluruh lapisan ini memang tidak bisa dibaca.",
    },
}


NO_BIRTH_TIME_BANK = {
    "notice": "Kamu tidak mengisi jam lahir, jadi bacaan ini disusun dari tiga pilar: tahun, bulan, dan hari. Tiga pilar tetap sah dibaca dan sudah dipakai berabad-abad saat jam lahir tidak tercatat. Yang hilang bukan ketepatannya, melainkan satu lapisan terakhirnya.",
    "still_valid": [
        "Day Master beserta seluruh watak dasarmu",
        "Kekuatan diri 身強/身弱 dan elemen yang menguntungkanmu",
        "Dewa dominan, jadi bacaan karir, rezeki, dan asmara tetap utuh",
        "Hubunganmu dengan latar keluarga lewat cabang tahun",
        "Sebagian besar bintang nasib yang dipicu batang hari dan cabang tahun",
    ],
    "not_available": [
        "Pilar jam beserta dewa yang ada di dalamnya",
        "Bacaan soal anak dan masa tua",
        "Bintang nasib yang kebetulan hanya menempel di cabang jam",
        "Usia mulai 大運 dengan ketepatan penuh",
    ],
    "invitation": "Kalau suatu saat kamu menemukan jam lahirmu di akta atau catatan keluarga, isi ulang — lapisan terakhirnya akan langsung terbuka.",
}


IDENTITY_BANK = {
    "tikus": {
        "icon": "🐀",
        "traits_positive": [
            "Cepat membaca situasi yang baru",
            "Hemat dan pandai menyimpan",
            "Banyak akal saat terdesak",
            "Ramah dan mudah diterima di lingkungan baru",
            "Rajin tanpa perlu disuruh",
            "Sigap mengambil kesempatan",
        ],
        "traits_negative": [
            "Gampang curiga pada niat orang",
            "Perhitungan sampai terlihat pelit",
            "Cemas berlebihan soal masa depan",
            "Suka menyimpan informasi untuk diri sendiri",
            "Sulit benar-benar santai",
        ],
        "personality_long": "Kamu tumbuh di lingkungan yang mengajarkan untuk sigap: menyiapkan sebelum dibutuhkan, menyimpan sebelum kekurangan. Orang mengenalmu sebagai yang paling cepat tanggap saat ada yang tidak beres, dan memang itu wajah yang kamu tunjukkan ke luar.\n\nDi mata orang kamu ramah dan gampang diajak bicara, tapi kedekatan yang sesungguhnya kamu berikan ke sedikit orang saja. Kebiasaan menyiapkan rencana cadangan besar kemungkinan kamu pelajari dari rumah, bukan dari pengalamanmu sendiri.",
        "green_flags": [
            "Ingat detail kecil yang kamu sebut cuma sekali",
            "Siap sedia justru saat keadaan genting",
            "Realistis soal uang dan rencana bersama",
            "Langsung mencarikan jalan keluar, bukan cuma bersimpati",
            "Tidak gampang membocorkan apa pun yang kamu titipkan",
        ],
        "red_flags": [
            "Mengecek diam-diam sebelum bertanya langsung",
            "Menghitung pengeluaran berdua terlalu detail",
            "Menyimpan kekhawatiran sampai keluar sekaligus",
            "Sulit percaya penuh meski sudah lama bersama",
            "Menyiapkan jalan keluar bahkan saat hubungan sedang baik",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Tikus Kayu — Perencana Ekspansi",
                "description": "Naluri menyimpanmu bertemu dorongan tumbuh, jadi kamu menabung untuk dipakai, bukan untuk didiamkan. Kamu paling hidup saat sedang merintis sesuatu dari nol.",
            },
            "api": {
                "title": "Tikus Api — Penjaga yang Berani",
                "description": "Kehati-hatianmu berpadu dengan keberanian bersuara, jadi kamu bukan tipe yang menunggu di belakang. Sekali yakin, kamu bergerak lebih cepat dari Tikus mana pun.",
            },
            "tanah": {
                "title": "Tikus Tanah — Pengelola Stabil",
                "description": "Kamu menabung dan menahan sekaligus, sehingga apa pun yang terkumpul jarang berkurang. Perubahan mendadak paling tidak nyaman buat versi ini.",
            },
            "logam": {
                "title": "Tikus Logam — Penghitung Tegas",
                "description": "Perhitunganmu jadi lebih dingin dan batasmu jauh lebih jelas. Kamu tidak sungkan menolak, dan itu menyelamatkanmu dari banyak kerugian.",
            },
            "air": {
                "title": "Tikus Air — Pembaca Arah Angin",
                "description": "Kepekaanmu berlipat: kamu tahu duluan ke mana sesuatu akan bergerak. Sisi sulitnya, kamu juga yang paling gampang cemas di antara semua Tikus.",
            },
        },
        "famous_people": [
            "Diego Maradona (1960)",
            "Dwayne Johnson (1972)",
            "Mark Zuckerberg (1984)",
            "Scarlett Johansson (1984)",
        ],
        "lucky_flowers": ["Lily", "Anggrek bulan"],
        "unlucky_colors": ["Kuning tanah", "Cokelat"],
        "unlucky_numbers": [2, 5, 8],
        "best_months": [3, 7, 12],
        "worst_months": [5, 6],
        "relation_to_day_master": {
            "sheng": "Latar keluargamu mengalir searah dengan tujuanmu — kehati-hatian yang kamu pelajari di rumah jadi modal, bukan beban.",
            "ke": "Kewaspadaan yang diwariskan lingkunganmu berubah jadi tekanan: kamu sulit melangkah tanpa lebih dulu memikirkan kemungkinan terburuk.",
            "sama": "Cara rumahmu membaca dunia dan caramu sendiri nyaris sama, jadi kamu jarang merasa harus menjelaskan diri di sana.",
            "diserap": "Kamu jadi orang yang menyiapkan segalanya untuk keluarga, sering sebelum ada yang meminta.",
            "dikuasai": "Kamu mengambil jarak dari cara rumahmu mengatur segala sesuatu dan menyusun sistemmu sendiri, meski sempat dianggap membangkang.",
        },
        "spirit_advice": "Naluri menyimpanmu itu berkah, tapi hidup tidak bisa terus-menerus dijalani sebagai persiapan. Sesekali pakailah apa yang sudah kamu kumpulkan, dan izinkan satu orang tahu isi kekhawatiranmu tanpa kamu saring dulu.",
    },
    "kerbau": {
        "icon": "🐂",
        "traits_positive": [
            "Tekun sampai pekerjaan benar-benar selesai",
            "Bisa dipegang omongannya",
            "Tahan pada kerja berat yang berulang",
            "Tenang saat orang lain kebingungan",
            "Tidak silau pada jalan pintas",
            "Bertanggung jawab tanpa perlu diawasi",
        ],
        "traits_negative": [
            "Keras kepala sampai sulit diajak berganti cara",
            "Lambat menerima hal baru",
            "Menyimpan kesal tanpa pernah dibicarakan",
            "Terlalu serius sampai jarang bersenang-senang",
            "Menganggap remeh perasaan yang tidak terlihat",
        ],
        "personality_long": "Kamu berasal dari lingkungan yang menilai orang dari apa yang dikerjakan, bukan dari apa yang dikatakan. Sejak kecil kamu terbiasa menyelesaikan bagianmu tanpa banyak menuntut, dan itu yang sampai sekarang orang lihat pertama kali darimu.\n\nDi luar kamu terlihat tenang dan sulit digoyahkan, dan sebagian besar memang benar. Yang tidak terlihat adalah berapa banyak hal yang kamu tahan sendiri karena menganggap mengeluh itu tidak ada gunanya.",
        "green_flags": [
            "Menepati apa yang dijanjikan tanpa perlu diingatkan",
            "Tidak berubah sikap saat keadaan memburuk",
            "Membereskan hal berat tanpa mengungkitnya lagi",
            "Jelas soal niat jangka panjang",
            "Aman diajak membangun sesuatu bersama",
        ],
        "red_flags": [
            "Menolak berubah meski caranya sudah jelas tidak jalan",
            "Diam berhari-hari daripada membahas masalah",
            "Menganggap kerja keras sudah cukup mewakili perasaan",
            "Sulit meminta maaf lebih dulu",
            "Menyimpan catatan kesalahan lama tanpa bilang",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Kerbau Kayu — Pembangun Bertahap",
                "description": "Ketekunanmu bertemu dorongan tumbuh, jadi kamu membangun sesuatu yang makin besar tiap tahun. Kamu lebih terbuka pada cara baru dibanding Kerbau lain.",
            },
            "api": {
                "title": "Kerbau Api — Penggerak Keras Kepala",
                "description": "Ada bara di balik ketenanganmu; sekali kamu yakin, tidak ada yang bisa menghentikan. Versi ini paling gampang bersitegang dengan orang yang menghalangi.",
            },
            "tanah": {
                "title": "Kerbau Tanah — Fondasi yang Tak Bergerak",
                "description": "Dari semua Kerbau, kamu yang paling sulit digeser. Yang kamu pegang bertahan puluhan tahun, termasuk kebiasaan yang sebenarnya perlu diganti.",
            },
            "logam": {
                "title": "Kerbau Logam — Penegak Standar",
                "description": "Ketekunanmu berpadu dengan ketegasan, jadi kamu menuntut mutu pada diri sendiri maupun orang lain. Mudah dihormati, tidak selalu mudah didekati.",
            },
            "air": {
                "title": "Kerbau Air — Pekerja yang Peka",
                "description": "Kamu tetap tekun tapi jauh lebih bisa membaca suasana. Versi ini paling lentur dan paling sering jadi tempat orang bercerita.",
            },
        },
        "famous_people": [
            "Barack Obama (1961)",
            "Diana Spencer (1961)",
            "George Clooney (1961)",
            "Keira Knightley (1985)",
        ],
        "lucky_flowers": ["Tulip", "Bunga sepatu"],
        "unlucky_colors": ["Hijau", "Hijau tua"],
        "unlucky_numbers": [3, 4],
        "best_months": [4, 8, 11],
        "worst_months": [5, 6],
        "relation_to_day_master": {
            "sheng": "Keluargamu memberi pijakan yang nyata — tanah, nama, atau kebiasaan kerja — dan itu betul-betul terpakai dalam hidupmu.",
            "ke": "Tuntutan dari rumah datang dalam bentuk pekerjaan dan kewajiban, dan kamu memikulnya jauh sebelum usiamu siap.",
            "sama": "Etos kerja rumahmu sudah jadi etos kerjamu sendiri; kalian tidak perlu saling menjelaskan soal itu.",
            "diserap": "Kamu jadi tulang punggung keluarga lebih awal dari seharusnya, dan sebagian besar orang menganggapnya wajar.",
            "dikuasai": "Kamu memilih jalan yang berbeda dari yang disiapkan untukmu, dan butuh waktu lama sampai pilihan itu diterima.",
        },
        "spirit_advice": "Kesanggupanmu memikul bukan alasan untuk selalu memikul sendirian. Latih menyampaikan keberatan saat masih kecil, sebelum berubah jadi diam yang berhari-hari.",
    },
    "macan": {
        "icon": "🐅",
        "traits_positive": [
            "Berani mengambil langkah pertama",
            "Punya wibawa yang tidak perlu diusahakan",
            "Membela orang yang diperlakukan tidak adil",
            "Cepat mengambil keputusan di saat genting",
            "Jujur soal apa yang dia mau",
            "Menular semangatnya ke orang sekitar",
        ],
        "traits_negative": [
            "Gampang panas dan menyesal setelahnya",
            "Sulit menerima diperintah",
            "Bosan pada hal yang sudah berjalan rapi",
            "Mengambil risiko tanpa menghitung ulang",
            "Sulit meminta bantuan karena gengsi",
        ],
        "personality_long": "Kamu besar di lingkungan yang membuatmu terbiasa berdiri di depan, entah karena memang didorong atau karena tidak ada yang lain yang mau. Orang membaca kehadiranmu lebih dulu daripada ucapanmu, dan itu berlaku bahkan saat kamu diam.\n\nDari luar kamu terlihat berani dan tidak takut apa-apa. Yang jarang terbaca adalah bahwa keberanian itu sering kamu pakai untuk menutupi keraguan yang tidak ingin kamu tunjukkan ke siapa pun.",
        "green_flags": [
            "Berdiri di depan saat kamu diperlakukan tidak adil",
            "Jujur soal perasaannya sejak awal",
            "Tidak takut memulai hal besar bersamamu",
            "Cepat bertindak saat kamu butuh bantuan",
            "Tidak menyimpan dendam setelah selesai bertengkar",
        ],
        "red_flags": [
            "Mengambil keputusan besar tanpa mengajak bicara",
            "Naik suara duluan sebelum tahu masalahnya",
            "Bosan begitu hubungan mulai terasa tenang",
            "Sulit mengakui salah di depan orang lain",
            "Menganggap kompromi sebagai bentuk kalah",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Macan Kayu — Pemimpin yang Merangkul",
                "description": "Keberanianmu berpadu dengan kemauan bekerja sama, jadi kamu memimpin dengan mengajak, bukan menyuruh. Versi Macan yang paling banyak pengikutnya.",
            },
            "api": {
                "title": "Macan Api — Bara yang Menyambar",
                "description": "Keberanian dan ketidaksabaran ada di puncaknya. Kamu memulai banyak hal besar, dan hanya sebagian yang sempat kamu tuntaskan.",
            },
            "tanah": {
                "title": "Macan Tanah — Penjaga Wilayah",
                "description": "Keberanianmu punya rem. Kamu bergerak setelah yakin, dan apa yang sudah kamu ambil kamu pertahankan sampai lama.",
            },
            "logam": {
                "title": "Macan Logam — Penegak yang Keras",
                "description": "Ketegasanmu berlipat sampai orang segan mendekat. Kamu tidak kenal abu-abu, dan itu jadi kekuatan sekaligus jarak.",
            },
            "air": {
                "title": "Macan Air — Pemimpin yang Membaca Orang",
                "description": "Keberanianmu dilengkapi kepekaan, jadi kamu tahu kapan menekan dan kapan mengalah. Versi Macan yang paling lentur dalam bernegosiasi.",
            },
        },
        "famous_people": [
            "Tom Cruise (1962)",
            "Leonardo DiCaprio (1974)",
            "Lady Gaga (1986)",
            "Agnez Mo (1986)",
        ],
        "lucky_flowers": ["Bunga matahari", "Kembang sepatu merah"],
        "unlucky_colors": ["Putih", "Perak"],
        "unlucky_numbers": [6, 7],
        "best_months": [5, 9, 10],
        "worst_months": [4, 7],
        "relation_to_day_master": {
            "sheng": "Keberanian yang kamu punya sebagian besar dipinjamkan oleh rumahmu — ada yang menyokong sejak kamu mulai berani.",
            "ke": "Otoritas di rumahmu menekan lebih keras daripada yang kamu tunjukkan, dan sebagian sikap melawanmu lahir dari situ.",
            "sama": "Kamu dan keluargamu sama-sama keras kepala, sehingga saling mengerti sekaligus sering berbenturan.",
            "diserap": "Kamu memakai keberanianmu untuk melindungi keluarga, sering dengan mengorbankan kesempatanmu sendiri.",
            "dikuasai": "Kamu keluar dari bayang-bayang rumahmu lebih awal dan membangun namamu sendiri dari nol.",
        },
        "spirit_advice": "Keberanian tanpa jeda cuma jadi kelelahan yang bergema. Sebelum menyambar, beri dirimu satu tarikan napas — hampir semua penyesalanmu lahir di detik yang tidak sempat kamu ambil itu.",
    },
    "kelinci": {
        "icon": "🐇",
        "traits_positive": [
            "Halus dalam bersikap dan berbicara",
            "Pandai meredakan ketegangan",
            "Punya selera yang bagus dan rapi",
            "Peka pada kenyamanan orang lain",
            "Sabar menghadapi orang yang sulit",
            "Mudah disukai di lingkungan baru",
        ],
        "traits_negative": [
            "Menghindar dari masalah alih-alih menghadapinya",
            "Sulit berkata tidak secara langsung",
            "Terlalu memikirkan penilaian orang",
            "Ragu-ragu pada keputusan besar",
            "Menarik diri diam-diam saat kecewa",
        ],
        "personality_long": "Kamu dibesarkan di lingkungan yang menjaga keharmonisan, kadang lebih menjaga suasana daripada menyelesaikan soalnya. Kamu belajar membaca ruangan sejak kecil, dan itu jadi kemampuan yang orang rasakan langsung saat berada di dekatmu.\n\nOrang menganggapmu menyenangkan dan tidak merepotkan. Yang tidak terlihat adalah berapa banyak keinginanmu sendiri yang kamu geser demi menjaga agar tidak ada yang tersinggung.",
        "green_flags": [
            "Membuat orang nyaman tanpa harus berusaha",
            "Memperhatikan hal kecil yang kamu sukai",
            "Menyelesaikan pertengkaran tanpa menambah luka",
            "Menjaga rumah dan suasana tetap enak",
            "Sabar pada versi terburukmu",
        ],
        "red_flags": [
            "Bilang iya padahal keberatan",
            "Menghilang sebentar saat ada masalah",
            "Menyimpan kecewa sampai tiba-tiba jauh",
            "Terlalu peduli pada bagaimana kalian terlihat",
            "Menunda keputusan penting berulang kali",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Kelinci Kayu — Penumbuh yang Lembut",
                "description": "Kehalusanmu berpadu dengan dorongan tumbuh, jadi kamu pelan-pelan membangun sesuatu yang membesar tanpa ribut. Kamu juga paling ramah pada ide orang lain.",
            },
            "api": {
                "title": "Kelinci Api — Pesona yang Menyala",
                "description": "Ada kehangatan yang bikin orang berkumpul di dekatmu. Versi ini paling berani tampil dan paling gampang tersinggung.",
            },
            "tanah": {
                "title": "Kelinci Tanah — Penenang yang Kokoh",
                "description": "Kelembutanmu punya pijakan, jadi kamu menenangkan tanpa ikut hanyut. Perubahan mendadak yang paling menguras versi ini.",
            },
            "logam": {
                "title": "Kelinci Logam — Anggun yang Berprinsip",
                "description": "Di balik sikap halusmu ada garis batas yang jelas. Kamu jarang menaikkan suara, tapi juga jarang bisa dibujuk.",
            },
            "air": {
                "title": "Kelinci Air — Peredam yang Peka",
                "description": "Kepekaanmu berlipat sampai kamu sering menyerap perasaan orang lain tanpa sadar. Versi Kelinci yang paling butuh waktu sendiri.",
            },
        },
        "famous_people": [
            "Michael Jordan (1963)",
            "David Beckham (1975)",
            "Angelina Jolie (1975)",
            "Lionel Messi (1987)",
        ],
        "lucky_flowers": ["Melati", "Snapdragon"],
        "unlucky_colors": ["Putih", "Perak"],
        "unlucky_numbers": [6, 7],
        "best_months": [6, 9, 10],
        "worst_months": [3, 8],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi rasa aman yang cukup, sehingga kelembutanmu tumbuh sebagai pilihan, bukan sebagai pertahanan.",
            "ke": "Ada suara keras di latar belakangmu yang bikin kamu belajar mengalah lebih cepat dari yang seharusnya.",
            "sama": "Keluargamu sama-sama menjaga keharmonisan, jadi kalian nyaman sekaligus sama-sama menunda pembicaraan yang sulit.",
            "diserap": "Kamu jadi peredam di keluargamu, orang yang menenangkan semua orang dan jarang ditenangkan.",
            "dikuasai": "Kamu melepaskan pola menjaga suasana yang diajarkan di rumah dan belajar menyatakan mau sendiri.",
        },
        "spirit_advice": "Menjaga suasana itu keahlian, bukan kewajiban seumur hidup. Sekali waktu katakan keberatanmu di saat kejadian, bukan setelah berminggu-minggu kamu simpan sendiri.",
    },
    "naga": {
        "icon": "🐉",
        "traits_positive": [
            "Punya cita-cita yang berani",
            "Membuat orang percaya pada rencananya",
            "Tidak mudah menyerah pada penolakan",
            "Murah hati saat sedang di atas",
            "Cepat pulih setelah kegagalan besar",
            "Menarik perhatian tanpa harus mencari",
        ],
        "traits_negative": [
            "Sulit menerima kritik yang terasa merendahkan",
            "Menuntut standar yang tidak realistis",
            "Meremehkan detail pelaksanaan",
            "Sulit mengakui butuh bantuan",
            "Cepat kehilangan minat pada hal yang biasa saja",
        ],
        "personality_long": "Kamu tumbuh dengan harapan yang menempel — dari keluarga, dari lingkungan, atau dari dirimu sendiri yang menyerapnya sejak kecil. Orang cenderung menaruh perhatian lebih padamu, dan kamu terbiasa dengan itu sampai terasa biasa.\n\nDari luar kamu terlihat percaya diri dan tidak butuh persetujuan siapa-siapa. Yang jarang terlihat adalah bahwa kamu menilai dirimu jauh lebih keras daripada siapa pun yang pernah menilaimu.",
        "green_flags": [
            "Mendorongmu bermimpi lebih besar dari yang kamu berani",
            "Bangga menunjukkan kamu ke orang lain",
            "Tidak ragu mengeluarkan banyak untuk orang yang disayangi",
            "Berdiri tegak saat keadaan memburuk",
            "Tidak menahan potensimu demi kenyamanannya",
        ],
        "red_flags": [
            "Menganggap pendapatnya otomatis lebih benar",
            "Kecewa berat kalau kamu tidak sehebat harapannya",
            "Sulit meminta maaf tanpa syarat",
            "Mengatur arah hidup kalian sepihak",
            "Menghilang saat sedang merasa gagal",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Naga Kayu — Visioner yang Membangun",
                "description": "Cita-cita besarmu disertai kesabaran menumbuhkan. Versi ini paling sering benar-benar menyelesaikan apa yang dijanjikan.",
            },
            "api": {
                "title": "Naga Api — Ambisi Tanpa Rem",
                "description": "Kharisma dan ambisimu di puncak, begitu juga risikonya. Kamu bisa naik sangat tinggi dan jatuh sama cepatnya.",
            },
            "tanah": {
                "title": "Naga Tanah — Pemimpin yang Membumi",
                "description": "Mimpimu besar tapi langkahnya terukur. Versi Naga yang paling dipercaya memegang sesuatu dalam jangka panjang.",
            },
            "logam": {
                "title": "Naga Logam — Penakluk yang Tegas",
                "description": "Ketegasan dan ambisi bertemu, jadi kamu memangkas siapa pun yang memperlambat. Kuat di hasil, mahal di hubungan.",
            },
            "air": {
                "title": "Naga Air — Pemimpin yang Mendengar",
                "description": "Ambisimu dilengkapi kesabaran membaca orang. Versi ini paling sanggup menyesuaikan rencana tanpa merasa kalah.",
            },
        },
        "famous_people": [
            "Keanu Reeves (1964)",
            "Sandra Bullock (1964)",
            "Rihanna (1988)",
            "Adele (1988)",
        ],
        "lucky_flowers": ["Hyacinth", "Bambu hoki"],
        "unlucky_colors": ["Hijau", "Hijau tua"],
        "unlucky_numbers": [3, 4],
        "best_months": [7, 8, 11],
        "worst_months": [2, 9],
        "relation_to_day_master": {
            "sheng": "Keluargamu menaruh harapan sekaligus menyediakan jalannya, jadi ambisimu punya bahan bakar sejak awal.",
            "ke": "Harapan dari rumah datang tanpa dukungan yang sepadan, dan kamu memikulnya sebagai beban, bukan sebagai bekal.",
            "sama": "Keluargamu juga besar kepala dengan cara yang baik; kalian saling memahami ambisi masing-masing tanpa perlu dijelaskan.",
            "diserap": "Kamu memakai seluruh kemampuanmu untuk mengangkat nama keluarga, kadang lebih dulu daripada namamu sendiri.",
            "dikuasai": "Kamu menolak cetakan yang disiapkan keluarga dan membuktikan diri lewat jalan yang mereka tidak mengerti.",
        },
        "spirit_advice": "Yang paling sering kamu perlukan bukan mimpi yang lebih besar, tapi izin untuk tidak selalu hebat. Ukur dirimu dari apa yang sudah kamu selesaikan, bukan dari jarak ke gambaran di kepalamu.",
    },
    "ular": {
        "icon": "🐍",
        "traits_positive": [
            "Tenang menghadapi situasi yang rumit",
            "Berpikir jauh sebelum bergerak",
            "Pandai menyimpan hal yang tidak perlu diketahui orang",
            "Punya daya tarik yang tidak berisik",
            "Tajam menilai karakter orang",
            "Tahan menunggu lama tanpa terlihat gelisah",
        ],
        "traits_negative": [
            "Tertutup sampai orang sulit mendekat",
            "Menyimpan curiga tanpa memverifikasi",
            "Sulit memaafkan pengkhianatan sekecil apa pun",
            "Menghitung terlalu lama sampai kesempatan lewat",
            "Menjaga jarak bahkan dari orang terdekat",
        ],
        "personality_long": "Kamu berasal dari lingkungan yang mengajarkan bahwa tidak semua hal perlu diceritakan. Kamu belajar mengamati lebih dulu dan menilai belakangan, dan sampai sekarang itu yang orang rasakan sebagai ketenanganmu.\n\nOrang menganggapmu misterius dan sulit ditebak, sebagian karena kamu memang tidak merasa perlu menjelaskan diri. Yang tidak mereka tahu, kamu sudah menyelesaikan seluruh perdebatan itu di dalam kepalamu jauh sebelum mereka bertanya.",
        "green_flags": [
            "Tidak panik saat keadaan berantakan",
            "Menjaga rahasia yang kamu titipkan",
            "Menilai orang dengan tajam dan biasanya benar",
            "Setia dalam diam tanpa perlu dibuktikan tiap hari",
            "Memberi nasihat yang sudah dipikirkan matang",
        ],
        "red_flags": [
            "Menyimpan kecurigaan tanpa pernah menanyakannya",
            "Menutup diri total saat sedang terluka",
            "Mengingat kesalahan kecil bertahun-tahun",
            "Menguji kesetiaanmu diam-diam",
            "Membalas dengan cara yang tidak kelihatan",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Ular Kayu — Penimbang yang Tumbuh",
                "description": "Ketenanganmu berpadu dengan keinginan berkembang, jadi kamu lebih terbuka pada orang baru. Versi Ular yang paling mudah diajak bekerja sama.",
            },
            "api": {
                "title": "Ular Api — Pesona yang Dingin di Luar",
                "description": "Ada api di balik ketenanganmu; kamu berani tampil dan mengambil panggung. Versi ini paling intens dalam menyukai maupun membenci.",
            },
            "tanah": {
                "title": "Ular Tanah — Penyimpan yang Sabar",
                "description": "Kesabaranmu berlipat dan kamu sanggup menunggu bertahun-tahun untuk satu hal. Sulit digeser, sulit juga diburu-buru.",
            },
            "logam": {
                "title": "Ular Logam — Penilai yang Tajam",
                "description": "Penilaianmu jadi sangat tegas dan batasmu keras. Kamu jarang memberi kesempatan kedua pada orang yang sudah mengecewakan.",
            },
            "air": {
                "title": "Ular Air — Pembaca yang Dalam",
                "description": "Kepekaanmu di puncak: kamu sering tahu sesuatu tanpa bisa menjelaskan dari mana. Versi Ular yang paling banyak memendam.",
            },
        },
        "famous_people": [
            "J.K. Rowling (1965)",
            "Shah Rukh Khan (1965)",
            "Daniel Radcliffe (1989)",
            "Taylor Swift (1989)",
        ],
        "lucky_flowers": ["Kaktus berbunga", "Anggrek"],
        "unlucky_colors": ["Hitam", "Biru tua"],
        "unlucky_numbers": [1],
        "best_months": [7, 8, 12],
        "worst_months": [1, 10],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi ruang untuk berpikir sendiri, dan dari situ ketenanganmu tumbuh jadi kekuatan.",
            "ke": "Ada yang membuatmu belajar tidak mempercayai orang sejak dini, dan kewaspadaan itu masih terbawa sampai sekarang.",
            "sama": "Keluargamu juga bukan tipe yang banyak bicara; kalian akrab lewat hal yang tidak perlu diucapkan.",
            "diserap": "Kamu memikul rahasia dan beban keluarga sendirian, dan hampir tidak ada yang tahu itu ada padamu.",
            "dikuasai": "Kamu memutus pola diam yang diwariskan rumahmu dan memilih mengurus hidupmu dengan caramu sendiri.",
        },
        "spirit_advice": "Menyimpan itu keahlianmu, tapi tidak semua yang kamu simpan pantas kamu tanggung sendirian. Pilih satu orang, lalu ceritakan satu hal yang belum pernah kamu ceritakan ke siapa pun.",
    },
    "kuda": {
        "icon": "🐎",
        "traits_positive": [
            "Bersemangat dan menular energinya",
            "Cepat akrab dengan siapa saja",
            "Berani mencoba hal yang belum pernah",
            "Jujur dan tidak berbelit",
            "Cepat bangkit setelah kecewa",
            "Tidak betah melihat orang murung",
        ],
        "traits_negative": [
            "Gampang bosan sebelum sesuatu selesai",
            "Bicara duluan lalu menyesal",
            "Sulit diam di satu tempat terlalu lama",
            "Menghindari pembicaraan yang berat",
            "Janji lebih banyak dari yang sempat ditepati",
        ],
        "personality_long": "Kamu tumbuh di lingkungan yang membuatmu terbiasa bergerak dan tidak betah menunggu. Orang mengenalmu sebagai yang paling cepat mencairkan suasana, dan itu memang bagian dirimu yang paling dulu terlihat.\n\nDari luar kamu terlihat selalu baik-baik saja dan gampang senang. Yang tidak terlihat adalah bahwa bergerak terus adalah caramu menghindari duduk terlalu lama dengan hal yang berat.",
        "green_flags": [
            "Membuat hari biasa jadi menyenangkan",
            "Jujur soal apa yang dia rasakan hari itu",
            "Selalu siap kalau kamu mengajak pergi",
            "Tidak memelihara pertengkaran sampai besok",
            "Menyemangati tanpa perlu diminta",
        ],
        "red_flags": [
            "Berpindah minat sebelum yang lama selesai",
            "Menghindari pembicaraan yang serius",
            "Melempar janji tanpa mengukur waktunya",
            "Merasa terkurung saat hubungan mulai menetap",
            "Bicara tanpa saring lalu minta maaf belakangan",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Kuda Kayu — Penjelajah yang Tumbuh",
                "description": "Semangatmu punya arah, jadi gerakanmu benar-benar membawa ke suatu tempat. Versi Kuda yang paling konsisten.",
            },
            "api": {
                "title": "Kuda Api — Lari Tanpa Menoleh",
                "description": "Energimu di puncak dan remnya paling tipis. Kamu bisa menempuh jarak paling jauh, sekaligus paling sering melewatkan yang di belakang.",
            },
            "tanah": {
                "title": "Kuda Tanah — Pelari yang Punya Rumah",
                "description": "Kamu tetap suka bergerak, tapi selalu tahu ke mana harus pulang. Versi ini paling bisa dipegang janjinya.",
            },
            "logam": {
                "title": "Kuda Logam — Penggerak yang Tegas",
                "description": "Semangatmu berpadu dengan ketegasan, jadi kamu bergerak cepat dan berani memutuskan. Sulit dihentikan saat sudah berangkat.",
            },
            "air": {
                "title": "Kuda Air — Pengembara yang Membaca Arah",
                "description": "Kamu bergerak mengikuti keadaan, bukan melawannya. Versi Kuda yang paling luwes dan paling gampang berubah rencana.",
            },
        },
        "famous_people": [
            "Jackie Chan (1954)",
            "Mike Tyson (1966)",
            "Kobe Bryant (1978)",
            "Emma Watson (1990)",
        ],
        "lucky_flowers": ["Marigold", "Calla lily"],
        "unlucky_colors": ["Hitam", "Biru tua"],
        "unlucky_numbers": [1],
        "best_months": [1, 6, 9],
        "worst_months": [11, 12],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi bekal untuk berangkat, jadi kebebasanmu bukan hasil melarikan diri melainkan hasil didukung.",
            "ke": "Ada yang menahan gerakmu sejak kecil, dan sebagian dorongan pergimu lahir dari keinginan lepas dari situ.",
            "sama": "Keluargamu juga tidak betah diam; kalian sama-sama gelisah dan sama-sama memahaminya.",
            "diserap": "Kamu habis banyak tenaga mengurusi keluarga, sampai rencanamu sendiri terus tertunda.",
            "dikuasai": "Kamu pergi lebih jauh dari yang keluargamu bayangkan, dan membuat jalanmu sendiri di tempat yang asing bagi mereka.",
        },
        "spirit_advice": "Bergerak terus bukan berarti sedang menuju ke suatu tempat. Sekali-sekali berhentilah cukup lama untuk mengetahui apa sebenarnya yang sedang kamu hindari.",
    },
    "kambing": {
        "icon": "🐐",
        "traits_positive": [
            "Lembut dan tidak tega melihat orang kesulitan",
            "Punya rasa seni yang kuat",
            "Sabar mendengarkan tanpa menghakimi",
            "Pandai membuat tempat jadi nyaman",
            "Setia pada orang yang sudah dekat",
            "Tidak haus menonjolkan diri",
        ],
        "traits_negative": [
            "Terlalu memikirkan pendapat orang",
            "Gampang sedih dan lama pulihnya",
            "Menunda keputusan sampai dipilihkan orang",
            "Sulit menolak permintaan",
            "Mengeluh di dalam tanpa menyampaikan ke luar",
        ],
        "personality_long": "Kamu berasal dari lingkungan yang menghargai perasaan dan kenyamanan, mungkin lebih dari yang menghargai ketegasan. Kamu belajar menempatkan diri supaya tidak merepotkan, dan orang merasakannya sebagai kehangatan yang tidak menuntut.\n\nDi luar kamu terlihat mudah menerima dan jarang keberatan. Yang jarang terbaca adalah seberapa detail kamu memperhatikan, dan seberapa lama kamu menyimpan hal-hal kecil yang menyakitkan.",
        "green_flags": [
            "Memperhatikan perasaanmu sebelum kamu menyebutkannya",
            "Membuat rumah terasa hangat tanpa banyak biaya",
            "Sabar pada hari-hari terburukmu",
            "Tidak pernah membesar-besarkan kesalahanmu",
            "Setia bertahun-tahun tanpa perlu diperiksa",
        ],
        "red_flags": [
            "Memendam kecewa sampai terasa dari jauh",
            "Menunggu ditebak daripada menyampaikan",
            "Bergantung berlebihan saat sedang rapuh",
            "Menghindari keputusan yang harus dia ambil",
            "Membandingkan diri dengan orang lain diam-diam",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Kambing Kayu — Perawat yang Menumbuhkan",
                "description": "Kelembutanmu berpadu dengan dorongan tumbuh, jadi kamu merawat orang sampai mereka jadi lebih besar. Versi paling sabar dari semua Kambing.",
            },
            "api": {
                "title": "Kambing Api — Hati yang Berani Bersuara",
                "description": "Ada keberanian di balik kelembutanmu, jadi kamu tidak selalu mengalah. Versi ini paling ekspresif dan paling gampang tersinggung.",
            },
            "tanah": {
                "title": "Kambing Tanah — Penjaga Rumah",
                "description": "Kelembutanmu punya pijakan; kamu merawat sekaligus mengelola. Versi Kambing yang paling bisa diandalkan soal urusan nyata.",
            },
            "logam": {
                "title": "Kambing Logam — Lembut dengan Garis Tegas",
                "description": "Kamu tetap halus tapi punya batas yang tidak bisa ditawar. Sulit dibujuk sekali kamu memutuskan.",
            },
            "air": {
                "title": "Kambing Air — Peka yang Menyerap",
                "description": "Kepekaanmu di puncak dan kamu sering menanggung perasaan orang lain. Versi Kambing yang paling butuh dijaga.",
            },
        },
        "famous_people": [
            "Bill Gates (1955)",
            "Steve Jobs (1955)",
            "Julia Roberts (1967)",
            "Nicole Kidman (1967)",
        ],
        "lucky_flowers": ["Anyelir", "Primrose"],
        "unlucky_colors": ["Hijau", "Hijau tua"],
        "unlucky_numbers": [3, 4],
        "best_months": [2, 5, 10],
        "worst_months": [11, 12],
        "relation_to_day_master": {
            "sheng": "Kehangatan rumahmu betul-betul mengisi, dan kelembutanmu tumbuh karena memang dirawat, bukan karena terpaksa.",
            "ke": "Ada tuntutan keras di rumahmu yang membuatmu belajar mengecilkan diri supaya aman.",
            "sama": "Keluargamu sama-sama lembut dan sama-sama menghindari konflik; nyaman, tapi banyak hal jadi tidak pernah dibahas.",
            "diserap": "Kamu menjadi tempat seluruh keluarga menumpahkan perasaan, dan hampir tidak pernah sebaliknya.",
            "dikuasai": "Kamu melepaskan peran yang dititipkan padamu di rumah dan belajar mengurus perasaanmu sendiri lebih dulu.",
        },
        "spirit_advice": "Kebaikanmu tidak jadi lebih bernilai kalau kamu menghabiskannya sampai kosong. Mulai dari satu penolakan kecil minggu ini, dan perhatikan bahwa dunia tetap baik-baik saja.",
    },
    "monyet": {
        "icon": "🐒",
        "traits_positive": [
            "Cepat belajar hal baru",
            "Punya banyak cara menyelesaikan satu masalah",
            "Menghidupkan suasana di mana pun berada",
            "Luwes menghadapi orang yang berbeda-beda",
            "Tidak gampang menyerah pada soal yang rumit",
            "Cepat melihat celah yang orang lain lewatkan",
        ],
        "traits_negative": [
            "Gampang bosan dan pindah minat",
            "Memakai kecerdikan untuk menghindar",
            "Sulit dianggap serius karena terlalu santai",
            "Terlalu percaya bisa mengakali keadaan",
            "Menutupi kesulitan dengan bercanda",
        ],
        "personality_long": "Kamu tumbuh di lingkungan yang menghargai orang yang bisa mencari jalan, bukan yang menunggu diberi tahu. Kamu terbiasa memutar cara sampai ada yang berhasil, dan itu yang paling cepat orang kenali darimu.\n\nOrang melihatmu sebagai yang paling gampang diajak dan paling cepat nyambung. Yang jarang mereka sadari, kamu memakai keramahan itu juga untuk menjaga jarak dari hal yang tidak ingin kamu bahas.",
        "green_flags": [
            "Selalu punya ide saat semuanya buntu",
            "Membuat masalah terasa lebih ringan",
            "Cepat menyesuaikan diri dengan keluargamu",
            "Tidak kaku soal rencana yang berubah",
            "Mau belajar hal baru demi kalian berdua",
        ],
        "red_flags": [
            "Mengalihkan pembicaraan serius dengan candaan",
            "Berjanji cepat lalu mencari alasan",
            "Bosan pada rutinitas hubungan yang sudah jalan",
            "Menutupi masalah dengan solusi cepat",
            "Sulit ditebak mana yang sungguhan dan mana yang bercanda",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Monyet Kayu — Pemikir yang Membangun",
                "description": "Kecerdikanmu punya arah jangka panjang, jadi idemu benar-benar jadi sesuatu. Versi Monyet yang paling tekun.",
            },
            "api": {
                "title": "Monyet Api — Otak yang Menyala",
                "description": "Cepat, berani, dan tidak sabar. Kamu memulai banyak hal brilian dan meninggalkan sebagiannya di tengah jalan.",
            },
            "tanah": {
                "title": "Monyet Tanah — Ahli Siasat yang Membumi",
                "description": "Kecerdikanmu dipakai untuk membereskan hal nyata. Versi ini paling bisa dipercaya memegang pekerjaan penting.",
            },
            "logam": {
                "title": "Monyet Logam — Penyiasat yang Tajam",
                "description": "Kamu menghitung untung rugi dengan dingin dan tidak sungkan memutuskan. Sangat efektif, kadang terasa terlalu dingin.",
            },
            "air": {
                "title": "Monyet Air — Pembaca Situasi",
                "description": "Kecerdikanmu dilengkapi kepekaan, jadi kamu tahu apa yang orang butuhkan sebelum mereka bilang. Paling luwes bernegosiasi.",
            },
        },
        "famous_people": [
            "Tom Hanks (1956)",
            "Will Smith (1968)",
            "Celine Dion (1968)",
            "Kim Kardashian (1980)",
        ],
        "lucky_flowers": ["Krisan", "Alamanda"],
        "unlucky_colors": ["Merah", "Oranye"],
        "unlucky_numbers": [9],
        "best_months": [3, 4, 11],
        "worst_months": [1, 10],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi ruang bereksperimen, jadi kecerdikanmu tumbuh sebagai keahlian, bukan sebagai siasat bertahan.",
            "ke": "Kamu belajar memutar akal karena keadaan di rumah menuntutnya, bukan karena kamu ingin.",
            "sama": "Keluargamu juga penuh akal dan cepat menyesuaikan; kalian saling mengerti tanpa perlu banyak penjelasan.",
            "diserap": "Kamu jadi orang yang dipanggil setiap ada masalah di keluarga, dan itu menyita jauh lebih banyak dari yang terlihat.",
            "dikuasai": "Kamu menolak cara keluargamu menyelesaikan masalah dan membangun cara berpikirmu sendiri.",
        },
        "spirit_advice": "Tidak semua hal perlu diakali; sebagian cuma perlu dijalani sampai selesai. Coba satu perkara yang kamu selesaikan dengan cara paling lurus, tanpa jalan pintas apa pun.",
    },
    "ayam": {
        "icon": "🐓",
        "traits_positive": [
            "Teliti sampai ke detail terkecil",
            "Terus terang dan tidak berbasa-basi",
            "Rapi dan terorganisir",
            "Berani menyuarakan yang orang lain diamkan",
            "Bekerja keras tanpa banyak mengeluh",
            "Tepat waktu dan menepati jadwal",
        ],
        "traits_negative": [
            "Terlalu blak-blakan sampai menyakiti",
            "Kritis pada hal yang sebenarnya sepele",
            "Sulit menerima cara kerja yang berantakan",
            "Mudah cemas kalau ada yang tidak sesuai rencana",
            "Suka mengulang keluhan yang sama",
        ],
        "personality_long": "Kamu berasal dari lingkungan yang menuntut rapi, tepat, dan bisa dipertanggungjawabkan. Kamu belajar memperhatikan detail sebelum belajar bersantai, dan sampai sekarang itu yang orang rasakan sebagai ketelitianmu.\n\nOrang melihatmu sebagai yang paling siap dan paling terorganisir di ruangan. Yang tidak mereka lihat adalah berapa banyak tenaga yang habis untuk memastikan semuanya sesuai dengan yang kamu bayangkan.",
        "green_flags": [
            "Mengurus hal-hal yang kamu lupakan",
            "Jujur bahkan saat jawabannya tidak enak",
            "Merencanakan sampai ke detail terkecil",
            "Tidak pernah terlambat pada hal yang kamu tunggu",
            "Membereskan kekacauan tanpa mengeluh",
        ],
        "red_flags": [
            "Mengoreksi hal kecil tanpa henti",
            "Menyampaikan kritik tanpa memikirkan waktunya",
            "Menuntut rapi pada hal yang tidak penting",
            "Cemas berlebihan kalau rencana berubah",
            "Mengungkit kesalahan lama sebagai contoh",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Ayam Kayu — Perapi yang Berkembang",
                "description": "Ketelitianmu dipakai untuk membangun, bukan cuma untuk mengoreksi. Versi Ayam yang paling terbuka pada masukan.",
            },
            "api": {
                "title": "Ayam Api — Suara yang Lantang",
                "description": "Kamu berani bicara di depan dan tidak takut menyinggung. Versi paling menonjol sekaligus paling sering bergesekan.",
            },
            "tanah": {
                "title": "Ayam Tanah — Perapi yang Sabar",
                "description": "Ketelitianmu bertemu kesabaran, jadi kamu sanggup mengurus hal rumit bertahun-tahun. Paling tahan pada pekerjaan berulang.",
            },
            "logam": {
                "title": "Ayam Logam — Standar yang Tidak Ditawar",
                "description": "Ketelitian dan ketegasan bertemu di puncak. Mutu kerjamu sangat tinggi, toleransimu sangat rendah.",
            },
            "air": {
                "title": "Ayam Air — Kritikus yang Halus",
                "description": "Kamu tetap teliti tapi jauh lebih pandai memilih kata. Versi Ayam yang paling enak diajak bekerja sama.",
            },
        },
        "famous_people": [
            "Matthew McConaughey (1969)",
            "Beyoncé (1981)",
            "Serena Williams (1981)",
            "Britney Spears (1981)",
        ],
        "lucky_flowers": ["Gladiol", "Balsam"],
        "unlucky_colors": ["Merah", "Oranye"],
        "unlucky_numbers": [9],
        "best_months": [3, 4, 12],
        "worst_months": [2, 9],
        "relation_to_day_master": {
            "sheng": "Ketertiban yang diajarkan di rumahmu benar-benar berguna, dan kamu memakainya tanpa perlu melawannya.",
            "ke": "Standar di rumahmu dipasang terlalu tinggi, dan suara yang mengoreksi itu masih terdengar di kepalamu sampai sekarang.",
            "sama": "Keluargamu sama-sama detail dan sama-sama terus terang; kalian bisa bertengkar tanpa menyimpan dendam.",
            "diserap": "Kamu jadi orang yang merapikan urusan semua orang di keluarga, dan itu dianggap sudah semestinya.",
            "dikuasai": "Kamu melepaskan standar yang dipasangkan padamu dan menetapkan takaran cukupmu sendiri.",
        },
        "spirit_advice": "Ketelitianmu menyelamatkan banyak hal, tapi tidak semua yang tidak rapi itu salah. Biarkan satu hal berjalan tidak sempurna minggu ini, dan lihat bahwa dunia tetap berputar.",
    },
    "anjing": {
        "icon": "🐕",
        "traits_positive": [
            "Setia pada orang dan prinsip",
            "Berani membela yang benar",
            "Bisa dipercaya memegang hal penting",
            "Jujur bahkan saat merugikan diri sendiri",
            "Peduli pada keadilan di sekitarnya",
            "Hadir saat orang lain menghilang",
        ],
        "traits_negative": [
            "Gampang cemas dan berpikir yang buruk duluan",
            "Sulit percaya pada orang baru",
            "Terlalu keras menilai yang dianggap tidak adil",
            "Menyimpan kekhawatiran sendirian",
            "Sulit melepaskan orang yang sudah mengecewakan",
        ],
        "personality_long": "Kamu tumbuh di lingkungan yang menanamkan bahwa setia dan benar itu lebih penting dari untung. Kamu terbiasa memilih pihak dan bertahan di situ, dan orang merasakannya sebagai keandalan yang jarang ditemukan.\n\nDari luar kamu terlihat tegas dan punya pendirian. Yang tidak terlihat adalah berapa sering kamu mengulang kekhawatiran di kepalamu, terutama soal orang-orang yang kamu sayangi.",
        "green_flags": [
            "Tidak pernah pergi saat keadaan sulit",
            "Membela kamu bahkan saat tidak ada yang lain",
            "Jujur meski jawabannya merugikan dirinya",
            "Konsisten bertahun-tahun tanpa berubah",
            "Menjaga janji seperti menjaga nama",
        ],
        "red_flags": [
            "Curiga berlebihan tanpa bukti",
            "Memikirkan hal buruk sampai mengganggu tidur",
            "Menghakimi orang terlalu cepat soal salah-benar",
            "Menyimpan kekhawatiran lalu menyalahkan diri",
            "Sulit memaafkan meski sudah memilih bertahan",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Anjing Kayu — Penjaga yang Tumbuh",
                "description": "Kesetiaanmu disertai keterbukaan pada hal baru. Versi Anjing yang paling gampang berteman dan paling jarang curiga.",
            },
            "api": {
                "title": "Anjing Api — Pembela yang Berapi",
                "description": "Kamu berani berdiri paling depan saat ada ketidakadilan. Versi ini paling mudah tersulut dan paling sulit didinginkan.",
            },
            "tanah": {
                "title": "Anjing Tanah — Penjaga yang Kokoh",
                "description": "Kesetiaanmu berpijak kuat dan hampir tidak bisa digoyahkan. Yang kamu jaga, kamu jaga sampai habis.",
            },
            "logam": {
                "title": "Anjing Logam — Penegak Prinsip",
                "description": "Rasa adilmu berubah jadi aturan yang keras. Sangat bisa dipercaya, sangat sulit diajak berkompromi.",
            },
            "air": {
                "title": "Anjing Air — Penjaga yang Peka",
                "description": "Kesetiaanmu dilengkapi kepekaan membaca orang. Versi Anjing yang paling banyak memikirkan dan paling banyak mencemaskan.",
            },
        },
        "famous_people": [
            "Michael Jackson (1958)",
            "Madonna (1958)",
            "Pangeran William (1982)",
            "Justin Bieber (1994)",
        ],
        "lucky_flowers": ["Mawar", "Sedap malam"],
        "unlucky_colors": ["Hijau", "Hijau tua"],
        "unlucky_numbers": [3, 4],
        "best_months": [1, 2, 5],
        "worst_months": [3, 8],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi rasa aman yang nyata, dan kesetiaanmu tumbuh karena memang pernah kamu terima lebih dulu.",
            "ke": "Kamu belajar waspada karena pernah ada yang mengecewakan di lingkaran terdekat, dan itu belum sepenuhnya lepas.",
            "sama": "Keluargamu memegang prinsip yang sama denganmu; kalian bisa berbeda pendapat tanpa kehilangan kepercayaan.",
            "diserap": "Kamu menjaga semua orang di keluarga sampai lupa siapa yang menjagamu.",
            "dikuasai": "Kamu berhenti membela hal yang diwariskan rumahmu dan menetapkan sendiri mana yang layak kamu bela.",
        },
        "spirit_advice": "Kesetiaanmu berharga, dan justru karena itu jangan diberikan tanpa syarat ke siapa pun yang meminta. Simpan sebagian tenaga kekhawatiranmu untuk merawat dirimu sendiri.",
    },
    "babi": {
        "icon": "🐖",
        "traits_positive": [
            "Tulus dan tidak banyak berhitung",
            "Murah hati pada orang yang membutuhkan",
            "Menerima orang apa adanya",
            "Tidak menyimpan dendam lama",
            "Menikmati hidup tanpa harus mewah",
            "Gampang dipercaya karena tidak pandai berpura-pura",
        ],
        "traits_negative": [
            "Terlalu gampang percaya pada orang",
            "Sulit menolak sampai dimanfaatkan",
            "Menunda hal yang tidak menyenangkan",
            "Boros saat sedang senang",
            "Menghindari konflik sampai merugikan diri",
        ],
        "personality_long": "Kamu besar di lingkungan yang mengajarkan berbagi lebih dulu dan berhitung belakangan. Kamu terbiasa memberi tanpa memikirkan balasan, dan orang merasakan ketulusan itu hampir sejak pertemuan pertama.\n\nDari luar kamu terlihat santai dan gampang diajak apa saja. Yang tidak terlihat adalah bahwa kamu sering tahu sedang dimanfaatkan, dan tetap memilih membiarkannya demi tidak merusak suasana.",
        "green_flags": [
            "Memberi tanpa menghitung balasannya",
            "Tidak mengungkit kesalahan yang sudah dimaafkan",
            "Menerima keluargamu apa adanya",
            "Membuat suasana jadi ringan tanpa dibuat-buat",
            "Jujur karena memang tidak pandai berpura-pura",
        ],
        "red_flags": [
            "Terlalu percaya pada orang yang belum terbukti",
            "Menunda pembicaraan yang tidak enak",
            "Membiarkan dirinya dimanfaatkan demi damai",
            "Boros saat suasana hatinya sedang bagus",
            "Menghindari tanggung jawab yang terasa berat",
        ],
        "alter_ego": {
            "kayu": {
                "title": "Babi Kayu — Pemberi yang Tumbuh",
                "description": "Ketulusanmu disertai dorongan berkembang, jadi kamu memberi sambil membangun. Versi Babi yang paling produktif.",
            },
            "api": {
                "title": "Babi Api — Hati Hangat yang Berani",
                "description": "Kamu murah hati sekaligus berani mengambil risiko. Versi ini paling ramai dan paling cepat menghabiskan.",
            },
            "tanah": {
                "title": "Babi Tanah — Penikmat yang Mengumpulkan",
                "description": "Ketulusanmu berpadu dengan kemampuan menyimpan. Versi Babi yang paling aman keuangannya.",
            },
            "logam": {
                "title": "Babi Logam — Murah Hati yang Punya Batas",
                "description": "Kamu tetap tulus tapi tahu kapan harus berhenti memberi. Versi Babi yang paling sulit dimanfaatkan.",
            },
            "air": {
                "title": "Babi Air — Peka dan Mudah Terbawa",
                "description": "Kepekaanmu membuatmu cepat iba dan cepat tersentuh. Versi Babi yang paling butuh belajar menolak.",
            },
        },
        "famous_people": [
            "Hillary Clinton (1947)",
            "Elon Musk (1971)",
            "Ewan McGregor (1971)",
            "Chelsea Islan (1995)",
        ],
        "lucky_flowers": ["Hortensia", "Krisan kuning"],
        "unlucky_colors": ["Kuning tanah", "Cokelat"],
        "unlucky_numbers": [2, 5, 8],
        "best_months": [1, 2, 6],
        "worst_months": [4, 7],
        "relation_to_day_master": {
            "sheng": "Rumahmu memberi lebih banyak daripada yang diminta, dan ketulusanmu tumbuh karena kamu memang pernah merasakannya.",
            "ke": "Kebaikanmu pernah dipakai orang di lingkaran terdekat, dan pelajaran itu datang dengan harga yang tidak murah.",
            "sama": "Keluargamu sama-sama tidak pandai berhitung soal memberi; kalian hangat sekaligus sama-sama mudah kehabisan.",
            "diserap": "Kamu terus menyubsidi keluarga dengan uang, waktu, atau tenaga, dan hampir tidak pernah menagihnya kembali.",
            "dikuasai": "Kamu berhenti jadi penyangga yang selalu tersedia dan mulai menetapkan batas yang sempat bikin canggung.",
        },
        "spirit_advice": "Ketulusan tanpa batas bukan kebaikan yang lebih besar, cuma kebaikan yang lebih cepat habis. Belajar menolak bukan mengkhianati wataknya, tapi menjaga agar wataknya bisa bertahan lama.",
    },
}
