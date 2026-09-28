<div align="center">
  <img src="https://img.icons8.com/?size=100&id=102558&format=png&color=FFFFFF" alt="Peace Oracle" width="80" height="80">
  <h1>Peace Oracle</h1>
  <p>Zodiak, Shio, Weton, dan Tarot (soon) dalam satu app.</p>

  <p>
    <img src="https://img.shields.io/badge/Python-3.13+-3776AB?style=flat-square&labelColor=30363D&logo=python&logoColor=FFD43B" alt="Python 3.13+">
    <img src="https://img.shields.io/badge/Flask-009688?style=flat-square&labelColor=30363D&logo=flask&logoColor=white" alt="Flask">
    <img src="https://img.shields.io/badge/MySQL-4479A1?style=flat-square&labelColor=30363D&logo=mysql&logoColor=white" alt="MySQL">
    <img src="https://img.shields.io/badge/Vercel-7B5CFF?style=flat-square&labelColor=30363D&logo=vercel&logoColor=white" alt="Vercel">
    <img src="https://img.shields.io/badge/Status-Beta-FF8C42?style=flat-square&labelColor=30363D" alt="Beta">
  </p>
</div>

Peace Oracle lahir dari ide simpel: kenapa harus buka banyak situs cuma buat cek ramalan dari tradisi yang beda-beda? Jadi semuanya kami kumpulin di satu tempat. Sekarang sudah ada Zodiak, Shio, dan Weton. Tarot lagi on progress.

UI desktop dan mobile dibangun terpisah, bukan versi desktop yang dipaksa responsif. Hasilnya, di HP rasanya kayak pakai native app.

## Fitur

**Zodiak**
- Ramalan harian yang di-generate AI via OpenRouter. Kalau kuota harian habis, otomatis fallback ke bank ramalan yang sudah disiapkan.
- Profil karakter tiap zodiak.
- Cek kecocokan buat asmara, sahabat, atau rekan kerja. Ada Quiz Room juga buat main berdua, hasilnya di-review AI.
- Roasting, solo atau bareng pasangan. Kurang pedas? Tinggal reroll.

**Shio**
- Ming Li: baca Empat Pilar Ba Zi (八字) dari tanggal, jam, dan kota lahir.
- Tong Shu: almanak harian, 12 dewa harian, plus ranking shio hari ini.
- Liu Nian: forecast energi tahunan per shio.
- Pei Dui: cek kecocokan dua orang, bisa pilih mode asmara, pertemanan, atau kerja.
- Tu Cao: roasting per shio, solo atau berdua.
- Ben Ming Fo: figur pelindung, mantra, dan tips Feng Shui.
- Xing Yun Bing: fortune cookie harian.
- Ju Hui: kuis bareng teman (ramalan pasangan, ramalan grup, dan tebak shio teman).

**Weton**
- Cek weton lahir: neptu, wuku, tanggal Jawa, pranata mangsa, watak, sampai gaya kerja. Lahir setelah maghrib? Hari wetonnya otomatis geser ke hari berikutnya, dihitung sesuai kota lahir.
- Kecocokan weton pakai dua metode petung sekaligus (sisa bagi 8 dan sisa bagi 5).
- Kalender Jawa: weton harian, hari istimewa, hari pantangan, dan reminder wetonan.
- Roasting berdasarkan hari, pasaran, dan neptu.
- Cari hari baik buat nikah, pindah rumah, buka usaha, atau transaksi besar. Hari pantangan disaring, sasi nikah dan petung Pancasuda ikut dihitung, lengkap dengan alasan dan sumbernya.

**Tarot** masih tahap scaffolding, jadi card-nya di landing page masih ke-lock.

Di landing page ada floating button buat switch mode, plus beberapa easter egg kecil. Good luck nyarinya.

## Arsitektur

Tiap sistem ramalan jadi Flask Blueprint sendiri di `modules/`. Semua modul cuma depend ke `core/` dan nggak saling import, jadi satu modul bisa dicabut tanpa bikin yang lain rusak. Navigasi dan landing page otomatis nyesuain modul yang ter-install.

AI cuma dipakai di Zodiak. Shio dan Weton full dihitung di server pakai data dan rumus sendiri, zero API call.

MySQL dipakai buat nyimpen kuota AI dan room kuis. Kalau database lagi down, app tetap jalan: kuota AI pindah ke in-memory store, sementara Quiz Room nonaktif sampai database balik lagi.

```text
peace-oracle/
├── app.py            # entry point, register blueprint
├── core/             # core.py, base template, landing page, shared assets
├── modules/
│   ├── zodiak/
│   ├── shio/
│   ├── weton/
│   └── tarot/        # WIP
├── api/index.py      # entry point Vercel
├── vercel.json
└── .python-version
```

## Setup lokal

Pastikan Python kamu minimal 3.13.

```bash
git clone https://github.com/dikigambol/peace-oracle.git
cd peace-oracle

python -m venv venv
source venv/bin/activate        # Linux / Mac
source venv/Scripts/activate    # Windows (Git Bash)
venv\Scripts\activate           # Windows (CMD / PowerShell)

pip install -r requirements.txt
cp .env.example .env
```

Lalu isi `.env`. Yang penting:

| Variabel | Keterangan |
| --- | --- |
| `SECRET_KEY` | Wajib. Generate pakai `python -c "import secrets; print(secrets.token_hex(32))"` |
| `OPENROUTER_KEY` | Buat ramalan dan review AI di Zodiak |
| `MYSQL_HOST`, `MYSQL_DB`, `MYSQL_USER`, `MYSQL_PASSWORD` | Koneksi database. Kalau kosong, Quiz Room nggak aktif |
| `FLASK_ENV` | Set `production` di server biar debug mode selalu off |

Sisanya opsional dan sudah ada default-nya: `FLASK_DEBUG`, `FLASK_HOST`, `FLASK_PORT` (5000), `MYSQL_PORT` (3306), `DAILY_AI_LIMIT` (10), `FINGERPRINT_AI_LIMIT` (30), `DB_OFFLINE_COOLDOWN` (60 detik), `MEMORY_STORE_MAX` (5000).

Terus run:

```bash
python app.py
```

Buka `http://127.0.0.1:5000/` dan selesai.

## Deploy ke Vercel

Connect repo ke [Vercel](https://vercel.com), copy semua environment variable dari `.env`, lalu deploy. Config-nya sudah siap di `vercel.json`, nggak perlu setting tambahan.

## Hak cipta

© 2026 Peace Oracle. All rights reserved.

Repo ini public supaya kodenya bisa dibaca dan dipelajari, tapi **bukan open source**. Menyalin, memodifikasi, mendistribusikan, atau menayangkan ulang sebagian maupun seluruhnya wajib dapat izin tertulis dari pemilik.

Aset ikon di mode Shio dibuat dengan bantuan generative AI.

Data kota kelahiran untuk Shio dan Weton (nama, bujur, lintang, zona waktu) diambil dari [GeoNames](https://www.geonames.org/) di bawah lisensi [CC BY 4.0](https://creativecommons.org/licenses/by/4.0/) pada 18 September 2026 (data lintang untuk Weton pada 25 September 2026). Data tersebut tetap milik GeoNames dan nggak termasuk dalam pembatasan hak cipta di atas.

---

<div align="center">
  <sub>Built with overthinking tengah malam dan sedikit dorongan dari Merkurius Retrograde.</sub>
</div>
