<div align="center">
  <img src="https://img.icons8.com/?size=100&id=102558&format=png&color=FFFFFF" alt="Peace Oracle Logo" width="80" height="80">
  <br>
  <h1>Peace Oracle</h1>
  <p><b>✨ Temukan Ketenangan Lewat Penyelarasan Kosmik, Oriental, Primbon Nusantara, & Tarot ✨</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Frontend-Vanilla_JS_&_CSS-F7DF1E?style=flat-square&labelColor=30363D&logo=javascript&logoColor=F7DF1E" alt="Frontend: Vanilla JS & CSS">
    <img src="https://img.shields.io/badge/Backend-Python_3.13+-3776AB?style=flat-square&labelColor=30363D&logo=python&logoColor=FFD43B" alt="Backend: Python 3.13+">
    <img src="https://img.shields.io/badge/Framework-Flask-009688?style=flat-square&labelColor=30363D&logo=flask&logoColor=white" alt="Framework: Flask">
    <img src="https://img.shields.io/badge/AI-OpenRouter-8B5CF6?style=flat-square&labelColor=30363D&logo=openai&logoColor=white" alt="AI: OpenRouter">
    <br>
    <img src="https://img.shields.io/badge/Database-MySQL-4479A1?style=flat-square&labelColor=30363D&logo=mysql&logoColor=white" alt="Database: MySQL">
    <img src="https://img.shields.io/badge/Deployment-Vercel-7B5CFF?style=flat-square&labelColor=30363D&logo=vercel&logoColor=white" alt="Deployment: Vercel">
    <img src="https://img.shields.io/badge/Status-Beta-FF8C42?style=flat-square&labelColor=30363D" alt="Status: Beta">
  </p>
</div>

<br>

**Peace Oracle** adalah aplikasi web ramalan dengan empat mode: Zodiak, Shio, Weton, dan Tarot.

---

## 🌟 Fitur Utama

### 🌌 Landing Page
* **Portal Nebula 3D**, **Mode Switcher** melayang, dan *easter egg* tersembunyi.

### 🌙 Mode Zodiak
* **Ramalan Harian** — ditulis AI, jatuh ke *data bank* bila kuota habis.
* **Karakteristik General** — sifat dan kebiasaan tiap zodiak.
* **Kalkulator Kecocokan** — asmara, sahabat, dan rekan kerja, plus **Quiz Room** berdua dengan ulasan AI.
* **Roasting Zodiak** — personal dan pasangan, bisa di-*reroll*.

### 🐉 Mode Shio
* **Baca Gulungan Takdir (Ming Li)** — Empat Pilar Ba Zi (八字) dari tanggal, jam, dan kota lahir.
* **Almanak Harian (Tong Shu)** — energi hari, 12 dewa harian, dan papan peringkat rahasia.
* **Teropong Energi Tahunan (Liu Nian)** — ramalan tahunan per shio.
* **Timbangan Kecocokan (Pei Dui)** — kecocokan dua orang, lensa asmara, pertemanan, atau kerja.
* **Roasting Shio (Tu Cao)** — sindiran pedas per shio, personal atau berdua.
* **Afinitas Penjaga Spiritual (Ben Ming Fo)** — figur pelindung, mantra, dan tips Feng Shui.
* **Kue Keberuntungan (Xing Yun Bing)** — pesan dan *lucky item* harian.
* **Quiz Shio Bareng (Ju Hui)** — Ramalan Pasangan, Ramalan Kelompok, dan Tebak Shio Teman.

### 🔜 Segera Hadir
* **Weton** dan **Tarot** — kerangka dasar sudah ada.

---

## 🏗️ Arsitektur Proyek

* **Flask Blueprints**, satu modul per sistem ramalan.
* Zodiak memakai AI (**OpenRouter**); Shio dihitung lokal tanpa AI.
* **MySQL** untuk kuota AI, Quiz Room Zodiak, dan *room* Quiz Shio.

```text
peace-oracle/
├── app.py                # Main Entry Point (Blueprint Registration)
├── core/                 # Shared Assets, Base Templates, & Landing Page
├── modules/              # Core Feature Logic (Isolated per astrology system)
│   ├── zodiak/           # Western Astrology Module
│   ├── shio/             # Eastern (Chinese) Astrology Module
│   ├── weton/            # (WIP) Eastern (Javanese) Astrology Module
│   └── tarot/            # (WIP) Tarot Reading Module
├── api/                  # Serverless entry points (Vercel)
├── .python-version       # Pinned runtime for Vercel & pyenv
└── vercel.json           # Serverless configuration
```

---

## 🚀 Instalasi & Menjalankan Lokal

Butuh **Python 3.13+**.

1. **Clone repository:**
   ```bash
   git clone https://github.com/dikigambol/peace-oracle.git
   cd peace-oracle
   ```

2. **Buat virtual environment (opsional):**
   ```bash
   python -m venv venv

   source venv/bin/activate      # Linux / Mac
   source venv/Scripts/activate  # Windows + Git Bash
   venv\Scripts\activate         # Windows + CMD / PowerShell
   ```

3. **Install dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Isi `.env`:**
   ```bash
   cp .env.example .env
   ```
   * `FLASK_ENV` — isi `production` di server agar mode debug selalu mati.
   * `SECRET_KEY` — wajib.
   * `OPENROUTER_KEY` — untuk narasi AI Zodiak.
   * `DAILY_AI_LIMIT` — kuota AI harian (default `10`).
   * `MYSQL_*` — wajib, untuk kuota AI, Quiz Room Zodiak, dan Quiz Shio.

5. **Jalankan:**
   ```bash
   python app.py
   ```
   > Buka `http://127.0.0.1:5000/`

---

## ☁️ Deployment (Vercel)

1. Hubungkan *repository* ke [Vercel](https://vercel.com).
2. Isi *Environment Variables* sesuai `.env`.
3. Klik **Deploy**. Konfigurasi dibaca otomatis dari `vercel.json`.

---

## 📄 Hak Cipta

**© 2026 Peace Oracle — Seluruh hak dilindungi.**

Repositori ini dibuka agar bisa dibaca dan dipelajari. Isinya **tidak
dilisensikan untuk penggunaan ulang**: dilarang menyalin, memodifikasi,
mendistribusikan, atau menayangkan ulang sebagian maupun seluruhnya tanpa
izin tertulis dari pemilik.

> Gambar ikonografi pada mode Shio dihasilkan dengan bantuan AI generatif.
>
> Data kota kelahiran (nama, bujur, zona waktu) berasal dari
> [GeoNames](https://www.geonames.org/), dilisensikan di bawah
> [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), diambil pada
> 18 September 2026. Data tersebut tetap milik GeoNames dan tidak tercakup
> dalam pembatasan hak cipta di atas.

---

<div align="center">
  <p><b>Peace Oracle</b> • Dibuat dengan ❤️, <i>overthinking</i> tengah malam, dan sedikit paksaan dari Merkurius Retrograde.</p>
</div>
