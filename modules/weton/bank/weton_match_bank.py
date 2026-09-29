WETON_LENS = {
    "asmara": {
        "label": "Asmara",
        "icon": "fa-heart",
        "romantic": True,
        "origin_note": "",
    },
    "pertemanan": {
        "label": "Pertemanan",
        "icon": "fa-user-group",
        "romantic": False,
        "origin_note": "Petung ini aslinya dipakai untuk menimbang calon pasangan. Di lensa pertemanan, tafsirnya diterjemahkan ke dinamika pertemanan.",
    },
    "kerja": {
        "label": "Rekan Kerja",
        "icon": "fa-briefcase",
        "romantic": False,
        "origin_note": "Petung ini aslinya dipakai untuk menimbang calon pasangan. Di lensa rekan kerja, tafsirnya diterjemahkan ke cara kalian bekerja bareng.",
    },
}

DEFAULT_LENS = "asmara"

PETUNG = {
    "sisa8": {
        "name": "Petung sisa bagi 8",
        "divisor": 8,
        "results": ["pesthi", "pegat", "ratu", "jodoh", "topo", "tinari", "padu", "sujanan"],
        "source": "Mutiara di Balik Tata Cara Pengantin Jawa (Pusat Bahasa, 2002)",
    },
    "sisa5": {
        "name": "Petung sisa bagi 5",
        "divisor": 5,
        "results": ["lungguh", "sri", "dana", "lara", "pati"],
        "source": "Mutiara di Balik Tata Cara Pengantin Jawa (Pusat Bahasa, 2002) dan Primbon Betaljemur Adammakna",
    },
    "sisa4": {
        "name": "Petung sisa bagi 4",
        "divisor": 4,
        "results": ["punggel", "gentho", "gembili", "sri"],
        "source": "Hitungan jodoh sisa bagi 4: Gentho, Gembili, Sri, Punggel (detikJateng, narasumber filolog Museum Radya Pustaka Solo)",
    },
    "sisa7": {
        "name": "Petung sisa bagi 7",
        "divisor": 7,
        "results": [
            "lebu_katiup_angin",
            "wasesa_segara",
            "tunggak_semi",
            "satriya_wibawa",
            "sumur_sinaba",
            "satriya_wirang",
            "bumi_kapetak",
        ],
        "source": "Mutiara di Balik Tata Cara Pengantin Jawa (Pusat Bahasa, 2002)",
    },
}

TONE_LABELS = {
    "baik": "Dibaca baik",
    "campur": "Ada tantangan",
    "berat": "Perlu usaha ekstra",
}

MATCH_DISCLAIMER = (
    "Petung adalah tradisi membaca kecenderungan, bukan vonis. Hasil akhirnya tetap ditentukan "
    "cara kalian saling memperlakukan."
)

PETUNG_RESULTS = {
    "pegat": {
        "name": "Pegat",
        "tone": "berat",
        "meaning": "Rawan renggang karena urusan ekonomi atau komunikasi.",
        "lens": {
            "asmara": {
                "inti": "Pegat dibaca sebagai hubungan yang rawan renggang, biasanya dipicu urusan uang atau komunikasi yang macet.",
                "saran": [
                    "Bikin kebiasaan ngobrol soal uang tiap bulan, bukan cuma saat ada masalah. Transparan sejak awal bikin kalian lebih kuat.",
                    "Kalau ada yang mengganjal, bahas di hari yang sama. Masalah kecil yang ditunda paling sering bikin jarak makin lebar.",
                ],
            },
            "pertemanan": {
                "inti": "Pegat dibaca sebagai pertemanan yang gampang merenggang kalau komunikasi jarang dan urusan uang tidak jelas.",
                "saran": [
                    "Hindari utang-piutang yang nggak tercatat. Pertemanan paling awet kalau urusan uang selalu terang.",
                    "Jadwalkan ketemu atau ngobrol rutin, walau singkat. Jarak kecil yang dibiarkan lama bisa jadi putus kontak.",
                ],
            },
            "kerja": {
                "inti": "Pegat dibaca sebagai kerja sama yang rawan bubar di tengah jalan karena pembagian hasil atau komunikasi yang kurang jelas.",
                "saran": [
                    "Tulis pembagian tugas dan hasil sejak awal. Kesepakatan tertulis mencegah salah paham saat proyek mulai padat.",
                    "Pasang jadwal update singkat tiap minggu supaya tidak ada yang merasa ditinggal atau kerja sendirian.",
                ],
            },
        },
    },
    "ratu": {
        "name": "Ratu",
        "tone": "baik",
        "meaning": "Dihormati dan disegani lingkungan, hubungannya rukun.",
        "lens": {
            "asmara": {
                "inti": "Ratu dibaca sebagai pasangan yang rukun dan disegani lingkungan. Orang di sekitar kalian cenderung respek.",
                "saran": [
                    "Nama baik kalian aset berharga. Jaga dengan tetap rendah hati dan nggak pamer di depan orang lain.",
                    "Karena sering jadi contoh, jangan lupa ruang pribadi berdua. Hubungan yang sehat bukan cuma soal citra.",
                ],
            },
            "pertemanan": {
                "inti": "Ratu dibaca sebagai duo yang disegani di tongkrongan. Kalian kompak dan sering jadi rujukan teman lain.",
                "saran": [
                    "Pakai pengaruh kalian buat bikin lingkaran pertemanan yang lebih inklusif, bukan eksklusif.",
                    "Tetap sisakan waktu ngobrol berdua. Kekompakan yang kelihatan dari luar perlu dirawat dari dalam.",
                ],
            },
            "kerja": {
                "inti": "Ratu dibaca sebagai tim yang dihormati. Kalian kelihatan kompak dan gampang dipercaya orang lain.",
                "saran": [
                    "Reputasi bagus bikin kalian sering diberi tanggung jawab lebih. Pastikan beban kerjanya tetap realistis.",
                    "Dokumentasikan cara kerja kalian supaya tim lain bisa belajar dan kalian nggak jadi satu-satunya andalan.",
                ],
            },
        },
    },
    "jodoh": {
        "name": "Jodoh",
        "tone": "baik",
        "meaning": "Cocok, saling menerima, dan awet.",
        "lens": {
            "asmara": {
                "inti": "Jodoh dibaca sebagai pasangan yang cocok dan saling menerima kekurangan. Hubungannya cenderung awet.",
                "saran": [
                    "Rasa cocok bisa bikin lengah. Tetap ucapkan terima kasih untuk hal kecil supaya kalian nggak saling take for granted.",
                    "Terus bikin pengalaman baru bareng. Rasa nyaman paling awet kalau tetap ada hal yang ditunggu berdua.",
                ],
            },
            "pertemanan": {
                "inti": "Petung ini dibaca sebagai pertemanan yang klop dan saling menerima. Kalian nyaman jadi diri sendiri satu sama lain.",
                "saran": [
                    "Pertemanan seawet ini layak dirayakan. Ingat momen penting temanmu dan hadir saat dia butuh.",
                    "Karena sudah nyaman, jangan ragu jujur saat ada yang kurang pas. Teman dekat justru paling bisa menerima.",
                ],
            },
            "kerja": {
                "inti": "Petung ini dibaca sebagai rekan kerja yang klop dan saling melengkapi. Kalian gampang sepakat soal cara kerja.",
                "saran": [
                    "Kalian nyaman bekerja bareng, jadi coba tantang diri dengan proyek yang lebih besar.",
                    "Jangan sampai terlalu sepakat sampai lupa mengecek ulang. Minta orang ketiga meninjau keputusan penting.",
                ],
            },
        },
    },
    "topo": {
        "name": "Topo",
        "tone": "campur",
        "meaning": "Awalnya berat, terutama soal ekonomi, lalu membaik seiring waktu.",
        "lens": {
            "asmara": {
                "inti": "Topo dibaca sebagai hubungan yang awalnya berat, terutama soal ekonomi, tapi membaik seiring waktu.",
                "saran": [
                    "Susun rencana keuangan bersama sejak awal. Masa sulit terasa lebih ringan kalau kalian tahu arahnya.",
                    "Rayakan kemajuan kecil. Topo mengajarkan sabar, dan kesabaran kalian sekarang jadi modal nanti.",
                ],
            },
            "pertemanan": {
                "inti": "Topo dibaca sebagai pertemanan yang butuh waktu untuk klik. Awalnya canggung, lama-lama justru solid.",
                "saran": [
                    "Jangan buru-buru menilai. Kasih kesempatan beberapa kali ngobrol sebelum menyimpulkan kalian nggak cocok.",
                    "Cari satu kegiatan yang sama-sama kalian suka. Kesamaan kecil sering jadi pintu pertemanan yang lebih dalam.",
                ],
            },
            "kerja": {
                "inti": "Topo dibaca sebagai kerja sama yang awalnya penuh penyesuaian, lalu makin lancar setelah ritmenya ketemu.",
                "saran": [
                    "Sepakati cara kerja di minggu pertama: jam respons, alat, dan format laporan. Awal yang rapi mempercepat klik.",
                    "Evaluasi bareng setelah proyek pertama. Hal yang dibahas terbuka jadi pelajaran, bukan ganjalan.",
                ],
            },
        },
    },
    "tinari": {
        "name": "Tinari",
        "tone": "baik",
        "meaning": "Bahagia, sering beruntung, dan rezeki lapang.",
        "lens": {
            "asmara": {
                "inti": "Tinari dibaca sebagai hubungan yang bahagia, sering beruntung, dan rezekinya terasa lapang.",
                "saran": [
                    "Keberuntungan paling awet kalau dikelola. Sisihkan sebagian rezeki untuk tabungan bersama.",
                    "Bagikan kebahagiaan kalian ke orang sekitar. Hubungan yang murah hati biasanya makin dimudahkan.",
                ],
            },
            "pertemanan": {
                "inti": "Tinari dibaca sebagai pertemanan yang seru dan bawa hoki. Rencana bareng kalian sering berjalan mulus.",
                "saran": [
                    "Manfaatkan energi positif ini untuk proyek bareng, misalnya usaha kecil atau kegiatan sosial.",
                    "Tetap jadi tempat pulang saat salah satu sedang apes. Pertemanan yang bahagia diuji saat keadaan sedang kurang baik.",
                ],
            },
            "kerja": {
                "inti": "Tinari dibaca sebagai kerja sama yang lancar dan sering bertemu peluang bagus.",
                "saran": [
                    "Peluang yang sering datang perlu disaring. Pilih yang paling sejalan dengan tujuan tim.",
                    "Catat apa yang bikin proyek kalian berhasil supaya keberhasilannya bisa diulang, bukan cuma kebetulan.",
                ],
            },
        },
    },
    "padu": {
        "name": "Padu",
        "tone": "campur",
        "meaning": "Sering berselisih, tapi tidak sampai berpisah.",
        "lens": {
            "asmara": {
                "inti": "Padu dibaca sebagai hubungan yang sering berselisih, tapi tidak sampai berpisah. Kalian sama-sama punya pendirian.",
                "saran": [
                    "Sepakati aturan bertengkar: tanpa membentak dan tanpa mengungkit masa lalu. Beda pendapat jadi lebih sehat.",
                    "Setelah berselisih, luangkan waktu untuk berbaikan dengan jelas. Jangan biarkan masalah menggantung.",
                ],
            },
            "pertemanan": {
                "inti": "Padu dibaca sebagai pertemanan yang sering debat, tapi tetap langgeng. Kalian nyaman beda pendapat.",
                "saran": [
                    "Debat itu seru asal tidak personal. Serang idenya, bukan orangnya.",
                    "Tahu kapan berhenti. Kadang setuju untuk tidak setuju lebih sehat daripada memaksa menang.",
                ],
            },
            "kerja": {
                "inti": "Padu dibaca sebagai rekan kerja yang sering beda pendapat, tapi tetap bisa menyelesaikan pekerjaan.",
                "saran": [
                    "Pakai data sebagai penengah. Keputusan yang berbasis bukti lebih cepat disepakati.",
                    "Tentukan siapa pemegang keputusan akhir untuk tiap bagian supaya debat tidak berlarut.",
                ],
            },
        },
    },
    "sujanan": {
        "name": "Sujanan",
        "tone": "berat",
        "meaning": "Rawan cekcok, kurang harmonis, dan rawan ada pihak ketiga.",
        "lens": {
            "asmara": {
                "inti": "Sujanan dibaca sebagai hubungan yang rawan cekcok dan rawan godaan pihak ketiga kalau kepercayaan tidak dijaga.",
                "saran": [
                    "Bangun kepercayaan lewat keterbukaan kecil, misalnya jujur soal rencana dan teman-teman baru.",
                    "Kalau cemburu muncul, bicarakan dengan tenang tanpa menuduh. Rasa aman tumbuh dari percakapan, bukan pengawasan.",
                ],
            },
            "pertemanan": {
                "inti": "Sujanan dibaca sebagai pertemanan yang rawan salah paham, apalagi kalau ada gosip dari orang lain.",
                "saran": [
                    "Konfirmasi langsung sebelum percaya omongan orang. Satu pesan klarifikasi bisa menyelamatkan pertemanan.",
                    "Jaga rahasia teman. Kepercayaan yang sekali bocor paling susah dipulihkan.",
                ],
            },
            "kerja": {
                "inti": "Sujanan dibaca sebagai kerja sama yang rawan gesekan dan kurang selaras, terutama kalau ada pihak lain ikut campur.",
                "saran": [
                    "Selesaikan masalah langsung berdua sebelum dibawa ke forum yang lebih besar.",
                    "Pastikan semua kesepakatan tercatat di satu tempat supaya tidak ada versi cerita yang berbeda-beda.",
                ],
            },
        },
    },
    "pesthi": {
        "name": "Pesthi",
        "tone": "baik",
        "meaning": "Tenteram, rukun, dan jarang ada konflik.",
        "lens": {
            "asmara": {
                "inti": "Pesthi dibaca sebagai hubungan yang tenteram dan rukun, jarang diwarnai konflik besar.",
                "saran": [
                    "Suasana adem itu berharga. Tetap bicarakan hal yang kurang pas supaya tenang bukan berarti memendam.",
                    "Bikin tradisi kecil berdua, misalnya jalan sore tiap pekan. Hubungan yang tenang tetap butuh kejutan.",
                ],
            },
            "pertemanan": {
                "inti": "Pesthi dibaca sebagai pertemanan yang adem dan jarang ribut. Kalian bikin satu sama lain merasa tenang.",
                "saran": [
                    "Pertemanan setenang ini cocok jadi tempat cerita. Jadilah pendengar yang baik saat temanmu butuh.",
                    "Sesekali ajak keluar dari zona nyaman bareng supaya pertemanan kalian tetap berkembang.",
                ],
            },
            "kerja": {
                "inti": "Pesthi dibaca sebagai kerja sama yang tenang dan minim drama. Suasana kerja kalian bikin fokus.",
                "saran": [
                    "Minim konflik bukan berarti tanpa masukan. Tetap biasakan saling review supaya kualitas terjaga.",
                    "Suasana tenang cocok untuk kerja mendalam. Ambil proyek yang butuh fokus panjang.",
                ],
            },
        },
    },
    "sri": {
        "name": "Sri",
        "tone": "baik",
        "meaning": "Rezeki melimpah dan kebutuhan tercukupi.",
        "lens": {
            "asmara": {
                "inti": "Sri dibaca sebagai hubungan yang rezekinya melimpah dan kebutuhan rumah tangganya tercukupi.",
                "saran": [
                    "Rezeki lancar paling terasa kalau diatur bersama. Tentukan pos tabungan, kebutuhan, dan senang-senang.",
                    "Syukuri kecukupan dengan berbagi ke keluarga atau orang sekitar yang sedang butuh.",
                ],
            },
            "pertemanan": {
                "inti": "Sri dibaca sebagai pertemanan yang saling membawa rezeki, misalnya info peluang atau koneksi baru.",
                "saran": [
                    "Saling bagi info peluang kerja atau usaha. Pertemanan yang saling menguatkan biasanya makin awet.",
                    "Jangan hitung-hitungan berlebihan saat saling bantu. Kemurahan hati bikin rezeki terasa lebih lapang.",
                ],
            },
            "kerja": {
                "inti": "Sri dibaca sebagai kerja sama yang mendatangkan rezeki, cocok untuk usaha atau proyek yang menghasilkan.",
                "saran": [
                    "Sepakati pembagian hasil yang adil sejak awal supaya rezeki yang datang tidak memicu salah paham.",
                    "Investasikan sebagian hasil untuk mengembangkan kemampuan tim.",
                ],
            },
        },
    },
    "dana": {
        "name": "Dana",
        "tone": "baik",
        "meaning": "Makmur dan kuat secara finansial.",
        "lens": {
            "asmara": {
                "inti": "Dana dibaca sebagai hubungan yang makmur dan kuat secara finansial dalam jangka panjang.",
                "saran": [
                    "Kemakmuran butuh rencana. Susun target keuangan jangka panjang bersama, misalnya dana darurat dan rumah.",
                    "Jangan biarkan uang jadi satu-satunya ukuran. Tetap investasikan waktu untuk kebersamaan.",
                ],
            },
            "pertemanan": {
                "inti": "Dana dibaca sebagai pertemanan yang bisa berkembang jadi kerja sama menguntungkan.",
                "saran": [
                    "Kalau mau patungan usaha, pisahkan urusan bisnis dan pertemanan dengan kesepakatan tertulis.",
                    "Saling dukung keputusan finansial yang sehat, misalnya menabung atau belajar investasi bareng.",
                ],
            },
            "kerja": {
                "inti": "Dana dibaca sebagai kerja sama yang kuat secara finansial dan berpotensi berkembang besar.",
                "saran": [
                    "Buat laporan keuangan sederhana sejak awal. Usaha yang tumbuh cepat butuh catatan yang rapi.",
                    "Tentukan target bersama yang terukur supaya pertumbuhan kalian tetap terarah.",
                ],
            },
        },
    },
    "lara": {
        "name": "Lara",
        "tone": "berat",
        "meaning": "Banyak hambatan, termasuk soal kesehatan.",
        "lens": {
            "asmara": {
                "inti": "Lara dibaca sebagai hubungan yang sering diuji hambatan, termasuk urusan kesehatan salah satu atau keduanya.",
                "saran": [
                    "Jadikan hidup sehat sebagai kebiasaan bersama, dari pola tidur sampai cek kesehatan rutin.",
                    "Saat salah satu sedang drop, bagi peran dengan jelas supaya beban tidak jatuh ke satu orang saja.",
                ],
            },
            "pertemanan": {
                "inti": "Lara dibaca sebagai pertemanan yang sering diuji hambatan, tapi justru membentuk rasa saling jaga.",
                "saran": [
                    "Saling ingatkan untuk istirahat dan jaga kesehatan. Teman yang peduli itu support system terbaik.",
                    "Saat rencana sering batal, jangan langsung kecewa. Cari cara ketemu yang lebih ringan dan fleksibel.",
                ],
            },
            "kerja": {
                "inti": "Lara dibaca sebagai kerja sama yang sering bertemu hambatan dan butuh cadangan rencana.",
                "saran": [
                    "Siapkan rencana cadangan untuk tenggat penting. Hambatan terasa lebih ringan kalau sudah diantisipasi.",
                    "Jaga beban kerja tetap manusiawi. Tim yang kelelahan lebih gampang terhambat.",
                ],
            },
        },
    },
    "pati": {
        "name": "Pati",
        "tone": "berat",
        "meaning": "Tanda paling berat dalam petung ini, dibaca sebagai ujian terbesar bagi keduanya.",
        "lens": {
            "asmara": {
                "inti": "Pati dianggap tanda paling berat dalam petung ini. Primbon membacanya sebagai ujian terbesar bagi keduanya.",
                "saran": [
                    "Label berat bukan takdir. Banyak keluarga Jawa menimbang petung lain juga, jadi lihat gambaran utuhnya.",
                    "Fokus pada hal yang bisa kalian kendalikan: saling jaga, jujur, dan hidup sehat bersama.",
                ],
            },
            "pertemanan": {
                "inti": "Pati dianggap tanda paling berat dalam petung ini. Pertemanan kalian mungkin sering diuji jarak atau keadaan.",
                "saran": [
                    "Pertemanan yang teruji justru bisa paling dalam. Tetap kabari satu sama lain meski sibuk.",
                    "Jangan jadikan label ini alasan menjauh. Lihat bagaimana kalian saling memperlakukan selama ini.",
                ],
            },
            "kerja": {
                "inti": "Pati dianggap tanda paling berat dalam petung ini. Kerja sama kalian mungkin sering diuji situasi di luar kendali.",
                "saran": [
                    "Susun kesepakatan kerja yang jelas, termasuk rencana kalau salah satu harus mundur.",
                    "Label berat bukan vonis. Evaluasi kerja sama berdasarkan hasil nyata, bukan hanya hitungan.",
                ],
            },
        },
    },
    "lungguh": {
        "name": "Lungguh",
        "tone": "baik",
        "meaning": "Stabil, aman, dan terhormat.",
        "lens": {
            "asmara": {
                "inti": "Lungguh dibaca sebagai rumah tangga yang stabil, aman, dan terhormat di mata lingkungan.",
                "saran": [
                    "Stabilitas itu fondasi. Pakai rasa aman ini untuk berani merencanakan mimpi besar bersama.",
                    "Tetap rawat keintiman lewat obrolan jujur, supaya hubungan yang stabil tidak berubah jadi datar.",
                ],
            },
            "pertemanan": {
                "inti": "Lungguh dibaca sebagai pertemanan yang stabil dan bisa diandalkan dalam jangka panjang.",
                "saran": [
                    "Teman yang stabil itu langka. Tunjukkan apresiasi, misalnya lewat pesan singkat di hari penting.",
                    "Coba rencanakan satu pengalaman besar bareng, misalnya perjalanan, supaya pertemanan tetap segar.",
                ],
            },
            "kerja": {
                "inti": "Lungguh dibaca sebagai kerja sama yang stabil dan dipercaya. Kalian cocok untuk tanggung jawab jangka panjang.",
                "saran": [
                    "Stabilitas cocok untuk proyek panjang. Ambil peran yang butuh konsistensi, bukan cuma kecepatan.",
                    "Jaga agar stabil tidak berubah jadi stagnan. Sesekali coba cara kerja baru bersama.",
                ],
            },
        },
    },
    "gentho": {
        "name": "Gentho",
        "tone": "campur",
        "meaning": "Jarang dikaruniai keturunan.",
        "lens": {
            "asmara": {
                "inti": "Gentho dibaca sebagai pasangan yang jarang dikaruniai keturunan. Primbon mencatatnya sebagai ujian kesabaran berdua.",
                "saran": [
                    "Kalau kalian memang ingin punya anak, rencanakan bareng dan cek kesehatan sejak awal. Hitungan tidak menggantikan dokter.",
                    "Bahagia berdua tidak harus menunggu apa pun. Rawat hubungan kalian sebagai tujuan, bukan sekadar jalan.",
                ],
            },
            "pertemanan": {
                "inti": "Gentho dibaca sebagai pertemanan yang jarang melahirkan proyek atau rencana bareng, meski kalian nyaman satu sama lain.",
                "saran": [
                    "Coba wujudkan satu ide kecil berdua, misalnya konten atau acara, supaya pertemanan punya cerita yang bisa dikenang.",
                    "Nggak apa-apa kalau pertemanan kalian santai. Yang penting tetap saling hadir saat dibutuhkan.",
                ],
            },
            "kerja": {
                "inti": "Gentho dibaca sebagai kerja sama yang sering lambat membuahkan hasil nyata, walau kalian cocok secara personal.",
                "saran": [
                    "Pecah target jadi hasil kecil yang bisa dilihat tiap minggu, supaya kerja sama kalian terasa produktif.",
                    "Evaluasi berkala apa yang sudah jadi dan apa yang mandek. Keputusan berbasis data bikin tim lebih tenang.",
                ],
            },
        },
    },
    "gembili": {
        "name": "Gembili",
        "tone": "baik",
        "meaning": "Dikaruniai banyak keturunan.",
        "lens": {
            "asmara": {
                "inti": "Gembili dibaca sebagai pasangan yang dikaruniai banyak keturunan. Rumah kalian digambarkan ramai dan hangat.",
                "saran": [
                    "Keluarga besar butuh rencana matang. Obrolkan soal pendidikan, tabungan, dan pembagian peran sejak dini.",
                    "Di tengah keramaian keluarga, tetap sisihkan waktu berdua supaya hubungan kalian nggak cuma soal urusan rumah.",
                ],
            },
            "pertemanan": {
                "inti": "Gembili dibaca sebagai pertemanan yang subur. Dari kalian berdua sering lahir lingkaran teman dan rencana baru.",
                "saran": [
                    "Kalian jago mengumpulkan orang. Pakai itu untuk bikin komunitas yang saling dukung, bukan cuma ramai.",
                    "Makin besar lingkaran, makin penting waktu berdua. Jaga obrolan dekat supaya kalian nggak cuma ketemu di keramaian.",
                ],
            },
            "kerja": {
                "inti": "Gembili dibaca sebagai kerja sama yang produktif. Ide kalian gampang berkembang jadi banyak proyek turunan.",
                "saran": [
                    "Banyak ide itu bagus, tapi pilih prioritas. Tentukan tiga proyek utama supaya tenaga tim nggak tercecer.",
                    "Dokumentasikan setiap ide yang muncul. Yang belum sempat dikerjakan hari ini bisa jadi peluang besok.",
                ],
            },
        },
    },
    "punggel": {
        "name": "Punggel",
        "tone": "berat",
        "meaning": "Tanda paling berat dalam petung ini, dibaca sebagai hubungan yang rawan terputus.",
        "lens": {
            "asmara": {
                "inti": "Punggel dianggap tanda paling berat di petung sisa bagi 4. Primbon membacanya sebagai hubungan yang rawan terputus.",
                "saran": [
                    "Label berat bukan takdir. Lihat juga hasil petung lain, lalu nilai hubungan kalian dari cara kalian saling memperlakukan.",
                    "Bangun kebiasaan menyelesaikan masalah sampai tuntas. Hubungan yang rawan putus paling butuh komunikasi yang jujur.",
                ],
            },
            "pertemanan": {
                "inti": "Punggel dianggap tanda paling berat di petung ini. Pertemanan kalian digambarkan mudah terputus kalau tidak dirawat.",
                "saran": [
                    "Kabari satu sama lain walau sibuk. Pesan singkat rutin sering jadi pembeda antara teman lama dan mantan teman.",
                    "Kalau ada salah paham, selesaikan langsung. Jangan biarkan asumsi yang memutus pertemanan kalian.",
                ],
            },
            "kerja": {
                "inti": "Punggel dianggap tanda paling berat di petung ini. Kerja sama kalian digambarkan rawan berhenti di tengah jalan.",
                "saran": [
                    "Siapkan kesepakatan tertulis, termasuk rencana kalau salah satu harus mundur, supaya proyek tetap aman.",
                    "Nilai kerja sama dari hasil nyata. Kalau progres bagus, label berat ini cukup jadi pengingat untuk berhati-hati.",
                ],
            },
        },
    },
    "wasesa_segara": {
        "name": "Wasesa Segara",
        "tone": "baik",
        "meaning": "Pemaaf, bijaksana, dan berwibawa, luas hatinya seperti samudra.",
        "lens": {
            "asmara": {
                "inti": "Wasesa Segara dibaca sebagai pasangan yang luas hatinya seperti samudra: pemaaf, bijak, dan berwibawa.",
                "saran": [
                    "Sifat pemaaf itu kekuatan, asal masalahnya tetap dibahas. Memaafkan bukan berarti memendam.",
                    "Kalian cocok jadi tempat curhat keluarga. Tetap pasang batas supaya energi berdua nggak habis untuk orang lain.",
                ],
            },
            "pertemanan": {
                "inti": "Wasesa Segara dibaca sebagai pertemanan yang lapang dan pemaaf. Kalian jarang ribut lama karena gampang memaafkan.",
                "saran": [
                    "Hati yang lapang bikin pertemanan awet. Tetap jujur soal hal yang mengganjal supaya nggak jadi beban diam-diam.",
                    "Kalian sering jadi penengah di tongkrongan. Pakai itu untuk merangkul, bukan memikul semua masalah orang.",
                ],
            },
            "kerja": {
                "inti": "Wasesa Segara dibaca sebagai kerja sama yang tenang dan bijak. Kalian gampang dipercaya memimpin dan menengahi.",
                "saran": [
                    "Kalian cocok pegang peran koordinasi. Pastikan keputusan tetap tegas walau suasananya dijaga tetap adem.",
                    "Pemaaf boleh, tapi evaluasi tetap perlu. Catat pelajaran dari tiap kesalahan supaya tim terus berkembang.",
                ],
            },
        },
    },
    "tunggak_semi": {
        "name": "Tunggak Semi",
        "tone": "campur",
        "meaning": "Rezeki mudah datang, tapi rawan sakit.",
        "lens": {
            "asmara": {
                "inti": "Tunggak Semi dibaca seperti tunggul yang bersemi lagi: rezeki kalian mudah datang, tapi kesehatan perlu dijaga.",
                "saran": [
                    "Rezeki lancar paling terasa kalau badan sehat. Jadwalkan cek kesehatan dan olahraga bareng sebagai kebiasaan.",
                    "Sisihkan sebagian rezeki untuk dana kesehatan. Siap sebelum butuh bikin kalian lebih tenang.",
                ],
            },
            "pertemanan": {
                "inti": "Tunggak Semi dibaca sebagai pertemanan yang sering membawa peluang, tapi gampang kelelahan karena terlalu banyak agenda.",
                "saran": [
                    "Saling bagi peluang itu keren. Jangan lupa saling ingatkan istirahat supaya semangat kalian nggak cepat habis.",
                    "Pilih agenda bareng yang bikin segar, bukan cuma produktif. Pertemanan juga butuh waktu santai.",
                ],
            },
            "kerja": {
                "inti": "Tunggak Semi dibaca sebagai kerja sama yang cepat mendatangkan hasil, tapi rawan membuat tim kelelahan.",
                "saran": [
                    "Rezeki proyek yang lancar bisa bikin lupa batas. Atur ritme kerja supaya hasil bagus nggak dibayar dengan burnout.",
                    "Siapkan cadangan orang untuk tugas penting, jadi kerja tetap jalan saat salah satu harus istirahat.",
                ],
            },
        },
    },
    "satriya_wibawa": {
        "name": "Satriya Wibawa",
        "tone": "baik",
        "meaning": "Mendapat keluhuran, kemuliaan, dan kewibawaan.",
        "lens": {
            "asmara": {
                "inti": "Satriya Wibawa dibaca sebagai pasangan yang mendapat keluhuran dan kewibawaan. Kalian cenderung dihormati orang.",
                "saran": [
                    "Wibawa paling awet kalau dibarengi rendah hati. Tetap sapa dan bantu orang sekitar tanpa merasa di atas.",
                    "Kehormatan dari luar perlu diimbangi kehangatan di dalam. Jangan lupa bercanda dan santai berdua.",
                ],
            },
            "pertemanan": {
                "inti": "Satriya Wibawa dibaca sebagai pertemanan yang disegani. Kalian berdua sering dipercaya dan dimintai pendapat.",
                "saran": [
                    "Pakai pengaruh kalian untuk hal baik, misalnya merangkul teman yang sering tertinggal.",
                    "Disegani bukan berarti harus selalu benar. Tetap terbuka saat teman lain punya pendapat berbeda.",
                ],
            },
            "kerja": {
                "inti": "Satriya Wibawa dibaca sebagai kerja sama yang membawa nama baik. Kalian cocok maju sebagai wajah tim.",
                "saran": [
                    "Reputasi bagus membuka banyak pintu. Jaga dengan menepati janji kerja sekecil apa pun.",
                    "Bagi sorotan dengan anggota tim lain supaya kewibawaan kalian terasa adil, bukan dominan.",
                ],
            },
        },
    },
    "sumur_sinaba": {
        "name": "Sumur Sinaba",
        "tone": "baik",
        "meaning": "Menjadi sumber ilmu dan teladan, didatangi banyak orang seperti sumur.",
        "lens": {
            "asmara": {
                "inti": "Sumur Sinaba dibaca seperti sumur yang didatangi banyak orang: kalian jadi teladan dan tempat orang belajar.",
                "saran": [
                    "Jadi panutan itu berat. Sepakati kapan kalian menerima tamu dan kapan waktu khusus untuk berdua.",
                    "Terus belajar bareng, dari kelas online sampai buku. Sumur yang dalam tetap butuh diisi supaya tidak kering.",
                ],
            },
            "pertemanan": {
                "inti": "Sumur Sinaba dibaca sebagai pertemanan yang jadi rujukan. Banyak teman datang ke kalian untuk minta saran.",
                "saran": [
                    "Berbagi ilmu itu keren. Tetap jaga energi dengan bilang tidak saat kalian sendiri sedang butuh istirahat.",
                    "Ajak teman lain ikut belajar bareng supaya kalian nggak jadi satu-satunya tempat bertanya.",
                ],
            },
            "kerja": {
                "inti": "Sumur Sinaba dibaca sebagai kerja sama yang jadi sumber pengetahuan tim. Kalian cocok jadi mentor bersama.",
                "saran": [
                    "Tulis pengetahuan kalian jadi panduan tim. Ilmu yang terdokumentasi bisa dipakai walau kalian sedang sibuk.",
                    "Sisihkan waktu untuk belajar hal baru berdua supaya kalian tetap relevan sebagai rujukan.",
                ],
            },
        },
    },
    "satriya_wirang": {
        "name": "Satriya Wirang",
        "tone": "berat",
        "meaning": "Sering menghadapi kesusahan dan rasa malu, disarankan menjalani selamatan.",
        "lens": {
            "asmara": {
                "inti": "Satriya Wirang dibaca sebagai pasangan yang sering diuji kesusahan dan rasa malu. Primbon menyarankan selamatan.",
                "saran": [
                    "Hadapi masalah berdua dan jangan saling menyalahkan di depan orang lain. Martabat pasangan dijaga bersama.",
                    "Kalau keluarga memegang tradisi, selamatan bisa jadi cara menguatkan niat. Yang terpenting tetap komitmen kalian.",
                ],
            },
            "pertemanan": {
                "inti": "Satriya Wirang dibaca sebagai pertemanan yang sering diuji situasi canggung atau masalah yang bikin malu.",
                "saran": [
                    "Saling tutupi kekurangan di depan umum dan bahas secara pribadi. Teman sejati menjaga nama baik satu sama lain.",
                    "Jangan jadikan momen canggung sebagai bahan ejekan yang berulang. Candaan juga ada batasnya.",
                ],
            },
            "kerja": {
                "inti": "Satriya Wirang dibaca sebagai kerja sama yang rawan tersandung masalah yang mempermalukan tim di depan orang.",
                "saran": [
                    "Cek ulang pekerjaan sebelum dipresentasikan. Ketelitian kecil mencegah momen memalukan di depan klien.",
                    "Kalau terjadi kesalahan, akui bersama dan tawarkan solusi. Cara menangani masalah menentukan nama baik tim.",
                ],
            },
        },
    },
    "bumi_kapetak": {
        "name": "Bumi Kapetak",
        "tone": "campur",
        "meaning": "Pendiam dan pekerja keras, tapi cenderung tertutup dari lingkungan.",
        "lens": {
            "asmara": {
                "inti": "Bumi Kapetak dibaca sebagai pasangan yang tekun bekerja keras, tapi cenderung tertutup dan jarang bergaul.",
                "saran": [
                    "Kerja keras kalian patut dibanggakan. Sesekali buka pintu untuk keluarga dan teman supaya nggak merasa sendirian.",
                    "Luangkan waktu untuk ngobrol santai berdua. Pasangan yang pendiam tetap butuh ruang untuk saling cerita.",
                ],
            },
            "pertemanan": {
                "inti": "Bumi Kapetak dibaca sebagai pertemanan yang setia tapi tertutup. Kalian nyaman berdua dan jarang membuka lingkaran.",
                "saran": [
                    "Coba kenalkan satu teman baru ke lingkaran kalian. Pertemanan yang terbuka justru makin kuat.",
                    "Kesetiaan kalian berharga. Tunjukkan lewat tindakan kecil, misalnya menemani saat teman sedang berjuang.",
                ],
            },
            "kerja": {
                "inti": "Bumi Kapetak dibaca sebagai kerja sama yang rajin dan tekun, tapi jarang terlihat oleh tim atau atasan.",
                "saran": [
                    "Laporkan progres secara rutin. Kerja keras yang tidak terlihat sering kalah pamor dari yang rajin update.",
                    "Libatkan tim lain sesekali supaya kontribusi kalian dikenal dan kalian nggak bekerja terlalu terisolasi.",
                ],
            },
        },
    },
    "lebu_katiup_angin": {
        "name": "Lebu Katiup Angin",
        "tone": "berat",
        "meaning": "Seperti debu tertiup angin: sering kesusahan dan cita-cita sulit tercapai.",
        "lens": {
            "asmara": {
                "inti": "Lebu Katiup Angin dibaca seperti debu tertiup angin: sering kesusahan dan cita-cita kalian sulit menetap.",
                "saran": [
                    "Tulis satu tujuan bersama yang konkret, lalu kejar pelan-pelan. Arah yang jelas bikin kalian nggak mudah terombang-ambing.",
                    "Label berat bukan vonis. Bandingkan dengan hasil petung lain dan nilai hubungan kalian dari kenyataan sehari-hari.",
                ],
            },
            "pertemanan": {
                "inti": "Lebu Katiup Angin dibaca sebagai pertemanan yang gampang tercerai keadaan, misalnya pindah kota atau kesibukan.",
                "saran": [
                    "Bikin ritual kecil yang konsisten, misalnya video call bulanan, supaya jarak tidak menghapus pertemanan.",
                    "Rencana yang sering batal bukan tanda kalian nggak peduli. Tetap kabari dan cari waktu yang lebih fleksibel.",
                ],
            },
            "kerja": {
                "inti": "Lebu Katiup Angin dibaca sebagai kerja sama yang rawan kehilangan arah dan targetnya sering berubah-ubah.",
                "saran": [
                    "Kunci tujuan proyek di awal dan catat setiap perubahan. Arah yang tertulis mencegah kerja tercecer.",
                    "Pilih satu ukuran keberhasilan yang jelas supaya kalian tahu kapan harus lanjut dan kapan harus berhenti.",
                ],
            },
        },
    },
}
