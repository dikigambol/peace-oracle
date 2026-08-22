import ephem
import requests
import datetime
import math
import hashlib
from .horoscope_bank import get_daily_horoscope, get_daily_youtube_track, get_ai_compatibility_modes
from .roasting_bank import determine_zodiac, get_roast, get_relationship_roast, get_ai_roast, get_ai_relationship_roast
# DATA ZODIAK STATIK
# ============================================================
ZODIAC_DATA = {
    "aries": {
        "name": "Aries", "date_range": "21 Maret - 19 April",
        "element": "Api", "ruler": "Mars", "ruler_planet": "mars",
        "strengths": ["Pemberani", "Bertekad kuat", "Percaya diri", "Antusias"],
        "weaknesses": ["Tidak sabaran", "Moody", "Mudah marah", "Impulsif"],
        "lucky_number": 9, "lucky_color": "Merah",
        "compatible_signs": ["Leo", "Sagittarius", "Gemini"],
        "base_ratings": {"love": 85, "career": 90, "health": 80}
    },
    "taurus": {
        "name": "Taurus", "date_range": "20 April - 20 Mei",
        "element": "Tanah", "ruler": "Venus", "ruler_planet": "venus",
        "strengths": ["Dapat diandalkan", "Sabar", "Praktis", "Setia"],
        "weaknesses": ["Keras kepala", "Posesif", "Kaku"],
        "lucky_number": 6, "lucky_color": "Hijau",
        "compatible_signs": ["Virgo", "Capricorn", "Cancer"],
        "base_ratings": {"love": 90, "career": 80, "health": 85}
    },
    "gemini": {
        "name": "Gemini", "date_range": "21 Mei - 20 Juni",
        "element": "Udara", "ruler": "Merkurius", "ruler_planet": "mercury",
        "strengths": ["Lemah lembut", "Penuh kasih", "Ingin tahu", "Mudah beradaptasi"],
        "weaknesses": ["Gugup", "Tidak konsisten", "Ragu-ragu"],
        "lucky_number": 5, "lucky_color": "Kuning",
        "compatible_signs": ["Libra", "Aquarius", "Aries"],
        "base_ratings": {"love": 75, "career": 85, "health": 90}
    },
    "cancer": {
        "name": "Cancer", "date_range": "21 Juni - 22 Juli",
        "element": "Air", "ruler": "Bulan", "ruler_planet": "moon",
        "strengths": ["Gigih", "Imajinasi tinggi", "Setia", "Empatis"],
        "weaknesses": ["Moody", "Pesimis", "Curigaan", "Kurang percaya diri"],
        "lucky_number": 2, "lucky_color": "Putih",
        "compatible_signs": ["Scorpio", "Pisces", "Taurus"],
        "base_ratings": {"love": 95, "career": 70, "health": 80}
    },
    "leo": {
        "name": "Leo", "date_range": "23 Juli - 22 Agustus",
        "element": "Api", "ruler": "Matahari", "ruler_planet": "sun",
        "strengths": ["Kreatif", "Penuh gairah", "Dermawan", "Hangat"],
        "weaknesses": ["Arogan", "Keras kepala", "Egosentris", "Malas"],
        "lucky_number": 1, "lucky_color": "Emas",
        "compatible_signs": ["Aries", "Sagittarius", "Libra"],
        "base_ratings": {"love": 88, "career": 92, "health": 85}
    },
    "virgo": {
        "name": "Virgo", "date_range": "23 Agustus - 22 September",
        "element": "Tanah", "ruler": "Merkurius", "ruler_planet": "mercury",
        "strengths": ["Setia", "Analitis", "Baik hati", "Pekerja keras"],
        "weaknesses": ["Pemalu", "Suka cemas", "Terlalu kritis pada diri sendiri dan orang lain"],
        "lucky_number": 3, "lucky_color": "Perak",
        "compatible_signs": ["Taurus", "Capricorn", "Scorpio"],
        "base_ratings": {"love": 80, "career": 88, "health": 92}
    },
    "libra": {
        "name": "Libra", "date_range": "23 September - 22 Oktober",
        "element": "Udara", "ruler": "Venus", "ruler_planet": "venus",
        "strengths": ["Kooperatif", "Diplomatis", "Anggun", "Adil"],
        "weaknesses": ["Ragu-ragu", "Menghindari konfrontasi", "Pendendam"],
        "lucky_number": 7, "lucky_color": "Merah Muda",
        "compatible_signs": ["Gemini", "Aquarius", "Leo"],
        "base_ratings": {"love": 92, "career": 78, "health": 88}
    },
    "scorpio": {
        "name": "Scorpio", "date_range": "23 Oktober - 21 November",
        "element": "Air", "ruler": "Pluto", "ruler_planet": "mars",
        "strengths": ["Cerdik", "Kuat", "Pemberani", "Penuh gairah"],
        "weaknesses": ["Kurang percaya orang", "Cemburuan", "Tertutup", "Keras"],
        "lucky_number": 8, "lucky_color": "Merah Karat",
        "compatible_signs": ["Cancer", "Pisces", "Virgo"],
        "base_ratings": {"love": 85, "career": 95, "health": 80}
    },
    "sagittarius": {
        "name": "Sagittarius", "date_range": "22 November - 21 Desember",
        "element": "Api", "ruler": "Jupiter", "ruler_planet": "jupiter",
        "strengths": ["Dermawan", "Idealis", "Humoris"],
        "weaknesses": ["Bicara tanpa disaring", "Sangat tidak sabar", "Suka berjanji berlebihan"],
        "lucky_number": 4, "lucky_color": "Biru",
        "compatible_signs": ["Aries", "Leo", "Aquarius"],
        "base_ratings": {"love": 82, "career": 85, "health": 95}
    },
    "capricorn": {
        "name": "Capricorn", "date_range": "22 Desember - 19 Januari",
        "element": "Tanah", "ruler": "Saturnus", "ruler_planet": "saturn",
        "strengths": ["Bertanggung jawab", "Disiplin", "Kontrol diri baik", "Manajer yang handal"],
        "weaknesses": ["Merasa tahu segalanya", "Sulit memaafkan", "Meremehkan orang lain", "Pesimis"],
        "lucky_number": 10, "lucky_color": "Cokelat",
        "compatible_signs": ["Taurus", "Virgo", "Pisces"],
        "base_ratings": {"love": 78, "career": 94, "health": 87}
    },
    "aquarius": {
        "name": "Aquarius", "date_range": "20 Januari - 18 Februari",
        "element": "Udara", "ruler": "Uranus", "ruler_planet": "saturn",
        "strengths": ["Progresif", "Orisinal", "Mandiri", "Humanis"],
        "weaknesses": ["Menghindari emosi", "Tempramental", "Keras kepala"],
        "lucky_number": 11, "lucky_color": "Biru Langit",
        "compatible_signs": ["Gemini", "Libra", "Sagittarius"],
        "base_ratings": {"love": 87, "career": 89, "health": 84}
    },
    "pisces": {
        "name": "Pisces", "date_range": "19 Februari - 20 Maret",
        "element": "Air", "ruler": "Neptunus", "ruler_planet": "jupiter",
        "strengths": ["Penuh kasih", "Artistik", "Intuitif", "Lemah lembut", "Bijaksana"],
        "weaknesses": ["Penakut", "Terlalu mudah percaya", "Mudah sedih", "Suka melarikan diri dari kenyataan"],
        "lucky_number": 7, "lucky_color": "Hijau Laut",
        "compatible_signs": ["Cancer", "Scorpio", "Capricorn"],
        "base_ratings": {"love": 90, "career": 80, "health": 91}
    }
}

# MATRIX KECOCOKAN ELEMEN
ELEMENT_COMPATIBILITY = {
    "Api": {
        "Api": {"score": 85, "love": 88, "comm": 85, "trust": 80, "future": 85},
        "Tanah": {"score": 60, "love": 62, "comm": 58, "trust": 70, "future": 65},
        "Udara": {"score": 92, "love": 90, "comm": 95, "trust": 88, "future": 92},
        "Air": {"score": 50, "love": 55, "comm": 45, "trust": 50, "future": 52}
    },
    "Tanah": {
        "Api": {"score": 60, "love": 62, "comm": 58, "trust": 70, "future": 65},
        "Tanah": {"score": 88, "love": 85, "comm": 82, "trust": 95, "future": 90},
        "Udara": {"score": 55, "love": 52, "comm": 60, "trust": 58, "future": 55},
        "Air": {"score": 90, "love": 94, "comm": 88, "trust": 92, "future": 90}
    },
    "Udara": {
        "Api": {"score": 92, "love": 90, "comm": 95, "trust": 88, "future": 92},
        "Tanah": {"score": 55, "love": 52, "comm": 60, "trust": 58, "future": 55},
        "Udara": {"score": 82, "love": 80, "comm": 92, "trust": 75, "future": 80},
        "Air": {"score": 65, "love": 68, "comm": 62, "trust": 60, "future": 65}
    },
    "Air": {
        "Api": {"score": 50, "love": 55, "comm": 45, "trust": 50, "future": 52},
        "Tanah": {"score": 90, "love": 94, "comm": 88, "trust": 92, "future": 90},
        "Udara": {"score": 65, "love": 68, "comm": 62, "trust": 60, "future": 65},
        "Air": {"score": 94, "love": 96, "comm": 90, "trust": 95, "future": 92}
    }
}

# DATA GENERAL
GENERAL_CHARACTERISTICS = {
    "aries": {
        "physical_traits": ["Tatapan mata tajam & percaya diri", "Bahu tegap & langkah kaki mantap", "Ekspresi wajah tegas & energik", "Gaya berpakaian bold & sporty"],
        "personality": "Aries adalah sosok pelopor yang mandiri, berani, dan berjiwa pemimpin tinggi. Mereka langsung pada inti masalah tanpa berbelit-belit, bersemangat membara, namun terkadang mudah tersulut emosi saat tidak sabar.",
        "habits": ["Bergerak dan berjalan dengan ritme cepat", "Sering memotong pembicaraan karena ide sudah di ubun-ubun", "Beli barang tanpa pikir panjang kalau sudah suka", "Langsung menyuarakan keluh kesah tanpa ditutup-tutupi"],
        "animal_soulmate": {"name": "🐕 Doberman / Elang Jawa", "description": "Sama-sama berjiwa pemimpin, energik, berani, dan setia. Punya intuisi kuat untuk melindungi kelompoknya."},
        "cosmic_pantry": {"taste_profile": "🌶️ Pedas, Rich & Rempah Tajam", "favorite_food": "Ayam Geprek Sambal Korek & Espresso Double Shot", "food_habit": "Suka makanan berasa tajam yang bikin melek. Makan cepat karena gak betah kelamaan di meja."},
        "astro_decor": {"style": "🔥 Industrial Sporty", "key_elements": "Pencahayaan terang, area mini workout, aksen logam & warna merah berani", "vibe": "Energetik, bebas rasa terkungkung, dan fungsional"},
        "fun_fact": "Aries kalau ditantang 'gak bakal berani', malah langsung dilakuin detik itu juga cuma buat ngebuktiin mereka bisa."
    },
    "taurus": {
        "physical_traits": ["Postur tubuh kokoh & proporsional", "Tatapan mata hangat & menenangkan", "Gaya busana kasual tapi terkesan mahal", "Suara lembut dengan nada tenang"],
        "personality": "Taurus dikenal sangat setia, penyabar, dan praktis. Mereka mencintai kenyamanan, estetika tinggi, dan kestabilan finansial. Sekali mengambil keputusan, Taurus sangat sulit digoyahkan.",
        "habits": ["Selalu punya spot tempat makan/ngopi favorit yang tak tergantikan", "Suka mengelus bahan pakaian halus saat belanja", "Checkout barang estetik yang bikin kamar makin nyaman", "Rela berjalan jauh demi makanan yang enak"],
        "animal_soulmate": {"name": "🐱 Kucing Persian / Beruang Panda", "description": "Mencintai kedamaian, tidur berkualitas, kenyamanan ekstrem, dan suka ngemil santai di tempat hangat."},
        "cosmic_pantry": {"taste_profile": "🍯 Manis, Creamy & Savory Gourmet", "favorite_food": "Matcha Latte, Truffle Pasta & Artisan Croissant", "food_habit": "Sangat pemilih soal rasa. Rela beli makanan mahal asal kualitas dan estetikanya dapet."},
        "astro_decor": {"style": "🌿 Warm Earthy & Luxury Cozy", "key_elements": "Kasur empuk kualitas super, karpet bulu, diffuser wewangian kayu cedar, & pencahayaan hangat", "vibe": "Tempat perlindungan ternyaman bagaikan resor bintang lima"},
        "fun_fact": "Taurus bisa tahan gak keluar rumah seminggu penuh asal persediaan makanan dan kasur nyamannya terpenuhi."
    },
    "gemini": {
        "physical_traits": ["Mata berbinar penuh rasa ingin tahu", "Gestur tangan sangat aktif saat berbicara", "Wajah tampak awet muda (youthful)", "Gaya berpakaian trendi & selalu berganti"],
        "personality": "Gemini adalah sosok komunikator yang cerdas, ramah, dan serba bisa. Pikiran mereka cepat menyerap informasi baru, namun terkadang cepat merasa bosan jika suasana terlalu monoton.",
        "habits": ["Buka puluhan tab browser sekaligus tanpa pernah ditutup", "Bisa ngobrolin topik filsafat lalu pindah ke gosip seleb dalam 5 detik", "Sering membalas chat di pikiran tapi lupa ngetik di HP", "Suka gonta-ganti playlist lagu sesuai perubahan mood"],
        "animal_soulmate": {"name": "🦜 Burung Beo Macaw / Kucing Siam", "description": "Cerdas, komunikatif, selalu ingin tahu hal baru, dan gak pernah kehabisan kata-kata untuk mengekspresikan diri."},
        "cosmic_pantry": {"taste_profile": "🍧 Ringan, Variatif & Snackable", "favorite_food": "Boba Tea, Dimsum, & Finger Foods", "food_habit": "Suka ngemil saat ngobrol atau kerja. Lebih milih nyobain 5 jenis camilan kecil ketimbang 1 porsi berat."},
        "astro_decor": {"style": "🎨 Eclectic Pop & Modern Library", "key_elements": "Rak buku penuh bacaan unik, dual monitor/gadget corner, poster estetik, & pencahayaan fleksibel", "vibe": "Kreatif, penuh warna, dan merangsang ide-ide baru"},
        "fun_fact": "Gemini bisa jadi orang paling introvert dan paling ekstrovert di hari yang sama."
    },
    "cancer": {
        "physical_traits": ["Raut wajah lembut & ramah", "Tatapan mata teduh & penuh empati", "Gaya pakaian cozy, simpel, dan berwarna lembut", "Senyuman manis yang membuat orang merasa aman"],
        "personality": "Cancer sangat emosional, intuitif, dan penyayang. Mereka memiliki naluri melindungi yang tinggi terhadap orang tersayang, namun cenderung menyembunyikan perasaan saat merasa terluka.",
        "habits": ["Menyimpan barang-barang penuh kenangan dari bertahun-tahun lalu", "Suka memasak atau menyajikan makanan untuk orang lain", "Matiin HP dan mengurung diri saat butuh recharge energi emosional", "Sering ketagihan dengerin lagu galau di malam hari"],
        "animal_soulmate": {"name": "🐰 Kelinci Angora / Kucing Scottish Fold", "description": "Sangat lembut, peka pada perasaan sekitar, menyukai kehangatan pelukan, dan sangat protektif pada rumahnya."},
        "cosmic_pantry": {"taste_profile": "🍲 Comfort Food & Masakan Rumah", "favorite_food": "Sup Ayam Hangat, Chocolate Lava Cake & Milk Tea", "food_habit": "Makan untuk merawat emosi (emotional comfort). Suka memasak untuk orang tersayang."},
        "astro_decor": {"style": "🌙 Soft Cottagecore & Vintage Warmth", "key_elements": "Bantal-bantal empuk, lampu tumblr temaram, foto kenangan keluarga, & sudut baca cozy", "vibe": "Aman, penuh kehangatan, dan menenangkan jiwa"},
        "fun_fact": "Cancer bisa ingat secara detail kejadian 5 tahun lalu lengkap dengan kalimat yang lo ucapin jam berapa."
    },
    "leo": {
        "physical_traits": ["Rambut lebat & bergaya menarik perhatian", "Postur dada tegap & percaya diri", "Senyum lebar yang menawan", "Gaya pakaian fashionable & elegan"],
        "personality": "Leo adalah sosok yang hangat, penuh gairah, dan dermawan. Mereka lahir sebagai pemimpin alami yang senang diapresiasi, jujur, dan memiliki loyalitas tinggi pada sahabatnya.",
        "habits": ["Spontan becermin atau ngerapihin rambut tiap lewat kaca", "Suka membelikan hadiah mewah untuk orang-orang tersayang", "Menjadi penyemarak suasana di tengah rombongan", "Suka mendapat pujian tulus atas pencapaiannya"],
        "animal_soulmate": {"name": "🦁 Singa Emas / Golden Retriever", "description": "Karismatik, hangat, berjiwa pelindung, dan menjadi pusat perhatian dengan energi kepemimpinan yang bersinar."},
        "cosmic_pantry": {"taste_profile": "👑 Mewah, Rich Flavor & Estetik", "favorite_food": "Wagyu Steak, Signature Cocktail & Gourmet Dessert", "food_habit": "Suka plating makanan yang memanjakan mata. Senang makan malam bersama kerabat sambil merayakan momen."},
        "astro_decor": {"style": "✨ Modern Glamour & Royal Gold", "key_elements": "Cermin besar berbingkai emas, aksen kain velvet, lampu kristal modern, & tempat piala/karya", "vibe": "Mewah, megah, dan membanggakan"},
        "fun_fact": "Meskipun kelihatan garang dan dominan, Leo sangat gampang melted cuma karena pelukan hangat atau pujian tulus."
    },
    "virgo": {
        "physical_traits": ["Penampilan selalu rapi, bersih, dan harum", "Tatapan mata analitis & jeli", "Postur tubuh simetris & cekatan", "Gaya pakaian simpel, clean, dan elegan"],
        "personality": "Virgo sosok yang sangat analitis, rapi, dan bertanggung jawab. Mereka memiliki pengamatan tajam terhadap detail yang terlewatkan orang lain dan selalu ingin membantu memecahkan masalah.",
        "habits": ["Suka merapikan barang yang miring atau tidak sejajar", "Selalu membuat to-do list harian sebelum beraktivitas", "Mencuci tangan atau bersih-bersih secara berkala", "Suka memberikan saran solusi praktis ketimbang cuma simpati"],
        "animal_soulmate": {"name": "🦊 Rubah Perak / Border Collie", "description": "Cerdas, analitis, cepat belajar, rapi, dan memiliki kesetiaan luar biasa pada pasangannya."},
        "cosmic_pantry": {"taste_profile": "🥗 Clean, Organik & Balanced", "favorite_food": "Smoothie Bowl, Fresh Salad & Organic Green Tea", "food_habit": "Sangat memperhatikan gizi dan kebersihan makanan. Suka mengatur meal prep harian."},
        "astro_decor": {"style": "🧹 Minimalist Japanese Zen & Clean Scandinavian", "key_elements": "Storage terorganisir rapi, tanaman harian pot kecil, bahan kayu alami, & meja kerja bebas debu", "vibe": "Rapi, jernih, tenang, dan efisien"},
        "fun_fact": "Virgo bisa kepikiran semalaman cuma gara-gara nemu typo di berkas penting yang udah dikirim."
    },
    "libra": {
        "physical_traits": ["Senyum simetris dengan wajah manis", "Gerak-gerik anggun & teratur", "Suara berirama & menyenangkan", "Gaya pakaian sangat stylish & serasi"],
        "personality": "Libra adalah pembawa keharmonisan, berjiwa seni tinggi, dan berwawasan adil. Mereka membenci konflik kasar dan selalu berusaha melihat masalah dari dua sudut pandang.",
        "habits": ["Lama memilih menu makanan karena semua kelihatan enak", "Suka bertanya pendapat ke 5 orang berbeda sebelum beli baju", "Mengubah posisi dekorasi kamar demi estetika yang pas", "Menyimpan foto-foto berpemandangan indah"],
        "animal_soulmate": {"name": "🦩 Burung Flamingo / Kucing Angora Ekor Panjang", "description": "Anggun, cantik, menyukai keharmonisan romantis, dan pandai beradaptasi dalam komunitasnya."},
        "cosmic_pantry": {"taste_profile": "🍰 Manis Estetik & Balance Taste", "favorite_food": "French Macarons, Croissant & Iced Oat Latte", "food_habit": "Makanan harus estetik buat difoto dulu sebelum dimakan. Menyukai perpaduan rasa yang seimbang."},
        "astro_decor": {"style": "🌸 Chic Parisian & Pastel Art Deco", "key_elements": "Cermin dinding bulat estetik, vas bunga segar, karya seni lukisan pastel, & lampu meja hias", "vibe": "Harmonis, romantis, dan penuh keindahan visual"},
        "fun_fact": "Libra bisa menghabiskan waktu 30 menit cuma buat milih warna font Canva."
    },
    "scorpio": {
        "physical_traits": ["Tatapan mata hipnotis, tajam, dan dalam", "Aura karismatik & misterius", "Ekspresi wajah sulit ditebak (poker face)", "Gaya pakaian dominan warna gelap/monokrom"],
        "personality": "Scorpio dikenal sangat fokus, tangguh, dan memiliki intuisi tajam. Mereka sangat menjaga privasi, penuh komitmen, dan dapat menjadi teman paling setia di saat sulit.",
        "habits": ["Mengecek latar belakang orang baru sebelum percaya penuh", "Suka berada di tempat tenang tanpa banyak gangguan", "Menyimpan rahasia teman dengan sangat rapat", "Mengamati dinamika ruangan tanpa banyak bicara"],
        "animal_soulmate": {"name": "🦅 Elang Hitam / Black Panther", "description": "Misterius, independen, berpikiran tajam, dan memiliki ketahanan jiwa yang tak tergoyahkan."},
        "cosmic_pantry": {"taste_profile": "🍷 Intense, Dark & Bold", "favorite_food": "Dark Chocolate 85%, Black Coffee & Seafood Pedas", "food_habit": "Menyukai makanan beraroma kuat dan intens. Menjaga privasi tempat dan suasana saat makan."},
        "astro_decor": {"style": "🖤 Gothic Modern & Moody Dark Mode", "key_elements": "Dinding kontras warna gelap, pencahayaan moody temaram, gorden tebal, & koleksi unik", "vibe": "Intim, misterius, dan eksklusif"},
        "fun_fact": "Detektor kebohongan Scorpio bisa mendeteksi ketidakjujuran bahkan sebelum orang tersebut selesai bicaranya."
    },
    "sagittarius": {
        "physical_traits": ["Kaki jenjang & gerak-gerik lincah", "Tawa lepas yang menularkan kebahagiaan", "Mata berekspresi antusias", "Gaya pakaian santai, sporty, dan nyaman"],
        "personality": "Sagittarius adalah sosok pencari kebebasan, jujur apa adanya, dan penuh optimisme. Mereka menyukai petualangan, pengetahuan baru, dan humor yang menyegarkan.",
        "habits": ["Tiba-tiba merencanakan perjalanan/trip tanpa persiapan lama", "Suka tertawa paling keras di tengah lelucon konyol", "Membaca artikel random jam 2 malam tentang sejarah dunia", "Langsung bicara jujur tanpa disaring dulu"],
        "animal_soulmate": {"name": "🐴 Kuda Liar / Siberian Husky", "description": "Berjiwa bebas, menyukai ruang terbuka, penuh energi humoris, dan tidak suka dikekang."},
        "cosmic_pantry": {"taste_profile": "🌮 Eksotis, Street Food & Kuliner Dunia", "favorite_food": "Tacos, Kebab, & Fresh Coconut Juice", "food_habit": "Suka mencoba makanan khas dari berbagai daerah/negara. Senang makan santai di alam terbuka."},
        "astro_decor": {"style": "🗺️ Bohemian Travel & World Explorer", "key_elements": "Peta dunia di dinding, souvenir perjalanan, hammock/kursi gantung, & tanaman tropis", "vibe": "Bebas, inspiratif, dan penuh cerita petualangan"},
        "fun_fact": "Sagittarius bisa merasa terkekang cuma gara-gara disuruh bikin jadwal kegiatan yang kaku."
    },
    "capricorn": {
        "physical_traits": ["Struktur tulang wajah tegas & berwibawa", "Tatapan mata fokus & tenang", "Penampilan profesional & matang", "Gaya pakaian klasik, berkualitas, dan timeless"],
        "personality": "Capricorn adalah definisi pekerja keras yang disiplin, berorientasi target, dan sangat bertanggung jawab. Di balik kesan kaku, mereka adalah pribadi yang sangat penyayang dan humoris bagi lingkaran terdekatnya.",
        "habits": ["Selalu datang tepat waktu atau 15 menit lebih awal", "Cek saldo tabungan dan target keuangan secara rutin", "Lebih memilih hasil nyata ketimbang janji manis", "Bekerja di saat orang lain sedang bersantai"],
        "animal_soulmate": {"name": "🦅 Burung Rajawali / German Shepherd", "description": "Tangguh, pekerja keras, berwibawa, dan berorientasi pada pencapaian tinggi di puncak."},
        "cosmic_pantry": {"taste_profile": "🥩 Klasik, Padat Gizi & Authentic", "favorite_food": "Nasi Padang Rendang, Black Tea & Roast Beef", "food_habit": "Menyukai makanan porsi mantap yang mengenyangkan untuk menyuplai energi kerjanya."},
        "astro_decor": {"style": "💼 Executive Classic & Architectural Leather", "key_elements": "Kursi kerja ergonomis kulit, furnitur kayu jati/mahoni, jam dinding klasik, & penghargaan karir", "vibe": "Berwibawa, matang, dan sangat profesional"},
        "fun_fact": "Capricorn kalau sudah liburan pun masih sempet-sempetnya ngecek email kerjaan."
    },
    "aquarius": {
        "physical_traits": ["Tatapan mata unik & melamun (visioner)", "Gaya penampilan eksentrik & beda dari yang lain", "Gestur santai namun unik", "Sering memakai aksesori unik"],
        "personality": "Aquarius adalah pribadi yang mandiri, visioner, dan berpikiran terbuka. Mereka menyukai kebebasan ide, peduli pada isu-isu sosial, dan selalu berpikir beberapa langkah ke depan.",
        "habits": ["Suka memakai kombinasi pakaian yang tidak terpikirkan orang lain", "Mempunyai hobi unik yang jarang disukai orang awam", "Tiba-tiba menghilang beberapa hari dari sosmed untuk menyendiri", "Suka debat mengenai topik-topik unik"],
        "animal_soulmate": {"name": "🐬 Lumba-lumba / Burung Hantu Putih", "description": "Visioner, cerdas di atas rata-rata, independen, dan menyukai kebebasan dalam berpikir."},
        "cosmic_pantry": {"taste_profile": "🧪 Fusion, Unik & Trendy", "favorite_food": "Molecular Gastronomy, Cold Brew & Kombucha", "food_habit": "Suka eksperimen mencampur bahan makanan yang jarang dipadukan orang lain."},
        "astro_decor": {"style": "🚀 Futuristic Cyberpunk & Smart Home", "key_elements": "Lampu LED RGB smart-home, setup PC futuristik, karya seni abstrak, & gadget unik", "vibe": "Canggih, eksentrik, dan jauh melompati zaman"},
        "fun_fact": "Aquarius sering dianggap aneh hari ini, tapi ide mereka baru terbukti kebenarannya 5 tahun kemudian."
    },
    "pisces": {
        "physical_traits": ["Mata besar yang teduh & ekspresif", "Raut wajah lembut & penuh empati", "Gerakan tubuh halus & mengalir", "Gaya pakaian bernuansa bohemian/soft"],
        "personality": "Pisces adalah pribadi yang sangat intuitif, imajinatif, dan penyayang. Mereka memiliki kedalaman emosi dan jiwa seni yang tinggi, serta mudah tersentuh oleh kebaikan.",
        "habits": ["Suka mendengarkan musik sambil membayangkan skenario fiksi", "Sering membantu orang lain meskipun diri sendiri sedang repot", "Gampang terharu saat menonton film atau mendengar cerita sedih", "Suka mengoleksi barang bernilai seni"],
        "animal_soulmate": {"name": "🐟 Ikan Cupang Hias / Kucing Ragdoll", "description": "Sangat indah, penuh empati emosional, lembut, dan mengalir mengikuti keindahan seni."},
        "cosmic_pantry": {"taste_profile": "🍦 Lembut, Manis & Dreamy", "favorite_food": "Gelato, Boba Milk Tea & Seafood Soup", "food_habit": "Menyukai makanan manis bertekstur lembut. Suka makan sambil dengerin musik atau nonton drakor."},
        "astro_decor": {"style": "🌊 Mystic Ocean & Dreamy Aesthetic", "key_elements": "Akuarium/proyektor bintang malam, kain renda melayang, lampu garam Himalaya, & aromaterapi lavender", "vibe": "Mistik, menenangkan batin, dan penuh imajinasi"},
        "fun_fact": "Pisces bisa bikin skenario cerita film lengkap di kepalanya cuma gara-gara liat hujan di kaca jendela."
    }
}

# COSMIC ENGINE
def get_planet_object(planet_name):
    planets = {
        "sun": ephem.Sun(), "moon": ephem.Moon(),
        "mercury": ephem.Mercury(), "venus": ephem.Venus(),
        "mars": ephem.Mars(), "jupiter": ephem.Jupiter(),
        "saturn": ephem.Saturn()
    }
    return planets.get(planet_name)

def get_moon_phase_label(illumination_pct):
    if illumination_pct < 5:
        return ("Bulan Baru", "🌑")
    elif illumination_pct < 35:
        return ("Bulan Sabit Awal", "🌒")
    elif illumination_pct < 65:
        return ("Bulan Separuh", "🌓")
    elif illumination_pct < 90:
        return ("Bulan Cembung", "🌔")
    elif illumination_pct >= 90:
        return ("Bulan Purnama", "🌕")
    else:
        return ("Bulan Cembung Akhir", "🌖")

def get_weather_label(wmo_code, temp_c):
    if wmo_code == 0:
        label = "Langit Cerah"
        emoji = "☀️"
    elif wmo_code in [1, 2]:
        label = "Sebagian Berawan"
        emoji = "⛅"
    elif wmo_code == 3:
        label = "Mendung"
        emoji = "☁️"
    elif wmo_code in [51, 53, 55]:
        label = "Gerimis"
        emoji = "🌦️"
    elif wmo_code in [61, 63, 65]:
        label = "Hujan"
        emoji = "🌧️"
    elif wmo_code in [80, 81, 82]:
        label = "Hujan Deras"
        emoji = "⛈️"
    elif wmo_code in [95, 96, 99]:
        label = "Badai Petir"
        emoji = "🌩️"
    else:
        label = "Berawan"
        emoji = "🌤️"
    return f"{emoji} {label}, {temp_c:.0f}°C"

def get_cosmic_context():
    now = ephem.now()
    today_str = datetime.date.today().strftime("%d %B %Y")

    moon = ephem.Moon(now)
    moon_illumination = moon.phase
    moon_phase_label, moon_emoji = get_moon_phase_label(moon_illumination)

    planet_status = {}
    planet_names = ["mercury", "venus", "mars", "jupiter", "saturn"]
    for pname in planet_names:
        planet = get_planet_object(pname)
        planet.compute(now)
        try:
            prev = get_planet_object(pname)
            prev.compute(ephem.date(now - 1))
            delta_elong = float(planet.hlong) - float(prev.hlong)
            is_retrograde = delta_elong < 0
        except Exception:
            is_retrograde = False
        planet_status[pname] = {
            "is_retrograde": is_retrograde,
            "label": "⬅️ Retrograde" if is_retrograde else "✅ Langsung"
        }

    weather_label = "Tidak tersedia"
    weather_code = -1
    temperature = 0.0
    try:
        resp = requests.get(
            "https://api.open-meteo.com/v1/forecast",
            params={
                "latitude": -6.2,
                "longitude": 106.8,
                "current": "temperature_2m,weather_code",
                "timezone": "Asia/Jakarta"
            },
            timeout=4
        )
        if resp.status_code == 200:
            data = resp.json()
            temperature = data["current"]["temperature_2m"]
            weather_code = data["current"]["weather_code"]
            weather_label = get_weather_label(weather_code, temperature)
    except Exception:
        weather_label = "🌤️ Data cuaca tidak tersedia"

    return {
        "date": today_str,
        "moon_phase": moon_phase_label,
        "moon_emoji": moon_emoji,
        "moon_illumination": round(moon_illumination, 1),
        "planet_status": planet_status,
        "weather": weather_label,
        "weather_code": weather_code,
        "temperature": temperature
    }

def generate_dynamic_ratings(base_ratings, cosmic, ruler_planet, sign_key):
    love = base_ratings["love"]
    career = base_ratings["career"]
    health = base_ratings["health"]

    seed = hashlib.md5(f"{cosmic['date']}_{sign_key}".encode()).hexdigest()
    var_love = (int(seed[0:2], 16) % 15) - 7
    var_career = (int(seed[2:4], 16) % 15) - 7
    var_health = (int(seed[4:6], 16) % 15) - 7

    love += var_love
    career += var_career
    health += var_health

    moon_pct = cosmic["moon_illumination"]
    planet_info = cosmic["planet_status"].get(ruler_planet, {})
    is_retrograde = planet_info.get("is_retrograde", False)

    if moon_pct >= 90:
        love += 5
    if is_retrograde:
        career -= 6

    return {
        "love": min(99, max(40, love)),
        "career": min(99, max(40, career)),
        "health": min(99, max(40, health))
    }

