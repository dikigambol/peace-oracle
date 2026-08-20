# ============================================================
# 🏦 SHIO BANK DATA — Central Hub
# ============================================================
# Folder ini berisi semua bank data konten untuk modul Shio.
# Setiap file berisi data statis yang kaya konten tulisan manual.
#
# STRUKTUR:
# bank/
# ├── __init__.py                    ← File ini (central export)
# ├── shio_daily_bank.py             ✅ SELESAI — Pesan harian per status
# ├── shio_fortune_bank.py           📝 SKELETON — Ramalan per kategori
# ├── shio_roasting_bank.py          📝 SKELETON — Roasting pedas per Shio
# ├── shio_compatibility_bank.py     📝 SKELETON — Narasi kecocokan pasangan
# ├── shio_profile_bank.py           📝 SKELETON — Profil mendalam per Shio
# ├── shio_yearly_bank.py            📝 SKELETON — Ramalan tahunan spesifik
# ├── shio_fortune_cookie_bank.py    📝 SKELETON — Pesan lucu fortune cookie
# └── shio_guardian_bank.py          📝 SKELETON — Data penjaga spiritual
#
# CARA PAKAI:
# from .bank import DAILY_CIONG_MESSAGES, SHIO_ROASTING_BANK, ...
# ============================================================

# === DAILY BANK (✅ SELESAI) ===
from .shio_daily_bank import (
    DAILY_CIONG_MESSAGES,
    DAILY_SAN_HE_MESSAGES,
    DAILY_LIU_HE_MESSAGES,
    DAILY_WARNING_MESSAGES,
    DAILY_TAI_SUI_MESSAGES,
    DAILY_NEUTRAL_MESSAGES,
    SHIO_DAILY_TIPS
)

# === FORTUNE BANK (📝 UPCOMING) ===
from .shio_fortune_bank import SHIO_FORTUNE_BANK

# === ROASTING BANK (📝 UPCOMING) ===
from .shio_roasting_bank import SHIO_ROASTING_BANK

# === COMPATIBILITY BANK (📝 UPCOMING) ===
from .shio_compatibility_bank import SHIO_COMPATIBILITY_BANK

# === PROFILE BANK (📝 UPCOMING) ===
from .shio_profile_bank import SHIO_PROFILE_BANK

# === YEARLY BANK (📝 UPCOMING) ===
from .shio_yearly_bank import SHIO_YEARLY_BANK

# === FORTUNE COOKIE BANK (📝 UPCOMING) ===
from .shio_fortune_cookie_bank import SHIO_FORTUNE_COOKIE_BANK

# === PENJAGA SPIRITUAL BANK (📝 UPCOMING) ===
from .shio_guardian_bank import SHIO_GUARDIAN_BANK
