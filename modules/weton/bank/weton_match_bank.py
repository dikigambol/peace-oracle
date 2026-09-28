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
}
