<div align="center">
  <img src="https://img.icons8.com/?size=100&id=102558&format=png&color=FFFFFF" alt="Peace Oracle Logo" width="80" height="80">
  <br>
  <h1>Peace Oracle</h1>
  <p><b>✨ Temukan Ketenangan Lewat Penyelarasan Kosmik, Oriental, Primbon Nusantara, & Tarot ✨</b></p>
  
  <p>
    <img src="https://img.shields.io/badge/Frontend-Vanilla_JS_&_CSS-orange.svg?style=for-the-badge&logo=javascript&logoColor=white" alt="Frontend">
    <img src="https://img.shields.io/badge/Python-3.9+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python">
    <img src="https://img.shields.io/badge/Framework-Flask-black.svg?style=for-the-badge&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/Database-MySQL-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white" alt="MySQL">
    <br>
    <img src="https://img.shields.io/badge/Deployment-Vercel-black.svg?style=for-the-badge&logo=vercel&logoColor=white" alt="Vercel">
    <img src="https://img.shields.io/badge/Status-Beta-success.svg?style=for-the-badge" alt="Status">
  </p>
</div>

<br>

**Peace Oracle** adalah aplikasi web interaktif yang menyajikan 4 pilar takdir kosmik: panduan astrologi barat (Zodiak), kebijaksanaan oriental (Shio), primbon nusantara (Weton), dan bacaan misteri arcana (Tarot). Dibangun dengan desain antarmuka yang sangat estetik, modern, dan dilengkapi efek *easter-egg* dinamis untuk memanjakan visual pengguna.

---

## 🌟 Fitur Utama

### 🌌 Landing Page (Hub Utama)
* **Portal Nebula 3D:** Halaman beranda dilengkapi animasi CSS *Nebula* interaktif sebagai gerbang sentral untuk memilih 4 jalan takdir Anda.
* **Mode Switcher:** Navigasi melayang (*floating mode switcher*) untuk pindah alam semesta kapan saja.
* **Easter Eggs Kosmik:** Interaksi tersembunyi pada teks *footer* planet 🪐 dan perlindungan anti-bot (*troll routes*) yang unik.

### 🌙 Mode Zodiak (Barat)
* **Ramalan Kosmik Harian:** Dihitung secara dinamis berdasarkan fase bulan dan metrik kosmik hari berjalan, disajikan dengan gaya bahasa *Gen Z* dan rekomendasi trek *YouTube*.
* **Karakteristik General:** Ketahui sifat bawaan fisik, kebiasaan unik, kecocokan *soulmate* hewan, hingga selera *cosmic pantry* dari masing-masing zodiak.
* **Kalkulator Kecocokan (Asmara, Sahabat, Rekan Kerja):** Analisis komprehensif keharmonisan dua zodiak dalam tiga dimensi sosial berbeda.
* **Roasting Zodiak:** Butuh hiburan kasar? Terdapat mode *roasting* pedas (personal & pasangan) khusus untuk setiap zodiak!
* **Kuis Pasangan Real-Time (Live Room):** Fitur kuis interaktif (*multiplayer*)! Buat *room* privat, undang pasangan, jawab pertanyaan sinkronisasi bersama, dan dapatkan analisis *chemistry* berbasis AI secara langsung.

### 🐉 Mode Shio (Oriental)
* **Profil Karakter Shio:** Ketahui karakteristik bawaan, kecenderungan *green flag/red flag*, dan elemen *alter ego* dari masing-masing Shio.
* **Almanak Harian (Tong Shu):** Dasbor harian interaktif *real-time* yang menampilkan hoki, status hari astrologi BaZi resmi (Chong, San He, Xiang Xing, Ben Ming) beserta *daily tip* untuk ke-12 Shio.
* **Pilih Penjaga Spiritual:** Eksplorasi figur Bodhisattva pelindung spiritual lengkap dengan mantra suci dan tips Feng Shui.
* **Timbangan Jodoh Kosmik:** Kalkulator kecocokan dua shio dengan visualisasi persentase *neon circular progress bar*.
* **Segera Hadir (SOON):** Baca Gulungan Takdir (Kalkulator Bazi), Teropong Energi Tahunan, dan Roasting Shio.
* **Latar Belakang Interaktif:** Tampilan *partikel galaksi 3D* interaktif.

### 🔜 Mode Mendatang (Terkunci / Coming Soon)
* **Weton (Kejawen):** Perhitungan primbon berdasarkan neptu hari dan pasaran Jawa (Kerangka dasar/Blueprint sudah aktif).
* **Tarot:** Pembacaan nasib lewat *spread* kartu Arcana (Kerangka dasar/Blueprint sudah aktif).

---

## 🏗️ Arsitektur Proyek (Modular)

Aplikasi ini menggunakan arsitektur **Flask Blueprints** untuk memastikan skalabilitas dan kebersihan kode (*clean architecture*). Seluruh sistem ramalan dan teks ditenagai oleh **Dynamic Data Bank** yang memastikan setiap respons (*roasting*, nasib harian, hingga profil karakter) tidak repetitif dan terasa lebih personal.

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
└── vercel.json           # Serverless configuration
```

---

## 🚀 Instalasi & Menjalankan Lokal

Pastikan Anda telah menginstal **Python 3.9+**.

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/username/peace-oracle.git
   cd peace-oracle
   ```

2. **Buat Virtual Environment (Opsional tapi disarankan):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # atau
   venv\Scripts\activate     # Windows
   ```

3. **Konfigurasi Environment (`.env`):**
   Aplikasi ini dijamin keamanannya secara dinamis. Buat file `.env` di direktori utama dan tambahkan (minimal):
   ```env
   FLASK_ENV=development
   FLASK_DEBUG=True
   SECRET_KEY=isi_dengan_teks_acak_rahasia
   # Konfigurasi MYSQL_HOST, DB, dll ditambahkan jika menggunakan database
   ```

4. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Jalankan Aplikasi:**
   ```bash
   python app.py
   # ATAU menggunakan Flask CLI:
   # flask --app app.py run
   ```
   > Aplikasi akan berjalan di `http://127.0.0.1:5000/`

---

## ☁️ Deployment (Vercel)

Proyek ini sudah dikonfigurasi sepenuhnya agar berjalan lancar sebagai **Serverless Functions** di Vercel. Anda tidak perlu melakukan *setting* tambahan pada file Python.

1. Hubungkan *repository* GitHub Anda dengan [Vercel](https://vercel.com).
2. Buat proyek baru (*Add New Project*) dan pilih *repository* ini.
3. Vercel akan secara otomatis mendeteksi konfigurasi dari file `vercel.json` dan menjadikan `api/index.py` sebagai *entry point*.
4. Biarkan pengaturan *Framework Preset* pada opsi default (Vercel akan mendeteksinya sebagai Python Serverless).
5. Klik **Deploy**! Aplikasi Anda kini *live*.

---

<div align="center">
  <p><b>Peace Oracle</b> • Dibuat dengan ❤️, <i>overthinking</i> tengah malam, dan sedikit paksaan dari Merkurius Retrograde.</p>
</div>
