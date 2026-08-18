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

### 🌙 Mode Zodiak
* **Ramalan Kosmik Harian:** Dihitung berdasarkan fase bulan dan posisi planet secara aktual (menggunakan library `ephem`).
* **Karakteristik General:** Ketahui sifat, kebiasaan unik, kecocokan *soulmate* hewan, hingga selera *cosmic pantry* dari masing-masing zodiak.
* **Kalkulator Kecocokan:** Cek skor kecocokan antara dua zodiak dalam 3 mode: Asmara, Sahabat (Bestie), dan Rekan Kerja.
* **Roasting Zodiak:** Butuh hiburan kasar? Terdapat mode *roasting* pedas khusus untuk setiap zodiak!

### 🐉 Mode Shio (Oriental)
* **Kalkulator Elemen:** Gabungkan energi 12 Lambang Shio (Tikus, Macan, Naga, dll.) dengan 5 Elemen Kosmik (Air, Kayu, Api, Tanah, Logam).
* **Efek Easter-Egg Interaktif:** Klik pada *background* halaman Shio untuk melihat ledakan partikel kembang api emas & merah!
* **Desain Premium:** Menggunakan skema warna merah dan emas elegan yang sangat lekat dengan kebudayaan timur.

### 🔜 Mode Mendatang (Terkunci)
* **Weton (Jawa):** Perhitungan primbon berdasarkan neptu hari dan pasaran.
* **Tarot:** Pembacaan takdir melalui kartu *arcana*.

---

## 🏗️ Arsitektur Proyek (Modular)

Aplikasi ini menggunakan arsitektur **Flask Blueprints** untuk memastikan skalabilitas dan kebersihan kode (*clean architecture*).

```text
zodiac-z/
├── app.py                      # Entry point Flask (Meregistrasi Blueprints)
├── core/                       # Template & CSS/JS Global (Loader, Mode Switcher)
├── modules/
│   ├── zodiak/                 # Blueprint Zodiak (Routes, Data, Templates, Static)
│   ├── shio/                   # Blueprint Shio (Routes, Data, Templates, Static)
│   ├── weton/                  # Placeholder untuk Weton
│   └── tarot/                  # Placeholder untuk Tarot
├── vercel.json                 # Konfigurasi Serverless Vercel
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
