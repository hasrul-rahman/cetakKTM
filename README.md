# Aplikasi Cetak KTM (Kartu Tanda Mahasiswa) - Web Version

Aplikasi web untuk mencetak Kartu Tanda Mahasiswa (KTM) dengan menginputkan NIM mahasiswa. Data otomatis ditampilkan dari database dan dapat diekspor ke format PDF. **Versi 2.0: Sekarang sebagai aplikasi web yang dapat dihost di Cloudflare atau server lainnya.**

## ✨ Fitur Utama
- ✅ Input NIM mahasiswa dengan pencarian data real-time
- ✅ Tampilan otomatis data: NIM, Nama, Prodi, Tanggal Lahir
- ✅ Preview KTM dalam browser
- ✅ Export ke PDF dengan format profesional
- ✅ Kelola database mahasiswa (Tambah, Edit, Hapus, Lihat)
- ✅ REST API untuk integrasi dengan aplikasi lain
- ✅ Responsive design untuk desktop dan mobile
- ✅ Deployment di Cloudflare Workers (opsional)

## 🛠️ Teknologi
- **Backend:** Python 3.8+ dengan Flask
- **Frontend:** HTML5, CSS3, JavaScript (Vanilla)
- **Database:** SQLite (dapat diganti dengan PostgreSQL/MySQL untuk production)
- **PDF Generation:** ReportLab
- **Deployment:** Docker, Cloudflare Workers, atau VPS tradisional

## 📋 Prerequisites
- Python 3.8 atau lebih tinggi
- pip (Python package manager)
- SQLite3 (biasanya sudah included dengan Python)

## 🚀 Instalasi & Menjalankan Aplikasi

### 1. Clone Repository
```bash
git clone https://github.com/hasrul-rahman/cetakKTM.git
cd cetakKTM
```

### 2. Setup Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Menjalankan Aplikasi Lokal
```bash
python app.py
```

Aplikasi akan berjalan di: **http://localhost:5000**

## 🐳 Menjalankan dengan Docker

### Build Docker Image
```bash
docker build -t cetakktm:latest .
```

### Run Container
```bash
docker run -p 5000:5000 -v $(pwd)/data:/app/data cetakktm:latest
```

Atau dengan docker-compose:
```bash
docker-compose up
```

## ☁️ Deploy ke Cloudflare Workers (Opsional)

Untuk deployment serverless di Cloudflare, ikuti langkah-langkah di bawah:

### 1. Install Wrangler CLI
```bash
npm install -g wrangler
```

### 2. Konfigurasi Cloudflare
```bash
wrangler login
```

### 3. Setup D1 Database
```bash
wrangler d1 create cetakktm
```

### 4. Deploy
```bash
wrangler deploy
```

**Catatan:** Untuk deployment Cloudflare, diperlukan refactor tambahan untuk menggunakan Cloudflare D1 atau R2 untuk storage.

## 📁 Struktur Project

```
cetakKTM/
├── app.py                     # Entry point aplikasi Flask
├── database.py               # Manajemen database SQLite
├── requirements.txt          # Python dependencies
├── Dockerfile               # Docker configuration
├── wrangler.toml           # Cloudflare Workers config
├── templates/
│   └── index.html          # Main HTML interface
├── static/
│   ├── css/
│   │   └── style.css       # Styling
│   └── js/
│       └── script.js       # Frontend logic
├── models/
│   └── mahasiswa.py        # Data model
├── utils/
│   └── pdf_generator.py    # PDF generation logic
├── data/
│   └── ktm.db              # SQLite database
└── output/
    └── *.pdf               # Generated PDF files
```

## 🔌 API Endpoints

### Search Student
```
POST /api/mahasiswa/search
Body: { "nim": "123456" }
Response: { "nim": "...", "nama": "...", "prodi": "..." }
```

### Get All Students
```
GET /api/mahasiswa/all
Response: [{ "nim": "...", "nama": "...", "prodi": "..." }, ...]
```

### Add Student
```
POST /api/mahasiswa/add
Body: { "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "..." }
Response: { "message": "Data mahasiswa berhasil ditambahkan" }
```

### Update Student
```
PUT /api/mahasiswa/update
Body: { "nim": "...", "nama": "...", "prodi": "..." }
Response: { "message": "Data mahasiswa berhasil diperbarui" }
```

### Delete Student
```
DELETE /api/mahasiswa/delete
Body: { "nim": "123456" }
Response: { "message": "Data mahasiswa berhasil dihapus" }
```

### Generate PDF
```
POST /api/ktm/generate
Body: { "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "..." }
Response: Binary PDF file (download)
```

### Preview PDF
```
POST /api/ktm/preview
Body: { "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "..." }
Response: Binary PDF file (open in browser)
```

### Health Check
```
GET /health
Response: { "status": "healthy" }
```

## 📝 Catatan Penting

### Development vs Production
- **Development:** Gunakan `python app.py`
- **Production:** Gunakan Gunicorn atau uWSGI
  ```bash
  gunicorn --bind 0.0.0.0:5000 app:app
  ```

### Database
- SQLite digunakan untuk development
- Untuk production, pertimbangkan menggunakan PostgreSQL atau MySQL
- Database file disimpan di folder `data/`

### Security
- Implementasi authentication/authorization sebelum production
- Gunakan environment variables untuk sensitive data
- Enable HTTPS di production
- Implementasi rate limiting untuk API

## 🤝 Kontribusi
Silakan buat pull request untuk fitur baru atau perbaikan bug.

## 📄 Lisensi
Proyek ini tersedia di bawah lisensi MIT.

## 📞 Support
Untuk pertanyaan atau issue, silakan buat GitHub Issue.

---

**Version 2.0** - Web Version for Cloudflare & Traditional Servers
Last Updated: 2024
