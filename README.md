# Aplikasi Cetak KTM (Kartu Tanda Mahasiswa) - Web Version

**🎯 Status:** Siap untuk production di Railway, Render, atau Heroku

Aplikasi web untuk mencetak Kartu Tanda Mahasiswa (KTM) dengan menginputkan NIM mahasiswa. Data otomatis ditampilkan dari database dan dapat diekspor ke format PDF.

## ✨ Fitur Utama
- ✅ Input NIM mahasiswa dengan pencarian data real-time
- ✅ Tampilan otomatis data: NIM, Nama, Prodi, Tanggal Lahir
- ✅ Preview KTM dalam browser
- ✅ Export ke PDF dengan format profesional
- ✅ Kelola database mahasiswa (Tambah, Edit, Hapus, Lihat)
- ✅ REST API untuk integrasi dengan aplikasi lain
- ✅ Responsive design untuk desktop dan mobile
- ✅ Production-ready dengan logging

## 🚀 Quick Deploy ke Railway

**Cara paling mudah dan cepat:**

1. Go to https://railway.app
2. Login dengan GitHub
3. Klik "New Project" → "Deploy from GitHub"
4. Select: `hasrul-rahman/cetakKTM`
5. Klik "Deploy Now"
6. Tunggu ~2-3 menit ✨
7. Buka URL yang diberikan Railway

**Itu saja! Aplikasi sudah live.** 🎉

## 🛠️ Teknologi
- **Backend:** Python 3.11 + Flask
- **Frontend:** HTML5 + CSS3 + Vanilla JavaScript
- **Database:** SQLite (built-in, production-ready)
- **PDF Generation:** ReportLab
- **Server:** Gunicorn + Flask-CORS
- **Deployment:** Railway, Render, Heroku, atau Docker

## 📋 Prerequisites
- Git & GitHub account
- Railway account (free: https://railway.app)

## 🏃 Running Locally

```bash
# Clone
git clone https://github.com/hasrul-rahman/cetakKTM.git
cd cetakKTM

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Install dependencies
pip install -r requirements.txt

# Run
python app.py

# Open browser
http://localhost:5000
```

## 🐳 Docker

```bash
# Build
docker build -t cetakktm .

# Run
docker run -p 5000:5000 -v $(pwd)/data:/app/data cetakktm

# Or with compose
docker-compose up
```

## 📁 Project Structure

```
cetakKTM/
├── app.py                      # Flask application
├── database.py                 # Database layer
├── requirements.txt            # Python dependencies
├── Procfile                    # Heroku/Railway config
├── runtime.txt                 # Python version
├── docker-compose.yml          # Docker config
├── Dockerfile                  # Container image
├── RAILWAY.md                  # Railway deployment guide
├── templates/
│   └── index.html             # Main interface
├── static/
│   ├── css/style.css          # Styling
│   └── js/script.js           # Frontend logic
├── models/
│   └── mahasiswa.py           # Data model
├── utils/
│   └── pdf_generator.py       # PDF generation
└── data/
    └── ktm.db                 # SQLite database
```

## 🔌 API Endpoints

Base URL: `https://your-railway-url`

### Search Student
```bash
POST /api/mahasiswa/search
Content-Type: application/json

{ "nim": "123456" }

→ { "nim": "...", "nama": "...", "prodi": "..." }
```

### Get All Students
```bash
GET /api/mahasiswa/all

→ [{ "nim": "...", "nama": "...", "prodi": "..." }, ...]
```

### Add Student
```bash
POST /api/mahasiswa/add
Content-Type: application/json

{ "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "2000-01-01" }

→ { "message": "Data mahasiswa berhasil ditambahkan" }
```

### Update Student
```bash
PUT /api/mahasiswa/update
Content-Type: application/json

{ "nim": "...", "nama": "...", "prodi": "..." }

→ { "message": "Data mahasiswa berhasil diperbarui" }
```

### Delete Student
```bash
DELETE /api/mahasiswa/delete
Content-Type: application/json

{ "nim": "123456" }

→ { "message": "Data mahasiswa berhasil dihapus" }
```

### Generate PDF
```bash
POST /api/ktm/generate
Content-Type: application/json

{ "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "2000-01-01" }

← Binary PDF file (auto-download)
```

### Preview PDF
```bash
POST /api/ktm/preview
Content-Type: application/json

{ "nim": "...", "nama": "...", "prodi": "...", "tanggal_lahir": "2000-01-01" }

← Binary PDF file (open in browser)
```

### Health Check
```bash
GET /health

→ { "status": "healthy", "timestamp": "2024-08-20T..." }
```

## 🔐 Security Notes

Para production, pertimbangkan:
- ✅ Implement authentication/authorization
- ✅ Enable HTTPS (Railway auto-enables)
- ✅ Rate limiting untuk API
- ✅ Input validation (sudah ada)
- ✅ Environment variables untuk secrets
- ✅ CORS configuration (sudah ada)

## 📊 Deployment Options

| Platform | Price | Setup Time | Pros |
|----------|-------|------------|------|
| **Railway** | Free (500h/mo) | 2 min | Easiest, auto-deploy from GitHub |
| **Render** | Free tier | 3 min | Good for side projects |
| **Heroku** | Paid | 5 min | Industry standard |
| **DigitalOcean** | $5/mo | 10 min | Full control, cheap |
| **Docker** | Varies | 15 min | Any host with Docker |

## 🤝 Contributing

Pull requests welcome! Silakan:
1. Fork repository
2. Create feature branch (`git checkout -b feature/amazing`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing`)
5. Open Pull Request

## 📝 License

MIT License - feel free to use in commercial projects

## 🆘 Support

- Issues: GitHub Issues
- Docs: README.md & RAILWAY.md
- Email: hasrulrahman@gmail.com

---

**Version 2.0** - Web Version for Railway & Cloud Platforms

Last Updated: 2026-08-20

Happy coding! 🚀
