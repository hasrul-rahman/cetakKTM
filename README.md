Tambahan fitur: upload background, upload foto, bulk CSV insert
-------------------------------------------------------------

Cara pakai (lokal):
1. Buat branch:
   git checkout -b feature/bg-photo-bulk

2. Tambahkan file-file seperti di repo (app.py, models.py, uploads.py, templates/, static/...)

3. Pasang dependensi:
   pip install -r requirements.txt

4. Jalankan:
   python app.py

5. Buka:
   - http://127.0.0.1:5000/        -> lihat daftar mahasiswa (background diterapkan)
   - http://127.0.0.1:5000/settings -> upload background / CSV / foto

Catatan:
- CSV header wajib mengandung kolom: nim, nama, prodi
- Foto disimpan di: static/photos/<nim>.<ext>
- Background disimpan di: static/backgrounds/current_bg.<ext>
- Di produksi, tambahkan autentikasi untuk membatasi akses upload dan batasi ukuran file.
