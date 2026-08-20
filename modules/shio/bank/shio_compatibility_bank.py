# ============================================================
# 🤝 SHIO COMPATIBILITY BANK — Bank Narasi Kecocokan Spesifik
# ============================================================
# STATUS: 📝 SKELETON — Siap diisi konten
#
# FUNGSI: Menggantikan desc_asmara dan desc_bisnis generik di
#         calculate_compatibility() dengan narasi unik per pasangan.
#
# TARGET: 78 pasangan (66 kombinasi unik + 12 pasangan sama)
#         Gunakan tuple (shio1, shio2) sebagai key, di mana
#         shio1 < shio2 secara alfabet untuk konsistensi.
#
# CATATAN: Untuk pasangan yang belum ada di bank, fungsi
#          calculate_compatibility() tetap bisa fallback ke
#          template generik yang sudah ada.
# ============================================================

SHIO_COMPATIBILITY_BANK = {
    # === CONTOH FORMAT ===
    ("tikus", "kerbau"): {
        "relationship": "Liu He (Jodoh Kosmik Sejati)",
        "asmara": "Tikus dan Kerbau adalah pasangan klasik yang saling melengkapi. Tikus yang cerdik dan lincah memberikan ide-ide brilian, sementara Kerbau yang tenang dan kokoh menjadi pondasi yang tak tergoyahkan. Di rumah tangga, Tikus jadi otaknya, Kerbau jadi tulang punggungnya.",
        "bisnis": "Duet bisnis yang sangat solid! Tikus hebat mencari peluang dan negosiasi, Kerbau ahli mengeksekusi dan menjaga kualitas. Cocok untuk membangun usaha jangka panjang.",
        "drama": "Kerbau kadang frustrasi dengan sifat Tikus yang gampang bosan dan sering pindah haluan. Tikus capek karena Kerbau dianggap terlalu lambat dan kuno.",
        "tips": "Tikus, belajar untuk sabar dan konsisten. Kerbau, belajar untuk lebih terbuka dengan ide-ide baru."
    },
    ("kuda", "tikus"): {
        "relationship": "Ciong (Bentrokan Ekstrem)",
        "asmara": "Hubungan yang penuh api dan drama! Tikus yang perhitungan bertemu Kuda yang impulsif — setiap keputusan jadi bahan debat panas. Tapi kalau bisa saling toleransi, justru saling melengkapi secara tak terduga.",
        "bisnis": "Jangan. Serius, jangan — kecuali kalian siap rapat 3 jam hanya untuk memutuskan warna logo.",
        "drama": "Kuda: 'Ayo langsung aja!' Tikus: 'Tunggu, aku masih bikin spreadsheet analisis risiko.' Keduanya: *drama ensues*",
        "tips": "Butuh mediator (Shio Monyet atau Naga) untuk menjembatani perbedaan gaya kalian."
    },

    # TODO: Isi 76 pasangan lainnya
    # Gunakan format key: (shio_lebih_kecil_alfabet, shio_lebih_besar_alfabet)
    # Contoh key: ("anjing", "babi"), ("ayam", "kerbau"), dll.
    #
    # DAFTAR RELASI PENTING:
    # Liu He (Jodoh Kosmik):
    #   Tikus-Kerbau, Macan-Babi, Kelinci-Anjing, Naga-Ayam, Ular-Monyet, Kuda-Kambing
    #
    # San He (Tiga Harmoni):
    #   Tikus-Naga-Monyet, Kerbau-Ular-Ayam, Macan-Kuda-Anjing, Kelinci-Kambing-Babi
    #
    # Ciong (Bentrokan):
    #   Tikus-Kuda, Kerbau-Kambing, Macan-Monyet, Kelinci-Ayam, Naga-Anjing, Ular-Babi
}
