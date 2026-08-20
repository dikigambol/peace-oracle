# ============================================================
# 🐉 SHIO YEARLY BANK — Bank Ramalan Tahunan Spesifik
# ============================================================
# STATUS: 📝 SKELETON — Siap diisi konten
#
# FUNGSI: Menggantikan template generik di calculate_yearly_fortune()
#         dengan narasi spesifik per kombinasi (user_shio, year_shio).
#
# TARGET: 144 kombinasi (12 user shio × 12 year shio)
#         Untuk pasangan yang belum ada, fungsi fallback ke template.
#
# KEY FORMAT: (user_shio_key, year_shio_key)
# ============================================================

SHIO_YEARLY_BANK = {
    # === CONTOH FORMAT ===
    ("tikus", "ular"): {
        "karir": "Tahun Ular membawa energi misterius bagi Tikus. Ada peluang tersembunyi di networking — seseorang dari masa lalu akan menawarkan kolaborasi mengejutkan.",
        "keuangan": "Investasi jangka panjang lebih menguntungkan daripada trading cepat. Tikus perlu meniru kebijaksanaan Ular: sabar menunggu momen terbaik.",
        "asmara": "Hubungan asmara penuh intrik! Ular mengajarkan Tikus untuk lebih peka membaca bahasa tubuh pasangan.",
        "kesehatan": "Waspadai kelelahan mental. Energi Ular yang intens bisa membuat pikiran Tikus terlalu aktif di malam hari.",
        "saran_utama": "Tahun ini tentang kualitas, bukan kuantitas. Pilih sedikit tapi berkualitas."
    },

    # TODO: Isi 143 kombinasi lainnya
    # Prioritas tinggi — isi dulu untuk relasi penting:
    #
    # CIONG (Bentrokan — paling dicari orang):
    # ("tikus", "kuda"), ("kerbau", "kambing"), ("macan", "monyet"),
    # ("kelinci", "ayam"), ("naga", "anjing"), ("ular", "babi")
    #
    # TAI SUI (Tahun kelahiran sendiri):
    # ("tikus", "tikus"), ("kerbau", "kerbau"), ... dst
    #
    # LIU HE (Jodoh Kosmik):
    # ("tikus", "kerbau"), ("macan", "babi"), ("kelinci", "anjing"),
    # ("naga", "ayam"), ("ular", "monyet"), ("kuda", "kambing")
}
