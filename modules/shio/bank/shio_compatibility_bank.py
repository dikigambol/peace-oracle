# ============================================================
# 🤝 SHIO COMPATIBILITY BANK — Bank Narasi Kecocokan Spesifik
# ============================================================
# 78 pasangan unik dengan narasi spesifik per kombinasi.
# Key: tuple (shio1, shio2) sorted alphabetically.
# 
# RELASI PENTING (Chinese Zodiac Traditional):
#
# Liu He (Jodoh Kosmik / Secret Friends):
#   Tikus-Kerbau, Macan-Babi, Kelinci-Anjing, Naga-Ayam, Ular-Monyet, Kuda-Kambing
#
# San He (Tiga Harmoni / Trine):
#   Tikus-Naga-Monyet (Air), Kerbau-Ular-Ayam (Logam),
#   Macan-Kuda-Anjing (Api), Kelinci-Kambing-Babi (Kayu)
#
# Liu Chong / Ciong (Bentrokan / Clash):
#   Tikus-Kuda, Kerbau-Kambing, Macan-Monyet, Kelinci-Ayam, Naga-Anjing, Ular-Babi
#
# Liu Hai / Harm:
#   Tikus-Kambing, Kerbau-Kuda, Macan-Ular, Kelinci-Naga, Monyet-Babi, Ayam-Anjing
# ============================================================

SHIO_COMPATIBILITY_BANK = {
    ("anjing", "anjing"): {
        "relationship": "Kembar Kosmik",
        "score": 73,
        "asmara": "Sama-sama Anjing bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("anjing", "ayam"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 41,
        "asmara": "Ada aja halangannya, Anjing dan Ayam butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("anjing", "babi"): {
        "relationship": "Netral",
        "score": 61,
        "asmara": "Anjing dan Babi? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Kerja bareng kalian asyik, satu mikir strategi satu lagi eksekusi.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("anjing", "kambing"): {
        "relationship": "Netral",
        "score": 55,
        "asmara": "Anjing dan Kambing? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("anjing", "kelinci"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 96,
        "asmara": "Beneran jodoh dari surga! Anjing dan Kelinci itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("anjing", "kerbau"): {
        "relationship": "Netral",
        "score": 58,
        "asmara": "Anjing dan Kerbau? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("anjing", "kuda"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 87,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Anjing dan Kuda.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("anjing", "macan"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 90,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Anjing dan Macan.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("anjing", "monyet"): {
        "relationship": "Netral",
        "score": 55,
        "asmara": "Anjing dan Monyet? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("anjing", "naga"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 28,
        "asmara": "Waduh, energi kalian gampang bentrok! Anjing sama Naga ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("anjing", "tikus"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Anjing dan Tikus? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("anjing", "ular"): {
        "relationship": "Netral",
        "score": 63,
        "asmara": "Anjing dan Ular? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("ayam", "ayam"): {
        "relationship": "Kembar Kosmik",
        "score": 72,
        "asmara": "Sama-sama Ayam bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("ayam", "babi"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Ayam dan Babi? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("ayam", "kambing"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Ayam dan Kambing? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("ayam", "kelinci"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 30,
        "asmara": "Waduh, energi kalian gampang bentrok! Ayam sama Kelinci ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("ayam", "kerbau"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 88,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Ayam dan Kerbau.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("ayam", "kuda"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Ayam dan Kuda? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Kerja bareng kalian asyik, satu mikir strategi satu lagi eksekusi.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("ayam", "macan"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Ayam dan Macan? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("ayam", "monyet"): {
        "relationship": "Netral",
        "score": 60,
        "asmara": "Ayam dan Monyet? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("ayam", "naga"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 95,
        "asmara": "Beneran jodoh dari surga! Ayam dan Naga itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("ayam", "tikus"): {
        "relationship": "Netral",
        "score": 62,
        "asmara": "Ayam dan Tikus? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Kerja bareng kalian asyik, satu mikir strategi satu lagi eksekusi.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("ayam", "ular"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 86,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Ayam dan Ular.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("babi", "babi"): {
        "relationship": "Kembar Kosmik",
        "score": 74,
        "asmara": "Sama-sama Babi bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("babi", "kambing"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 89,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Babi dan Kambing.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("babi", "kelinci"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 89,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Babi dan Kelinci.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("babi", "kerbau"): {
        "relationship": "Netral",
        "score": 58,
        "asmara": "Babi dan Kerbau? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Kasih space satu sama lain biar gak gampang bosen."
    },
    ("babi", "kuda"): {
        "relationship": "Netral",
        "score": 56,
        "asmara": "Babi dan Kuda? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Kasih space satu sama lain biar gak gampang bosen."
    },
    ("babi", "macan"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 97,
        "asmara": "Beneran jodoh dari surga! Babi dan Macan itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("babi", "monyet"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 41,
        "asmara": "Ada aja halangannya, Babi dan Monyet butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("babi", "naga"): {
        "relationship": "Netral",
        "score": 60,
        "asmara": "Babi dan Naga? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("babi", "tikus"): {
        "relationship": "Netral",
        "score": 60,
        "asmara": "Babi dan Tikus? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("babi", "ular"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 23,
        "asmara": "Waduh, energi kalian gampang bentrok! Babi sama Ular ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("kambing", "kambing"): {
        "relationship": "Kembar Kosmik",
        "score": 75,
        "asmara": "Sama-sama Kambing bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("kambing", "kelinci"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 87,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Kambing dan Kelinci.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("kambing", "kerbau"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 33,
        "asmara": "Waduh, energi kalian gampang bentrok! Kambing sama Kerbau ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("kambing", "kuda"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 96,
        "asmara": "Beneran jodoh dari surga! Kambing dan Kuda itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("kambing", "macan"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Kambing dan Macan? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Kerja bareng kalian asyik, satu mikir strategi satu lagi eksekusi.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("kambing", "monyet"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Kambing dan Monyet? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("kambing", "naga"): {
        "relationship": "Netral",
        "score": 56,
        "asmara": "Kambing dan Naga? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("kambing", "tikus"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 47,
        "asmara": "Ada aja halangannya, Kambing dan Tikus butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("kambing", "ular"): {
        "relationship": "Netral",
        "score": 59,
        "asmara": "Kambing dan Ular? Boleh banget dicoba, siapa tau malah jadi power couple tak terduga.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("kelinci", "kelinci"): {
        "relationship": "Kembar Kosmik",
        "score": 74,
        "asmara": "Sama-sama Kelinci bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("kelinci", "kerbau"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Kelinci dan Kerbau? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Turunin ego dikit, kalian berdua sama-sama berharga kok."
    },
    ("kelinci", "kuda"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Kelinci dan Kuda? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("kelinci", "macan"): {
        "relationship": "Netral",
        "score": 62,
        "asmara": "Kelinci dan Macan? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("kelinci", "monyet"): {
        "relationship": "Netral",
        "score": 55,
        "asmara": "Kelinci dan Monyet? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("kelinci", "naga"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 43,
        "asmara": "Ada aja halangannya, Kelinci dan Naga butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("kelinci", "tikus"): {
        "relationship": "Netral",
        "score": 65,
        "asmara": "Kelinci dan Tikus? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Beda gaya kerja dikit wajar, yang penting target kecapai.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("kelinci", "ular"): {
        "relationship": "Netral",
        "score": 62,
        "asmara": "Kelinci dan Ular? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("kerbau", "kerbau"): {
        "relationship": "Kembar Kosmik",
        "score": 70,
        "asmara": "Sama-sama Kerbau bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("kerbau", "kuda"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 42,
        "asmara": "Ada aja halangannya, Kerbau dan Kuda butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("kerbau", "macan"): {
        "relationship": "Netral",
        "score": 56,
        "asmara": "Kerbau dan Macan? Ada chemistry yang menarik di antara kalian, lumayan smooth.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("kerbau", "monyet"): {
        "relationship": "Netral",
        "score": 65,
        "asmara": "Kerbau dan Monyet? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Satu mau healing ke gunung, satu mau ke mall, akhirnya malah sama-sama bad mood di rumah.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("kerbau", "naga"): {
        "relationship": "Netral",
        "score": 55,
        "asmara": "Kerbau dan Naga? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Turunin ego dikit, kalian berdua sama-sama berharga kok."
    },
    ("kerbau", "tikus"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 99,
        "asmara": "Beneran jodoh dari surga! Kerbau dan Tikus itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("kerbau", "ular"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 90,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Kerbau dan Ular.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("kuda", "kuda"): {
        "relationship": "Kembar Kosmik",
        "score": 74,
        "asmara": "Sama-sama Kuda bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("kuda", "macan"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 87,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Kuda dan Macan.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("kuda", "monyet"): {
        "relationship": "Netral",
        "score": 57,
        "asmara": "Kuda dan Monyet? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Debat soal film yang mau ditonton berujung perang dingin di chat.",
        "tips": "Turunin ego dikit, kalian berdua sama-sama berharga kok."
    },
    ("kuda", "naga"): {
        "relationship": "Netral",
        "score": 64,
        "asmara": "Kuda dan Naga? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Kerja bareng kalian asyik, satu mikir strategi satu lagi eksekusi.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("kuda", "tikus"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 23,
        "asmara": "Waduh, energi kalian gampang bentrok! Kuda sama Tikus ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("kuda", "ular"): {
        "relationship": "Netral",
        "score": 62,
        "asmara": "Kuda dan Ular? Bisa dibilang cocok, cuma kadang beda frekuensi sedikit aja.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Kasih space satu sama lain biar gak gampang bosen."
    },
    ("macan", "macan"): {
        "relationship": "Kembar Kosmik",
        "score": 74,
        "asmara": "Sama-sama Macan bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("macan", "monyet"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "score": 23,
        "asmara": "Waduh, energi kalian gampang bentrok! Macan sama Monyet ibarat api ketemu bensin.",
        "bisnis": "Bakal sering debat meeting, siapin kopi ekstra biar gak gampang emosi.",
        "drama": "Satu ngomong A, satu denger Z. Ujung-ujungnya saling block di Instagram semaleman.",
        "tips": "Harus ada yang ngalah! Jangan dua-duanya keras kepala kalau mau langgeng."
    },
    ("macan", "naga"): {
        "relationship": "Netral",
        "score": 56,
        "asmara": "Macan dan Naga? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Masing-masing gengsi minta maaf duluan, endingnya malah sama-sama kangen.",
        "tips": "Banyakin quality time bareng, nonton konser atau jalan-jalan santai."
    },
    ("macan", "tikus"): {
        "relationship": "Netral",
        "score": 59,
        "asmara": "Macan dan Tikus? Kombinasi unik nih, asal gak sama-sama batu pasti aman.",
        "bisnis": "Cuan ngalir lancar kalau udah satu visi misi.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Turunin ego dikit, kalian berdua sama-sama berharga kok."
    },
    ("macan", "ular"): {
        "relationship": "Liu Hai (Saling Menyakiti)",
        "score": 49,
        "asmara": "Ada aja halangannya, Macan dan Ular butuh extra effort buat nyatu.",
        "bisnis": "Sering miskom dan curigaan sendiri, mending bikin job desk yang super jelas.",
        "drama": "Drama saling sindir pakai quotes di IG Story sampe temen-temen ikutan bingung.",
        "tips": "Stop saling nyalahin, coba duduk bareng dan ngomong dari hati ke hati."
    },
    ("monyet", "monyet"): {
        "relationship": "Kembar Kosmik",
        "score": 70,
        "asmara": "Sama-sama Monyet bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("monyet", "naga"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 90,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Monyet dan Naga.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("monyet", "tikus"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 90,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Monyet dan Tikus.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("monyet", "ular"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "score": 99,
        "asmara": "Beneran jodoh dari surga! Monyet dan Ular itu match banget.",
        "bisnis": "Chemistry kalian di dunia kerja itu dewa banget, auto cuan kalau bareng.",
        "drama": "Gak ada drama berat, paling ribut rebutan siapa yang traktir boba duluan.",
        "tips": "Pertahankan vibes positif kalian, you guys are perfect together!"
    },
    ("naga", "naga"): {
        "relationship": "Kembar Kosmik",
        "score": 75,
        "asmara": "Sama-sama Naga bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("naga", "tikus"): {
        "relationship": "San He (Tiga Harmoni)",
        "score": 85,
        "asmara": "Hubungan yang super chill dan saling melengkapi buat Naga dan Tikus.",
        "bisnis": "Kerja bareng kalian itu smooth banget, kayak air ngalir santai tapi pasti nyampe tujuan.",
        "drama": "Kalau ribut paling soal hal sepele kayak mau dengerin playlist siapa pas road trip.",
        "tips": "Tetep solid dan jangan biarin omongan orang ngerusak mood kalian."
    },
    ("naga", "ular"): {
        "relationship": "Netral",
        "score": 60,
        "asmara": "Naga dan Ular? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Jangan rebutan spotlight ya pas meeting, bagi-bagi tugas aja.",
        "drama": "Ribut kecil dari salah paham emoji doang, tapi panjang urusannya wkwk.",
        "tips": "Kurangin overthinking dan saling jujur aja tentang perasaan kalian."
    },
    ("tikus", "tikus"): {
        "relationship": "Kembar Kosmik",
        "score": 74,
        "asmara": "Sama-sama Tikus bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    },
    ("tikus", "ular"): {
        "relationship": "Netral",
        "score": 60,
        "asmara": "Tikus dan Ular? Kalian berdua bisa nyambung kok, asal mau saling dengerin.",
        "bisnis": "Kalian bisa jadi tim yang solid asal komunikasi dijaga.",
        "drama": "Pas ribut gara-gara milih tempat makan, bisa sampai diem-dieman tiga hari.",
        "tips": "Jangan gengsi buat minta maaf duluan kalau lagi ada masalah."
    },
    ("ular", "ular"): {
        "relationship": "Kembar Kosmik",
        "score": 75,
        "asmara": "Sama-sama Ular bikin kalian paham luar dalam, tapi kadang ngebosenin.",
        "bisnis": "Bisa ngegas bareng kalau visi sama, tapi kalau mandek malah overthinking berdua.",
        "drama": "Karna sifatnya sama plek ketiplek, kalau ngambek ya sama-sama nunggu disapa duluan.",
        "tips": "Cari hobi baru di luar rutinitas biar hubungan gak terasa hambar."
    }
}
