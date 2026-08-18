<div align="center">
  <img src="https://img.icons8.com/?size=100&id=102558&format=png&color=FFFFFF" alt="Zodiak Peace Logo" width="80" height="80">
  <br>
  <h1>Zodiak Peace</h1>
  <p><b>✨ Temukan Ketenangan Lewat Penyelarasan Kosmik & Keberuntungan Oriental ✨</b></p>
  
  <p>
    <a href="#fitur-utama"><img src="https://img.shields.io/badge/Fitur-Multi--Mode-blue.svg?style=for-the-badge&logo=flask" alt="Fitur"></a>
    <a href="#arsitektur"><img src="https://img.shields.io/badge/Arsitektur-Flask_Blueprints-orange.svg?style=for-the-badge&logo=python" alt="Arsitektur"></a>
    <a href="#deployment"><img src="https://img.shields.io/badge/Deployment-Vercel_Serverless-black.svg?style=for-the-badge&logo=vercel" alt="Vercel"></a>
  </p>
</div>

<br>

**Zodiak Peace** adalah aplikasi web interaktif yang menyajikan panduan astrologi (Zodiak) dan kebijaksanaan oriental (Shio). Dibangun dengan desain antarmuka yang sangat estetik, modern, dan dilengkapi efek *easter-egg* dinamis untuk memanjakan visual pengguna.

---

## 🌟 Fitur Utama

### 🌌 Landing Page (Hub Utama)
* **Portal Nebula 3D:** Halaman beranda dilengkapi animasi CSS *Nebula* yang sangat memanjakan mata, sebagai gerbang sentral untuk memilih 4 jalan takdir Anda.
* **Mode Switcher:** Navigasi melayang (*floating mode switcher*) untuk pindah alam semesta kapan saja.

### 🌙 Mode Zodiak
* **Ramalan Kosmik Harian:** Dihitung berdasarkan fase bulan dan posisi planet secara aktual (menggunakan library `ephem`).
* **Karakteristik General:** Ketahui sifat, kebiasaan unik, kecocokan *soulmate* hewan, hingga selera *cosmic pantry* dari masing-masing zodiak.
* **Kalkulator Kecocokan:** Cek skor kecocokan antara dua zodiak dalam 3 mode: Asmara, Sahabat (Bestie), dan Rekan Kerja.
* **Roasting Zodiak:** Butuh hiburan kasar? Terdapat mode *roasting* pedas khusus untuk setiap zodiak!

### 🐉 Mode Shio (Oriental)
* **Sistem Hitung Otomatis (Baru!):** Masukkan tanggal lahir Anda menggunakan *Premium Date Picker* (Flatpickr), dan sistem akan secara otomatis mengkalkulasi elemen kosmik serta Shio Anda!
* **Generator Takdir Unik:** Setiap kombinasi dari 12 Shio + 5 Elemen (60 kombinasi unik) menghasilkan ramalan Karir, Asmara, Keuangan, dan Kesehatan yang dipersonalisasi.
* **Background 3D Interaktif:** Menyertakan `Three.js` untuk merender galaksi 3D partikel yang merespon gerakan *mouse*!
* **Efek Easter-Egg (Drag & Burst):** Klik dan seret (*drag*) partikel kosmik di layar untuk menciptakan ledakan cahaya di halaman Shio.

### 🔜 Mode Mendatang (Terkunci)
* **Weton (Jawa):** Perhitungan primbon berdasarkan neptu hari dan pasaran.
* **Tarot:** Pembacaan takdir melalui kartu *arcana*.

---

## 🏗️ Arsitektur Proyek (Modular)

Aplikasi ini menggunakan arsitektur **Flask Blueprints** untuk memastikan skalabilitas dan kebersihan kode (*clean architecture*).

```text
zodiac-z/
├── app.py                      # Entry point Flask (Meregistrasi Blueprints & Rute Utama)
├── core/                       # Template & CSS/JS Global
│   ├── static/css/home.css     # CSS untuk Landing Page Hub
│   └── templates/home.html     # Landing Page Utama (Hub)
├── modules/
│   ├── zodiak/                 # Blueprint Zodiak (Routes, Data, Templates, Static)
│   ├── shio/                   # Blueprint Shio (Routes, Data, Templates, Static)
│   ├── weton/                  # Placeholder untuk Weton
│   └── tarot/                  # Placeholder untuk Tarot
├── requirements.txt            # Dependensi Python
├── vercel.json                 # Konfigurasi Deployment Serverless Vercel
└── api/index.py                # Adapter Vercel
```

---

## 🚀 Instalasi & Menjalankan Lokal

Pastikan Anda telah menginstal **Python 3.9+**.

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/username/zodiac-z.git
   cd zodiac-z
   ```

2. **Buat Virtual Environment (Opsional tapi disarankan):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Untuk Linux/Mac
   # atau
   venv\Scripts\activate     # Untuk Windows
   ```

3. **Install Dependensi:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Jalankan Aplikasi Flask:**
   ```bash
   flask --app app.py run --debug
   ```
   > Aplikasi akan berjalan di `http://127.0.0.1:5000/`

---

## ☁️ Deployment (Vercel)

Proyek ini sudah dikonfigurasi sepenuhnya agar berjalan lancar sebagai **Serverless Functions** di Vercel. Anda tidak perlu melakukan *setting* tambahan pada file Python.

1. Hubungkan *repository* GitHub Anda dengan Vercel.
2. Vercel akan secara otomatis membaca file `vercel.json` dan folder `api/index.py`.
3. Klik **Deploy**!

---

<div align="center">
  <p>Dibuat dengan ❤️ dan debu kosmik.</p>
</div>
