# Aplikasi Cetak KTM (Kartu Tanda Mahasiswa)

Aplikasi desktop untuk mencetak Kartu Tanda Mahasiswa (KTM) dengan menginputkan NIM mahasiswa. Data otomatis ditampilkan dari database dan dapat diekspor ke format PDF.

## Fitur Utama
- ✅ Input NIM mahasiswa
- ✅ Tampilan otomatis data: NIM, Nama, Prodi
- ✅ Preview KTM
- ✅ Export ke PDF
- ✅ Database penyimpanan data mahasiswa

## Teknologi
- Python 3.8+
- PyQt5 (GUI Desktop)
- SQLite (Database)
- ReportLab (PDF Generation)

## Instalasi

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

```bash
python main.py
```

## Struktur Project
```
cetakKTM/
├── main.py                 # Entry point aplikasi
├── database.py            # Manajemen database
├── ui/
│   └── main_window.py    # Interface utama
├── models/
│   └── mahasiswa.py      # Model data mahasiswa
├── utils/
│   └── pdf_generator.py  # Generator PDF
├── data/
│   └── ktm.db            # Database SQLite
└── requirements.txt      # Dependencies
```