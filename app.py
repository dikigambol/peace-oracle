from flask import Flask, render_template, jsonify, request
import ephem
import requests
import datetime
import math
import hashlib

# Import Data Bank Ramalan & Musik (100 Afirmasi & 100 Lagu per Zodiak)
from horoscope_bank import get_daily_horoscope, get_daily_youtube_track
from roasting_bank import determine_zodiac, get_roast, get_relationship_roast

app = Flask(__name__)

# ============================================================
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

# ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/kecocokan')
def compatibility_page():
    return render_template('kecocokan.html')

@app.route('/general')
@app.route('/karakter')
def general_page():
    return render_template('general.html')

@app.route('/roasting')
def roasting_page():
    return render_template('roasting.html')

@app.route('/api/roast', methods=['GET', 'POST'])
def api_roast():
    sign_key = None
    if request.method == 'POST':
        data = request.get_json() or {}
        birthdate = data.get('birthdate')
        sign = data.get('sign')
        if birthdate:
            try:
                parts = birthdate.split('-')
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
        elif sign:
            sign_key = sign.lower()
    else:
        birthdate = request.args.get('birthdate')
        sign = request.args.get('sign')
        day = request.args.get('day')
        month = request.args.get('month')
        if day and month:
            sign_key = determine_zodiac(day, month)
        elif birthdate:
            try:
                parts = birthdate.split('-')
                if len(parts) == 3:
                    day = int(parts[2])
                    month = int(parts[1])
                    sign_key = determine_zodiac(day, month)
            except Exception:
                pass
        elif sign:
            sign_key = sign.lower()

    if not sign_key or sign_key not in ZODIAC_DATA:
        sign_key = 'aries'

    z = ZODIAC_DATA[sign_key]
    roast_info = get_roast(sign_key)

    sign_b = None
    if request.method == 'POST':
        data = request.get_json() or {}
        sign_b = data.get('sign_b')
    else:
        sign_b = request.args.get('sign_b')

    relationship_roast = None
    if sign_b and sign_b.lower() in ZODIAC_DATA:
        relationship_roast = get_relationship_roast(sign_key, sign_b.lower())

    return jsonify({
        "sign_key": sign_key,
        "name": z["name"],
        "element": z["element"],
        "date_range": z["date_range"],
        "roast": roast_info,
        "relationship_roast": relationship_roast
    })

@app.route('/api/zodiac/<sign>')
def get_zodiac(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z = ZODIAC_DATA[sign_key]

    cosmic = get_cosmic_context()
    dynamic_ratings = generate_dynamic_ratings(
        z["base_ratings"], cosmic, z["ruler_planet"], sign_key
    )
    genz_readings = get_daily_horoscope(sign_key, cosmic)
    youtube_track = get_daily_youtube_track(sign_key, cosmic)

    ruler_planet = z["ruler_planet"]
    planet_info = cosmic["planet_status"].get(ruler_planet, {})
    ruler_status = planet_info.get("label", "✅ Langsung")

    return jsonify({
        "name": z["name"],
        "date_range": z["date_range"],
        "element": z["element"],
        "ruler": z["ruler"],
        "strengths": z["strengths"],
        "weaknesses": z["weaknesses"],
        "lucky_number": z["lucky_number"],
        "lucky_color": z["lucky_color"],
        "compatible_signs": z["compatible_signs"],
        "summary": genz_readings["summary"],
        "genz_readings": genz_readings,
        "youtube_track": youtube_track,
        "ratings": dynamic_ratings,
        "cosmic": {
            "date": cosmic["date"],
            "moon_phase": cosmic["moon_phase"],
            "moon_emoji": cosmic["moon_emoji"],
            "moon_illumination": cosmic["moon_illumination"],
            "ruler_status": ruler_status,
            "ruler_is_retrograde": planet_info.get("is_retrograde", False),
            "weather": cosmic["weather"]
        }
    })

@app.route('/api/general/<sign>')
@app.route('/api/karakter/<sign>')
def get_general_details(sign):
    sign_key = sign.lower()
    if sign_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z = ZODIAC_DATA[sign_key]
    char = GENERAL_CHARACTERISTICS.get(sign_key, GENERAL_CHARACTERISTICS["aries"])

    return jsonify({
        "name": z["name"],
        "date_range": z["date_range"],
        "element": z["element"],
        "ruler": z["ruler"],
        "physical_traits": char["physical_traits"],
        "personality": char["personality"],
        "habits": char["habits"],
        "animal_soulmate": char["animal_soulmate"],
        "cosmic_pantry": char["cosmic_pantry"],
        "astro_decor": char["astro_decor"],
        "fun_fact": char["fun_fact"]
    })

@app.route('/api/compatibility/<sign_one>/<sign_two>')
def get_compatibility(sign_one, sign_two):
    s1_key = sign_one.lower()
    s2_key = sign_two.lower()

    if s1_key not in ZODIAC_DATA or s2_key not in ZODIAC_DATA:
        return jsonify({"error": "Zodiac sign not found"}), 404

    z1 = ZODIAC_DATA[s1_key]
    z2 = ZODIAC_DATA[s2_key]

    elem_one = z1["element"]
    elem_two = z2["element"]
    base_metrics = ELEMENT_COMPATIBILITY[elem_one][elem_two].copy()

    if s1_key == s2_key:
        base_metrics.update({"score": 80, "love": 82, "comm": 78, "trust": 85, "future": 75})
    elif (
        (s1_key == 'scorpio' and s2_key == 'cancer') or (s1_key == 'cancer' and s2_key == 'scorpio') or
        (s1_key == 'leo' and s2_key == 'aries') or (s1_key == 'aries' and s2_key == 'leo') or
        (s1_key == 'gemini' and s2_key == 'libra') or (s1_key == 'libra' and s2_key == 'gemini')
    ):
        base_metrics.update({"score": 98, "love": 99, "comm": 97, "trust": 98, "future": 98})

    base_score = base_metrics["score"]

    # 1. MODE PASANGAN (Asmara / Romantis)
    love_score = min(99, max(45, int(base_score * 1.02)))
    if love_score >= 85:
        love_status = "Sangat Harmonis (Kosmik Selaras) ✨"
        love_summary = f"Kombinasi asmara antara {z1['name']} ({elem_one}) dan {z2['name']} ({elem_two}) membentuk perpaduan cinta yang luar biasa kuat dan penuh daya tarik emosional."
        love_strengths = ["Chemistry cinta meletup-letup dan romantis", "Saling memahami perasaan tanpa banyak bicara", "Dukungan emosional yang hangat dan menenangkan"]
        love_challenges = ["Kecenderungan menyembunyikan masalah emosional kecil", "Menjaga ritme romansa agar tidak menjadi rutinitas"]
    elif love_score >= 70:
        love_status = "Cinta Kuat & Komitmen Tinggi 💖"
        love_summary = f"Hubungan {z1['name']} dan {z2['name']} memiliki fondasi kesetiaan yang stabil. Perbedaan gaya mencintai justru saling melengkapi kelemahan masing-masing."
        love_strengths = ["Saling melengkapi bahasa cinta (love language)", "Kesetiaan tinggi dan komitmen jangka panjang", "Rasa aman saat bersama"]
        love_challenges = ["Perbedaan cara merespon konflik emosional", "Butuh waktu untuk menyelaraskan ekspektasi"]
    else:
        love_status = "Tantangan Kompromi Asmara ⚡"
        love_summary = f"Perpaduan elemen {elem_one} dan {elem_two} membutuhkan kesabaran ekstra dalam asmara. Butuh komunikasi terbuka untuk menyelaraskan keinginan ego."
        love_strengths = ["Memberikan pelajaran kedewasaan emosional", "Daya tarik perbedaan karakter yang kuat", "Menumbuhkan rasa toleransi tinggi"]
        love_challenges = ["Kecerobohan emosi saat dipicu rasa cemburu", "Perbedaan ritme mengekspresikan kasih sayang"]

    # 2. MODE SAHABAT (Pertemanan / Bestie)
    friend_score = min(99, max(40, int(base_score * 0.98 + (10 if elem_one in ['Udara', 'Api'] and elem_two in ['Udara', 'Api'] else 0))))
    if friend_score >= 85:
        friend_status = "Bestie Sejati (Frekuensi Selaras) 🤝"
        friend_summary = f"Sebagai sahabat, {z1['name']} dan {z2['name']} adalah kombinasi duo paling seru! Keduanya bisa ngobrolin apa saja dari spill the tea hingga topik filsafat tanpa takut di-judge."
        friend_strengths = ["Frekuensi humor dan nyambung obrolannya 100%", "Tempat curhat aman tanpa rasa canggung", "Selalu siap saling bantu di masa sulit"]
        friend_challenges = ["Sering lupa waktu kalau udah ketemu dan ngobrol", "Keduanya sama-sama suka ceplas-ceplos"]
    elif friend_score >= 70:
        friend_status = "Teman Asyik & Suportif 🥳"
        friend_summary = f"Pertemanan antara {z1['name']} dan {z2['name']} sangat menyenangkan untuk diajak nongkrong, berpetualang, atau nyobain hal-hal baru bersama."
        friend_strengths = ["Asyik diajak jalan-jalan atau nyobain kuliner baru", "Saling mendukung impian satu sama lain", "Bisa menjaga rahasia dengan baik"]
        friend_challenges = ["Kadang butuh waktu sendiri jika mood sedang tidak bagus", "Jarang menyampaikan rasa tidak suka secara langsung"]
    else:
        friend_status = "Teman Kasual (Perlu Saling Menghormati) ☕"
        friend_summary = f"Hubungan pertemanan ini paling pas berada di tingkat kasual. Menghormati batasan dan ruang pribadi adalah kunci agar hubungan pertemanan tetap awet."
        friend_strengths = ["Membawa sudut pandang baru yang tidak terpikirkan", "Menguji batas kepekaan sosial", "Menyenangkan saat mengerjakan proyek hobi tertentu"]
        friend_challenges = ["Gaya bercanda kadang tidak sengaja menyinggung perasaan", "Perbedaan selera aktivitas waktu luang"]

    # 3. MODE REKAN KERJA (Karir / Profesional)
    work_score = min(99, max(40, int(base_score * 0.95 + (12 if elem_one in ['Tanah', 'Api'] and elem_two in ['Tanah', 'Api'] else 5))))
    if work_score >= 85:
        work_status = "Dream Team Profesional (Sinergi Tinggi) 💼"
        work_summary = f"Di tempat kerja, {z1['name']} dan {z2['name']} adalah kombinasi Dream Team! Satu pihak mahir memikirkan ide & strategi, sementara pihak lainnya tangguh dalam eksekusi target."
        work_strengths = ["Sinergi eksekusi proyek sangat cepat dan efisien", "Pembagian tugas yang sangat alami dan saling melengkapi", "Fokus tinggi pada pencapaian target kerja"]
        work_challenges = ["Keduanya bisa terlalu kompetitif jika tidak menetapkan tujuan bersama", "Cenderung lupa istirahat karena keasyikan kerja"]
    elif work_score >= 70:
        work_status = "Rekan Kerja Efisien & Produktif 📈"
        work_summary = f"Kerja sama profesional antara {z1['name']} dan {z2['name']} berjalan lancar dan terorganisir. Mereka dapat mencapai deadline dengan hasil memuaskan."
        work_strengths = ["Komunikasi profesional yang jelas dan terarah", "Saling menghormati wewenang dan job description", "Dapat diandalkan dalam pemecahan masalah teknis"]
        work_challenges = ["Perlu menyelaraskan ritme kerja saat tekanan deadline tinggi", "Kadang terlalu kaku dalam mengambil keputusan kompromi"]
    else:
        work_status = "Perlu Pembagian Tugas Jelas 🛠️"
        work_summary = f"Dalam dunia kerja, {z1['name']} dan {z2['name']} membutuhkan struktur dan SOP yang sangat transparan agar tidak terjadi tumpang tindih wewenang."
        work_strengths = ["Saling menguji kelemahan konsep bisnis sebelum eksekusi", "Mendorong kehati-hatian dalam mengambil risiko", "Membuat analisis kerja menjadi lebih tajam"]
        work_challenges = ["Potensi benturan ego saat mempertahankan ide masing-masing", "Perbedaan gaya manajemen waktu"]

    modes_data = {
        "romance": {
            "label": "Pasangan (Asmara)",
            "icon": "fa-heart",
            "score": love_score,
            "status": love_status,
            "summary": love_summary,
            "strengths": love_strengths,
            "challenges": love_challenges,
            "metrics": {"love": base_metrics["love"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": base_metrics["future"]}
        },
        "friendship": {
            "label": "Sahabat (Bestie)",
            "icon": "fa-user-group",
            "score": friend_score,
            "status": friend_status,
            "summary": friend_summary,
            "strengths": friend_strengths,
            "challenges": friend_challenges,
            "metrics": {"love": base_metrics["comm"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": int((friend_score + base_metrics["comm"]) / 2)}
        },
        "work": {
            "label": "Rekan Kerja",
            "icon": "fa-briefcase",
            "score": work_score,
            "status": work_status,
            "summary": work_summary,
            "strengths": work_strengths,
            "challenges": work_challenges,
            "metrics": {"love": base_metrics["comm"], "comm": base_metrics["comm"], "trust": base_metrics["trust"], "future": int((work_score + base_metrics["trust"]) / 2)}
        }
    }

    return jsonify({
        "sign_one": z1["name"], "sign_two": z2["name"],
        "element_one": elem_one, "element_two": elem_two,
        "modes": modes_data
    })

if __name__ == '__main__':
    app.run(debug=True)
