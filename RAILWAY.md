# Railway Deployment Guide for Aplikasi Cetak KTM

## Quick Start dengan Railway

### 1. Setup Awal (One-time)
```bash
# Install Railway CLI
npm install -g @railway/cli

# Login ke Railway
railway login
```

### 2. Deploy ke Railway
```bash
# Di folder project
cd cetakKTM
railway init
# Pilih: Create a new project
# Project name: cetakktm
```

### 3. Automatic Deployment
- Railway akan auto-detect Python
- Jalankan build command: `pip install -r requirements.txt`
- Start command: Baca dari Procfile (sudah ada)
- Deploy otomatis setiap push ke GitHub!

### Atau via Web Dashboard (Lebih Mudah):
1. Go to https://railway.app
2. Login dengan GitHub
3. Klik "New Project" → "Deploy from GitHub"
4. Select repository: `hasrul-rahman/cetakKTM`
5. Railway auto-detect dan deploy!
6. Tunggu ~2-3 menit
7. Buka URL yang diberikan Railway

## Environment Variables (Optional)
Di Railway Dashboard → Variables:
```
FLASK_ENV=production
FLASK_DEBUG=False
```

## Database & Storage
- SQLite database tersimpan di `/data/ktm.db`
- PDF output tersimpan di `/output/`
- Railway auto-mount persistent storage

## Monitoring
- Buka Railway Dashboard → Deployments
- Lihat logs real-time
- Monitor resource usage

## Custom Domain (Optional)
1. Di Railway Dashboard → Settings
2. Custom Domain
3. Add domain
4. Setup DNS di registrar Anda

## Scale Up (Optional)
1. Di Railway Dashboard → Settings
2. Instances → Upgrade
3. Pilih resource yang lebih besar

## Troubleshooting

### Build Gagal?
```bash
# Check logs di Railway dashboard
# Rebuild: Railway → Deployments → Redeploy
```

### Database Error?
```bash
# Railway akan auto-create /data folder
# Jika error, restart deployment
```

### API tidak bisa diakses?
```bash
# Buka Railway URL + /health
# Contoh: https://cetakktm-production.up.railway.app/health
# Harus return: {"status": "healthy"}
```

## Tips
- Railway gratis untuk 500 jam/bulan (~20 hari non-stop)
- Auto-scaling jika traffic tinggi
- PostgreSQL/MySQL bisa ditambah di Railway Marketplace
- Email notifications untuk deployment events

Selamat deployment! 🚀
