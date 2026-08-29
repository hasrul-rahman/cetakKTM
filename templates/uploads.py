import os
from flask import Blueprint, current_app, request, jsonify
from werkzeug.utils import secure_filename
from models import db, Mahasiswa

uploads_bp = Blueprint('uploads', __name__)

ALLOWED_IMG = {'png', 'jpg', 'jpeg', 'gif'}
MAX_CSV_ROWS = 5000  # safety limit; adjust if needed

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_IMG

@uploads_bp.route('/upload-background', methods=['POST'])
def upload_background():
    if 'background' not in request.files:
        return jsonify({'error': 'no file'}), 400
    f = request.files['background']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    if f and allowed_file(f.filename):
        ext = f.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"current_bg.{ext}")
        save_dir = os.path.join(current_app.static_folder, 'backgrounds')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        f.save(save_path)
        return jsonify({'ok': True, 'path': '/static/backgrounds/' + filename})
    return jsonify({'error': 'invalid file type'}), 400

@uploads_bp.route('/upload-photo/<nim>', methods=['POST'])
def upload_photo(nim):
    if 'photo' not in request.files:
        return jsonify({'error': 'no file'}), 400
    f = request.files['photo']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400
    if f and allowed_file(f.filename):
        ext = f.filename.rsplit('.', 1)[1].lower()
        filename = secure_filename(f"{nim}.{ext}")
        save_dir = os.path.join(current_app.static_folder, 'photos')
        os.makedirs(save_dir, exist_ok=True)
        save_path = os.path.join(save_dir, filename)
        f.save(save_path)
        # update DB: store filename only
        m = Mahasiswa.query.get(nim)
        if m:
            m.photo_path = filename
        else:
            m = Mahasiswa(nim=nim, nama='(nama belum diisi)', prodi='(prodi belum)', photo_path=filename)
            db.session.add(m)
        db.session.commit()
        return jsonify({'ok': True, 'photo': '/static/photos/' + filename})
    return jsonify({'error': 'invalid file type'}), 400

@uploads_bp.route('/bulk-insert', methods=['POST'])
def bulk_insert():
    if 'csvfile' not in request.files:
        return jsonify({'error': 'no file'}), 400
    f = request.files['csvfile']
    if f.filename == '':
        return jsonify({'error': 'empty filename'}), 400

    import csv, io
    try:
        # decode to text
        content = f.stream.read().decode('utf-8', errors='ignore')
    except Exception:
        return jsonify({'error': 'cannot read file'}), 400

    stream = io.StringIO(content)
    reader = csv.DictReader(stream)
    inserted = 0
    updated = 0
    errors = []
    rows_processed = 0

    for i, row in enumerate(reader, start=1):
        rows_processed += 1
        if rows_processed > MAX_CSV_ROWS:
            errors.append({'row': i, 'reason': 'row limit exceeded'})
            break
        # try common header names
        nim = (row.get('nim') or row.get('NIM') or row.get('nis') or '').strip()
        nama = (row.get('nama') or row.get('Nama') or row.get('name') or '').strip()
        prodi = (row.get('prodi') or row.get('Prodi') or row.get('program') or '').strip()
        if not nim or not nama or not prodi:
            errors.append({'row': i, 'reason': 'missing field', 'row_data': row})
            continue
        m = Mahasiswa.query.get(nim)
        if m:
            m.nama = nama
            m.prodi = prodi
            updated += 1
        else:
            m = Mahasiswa(nim=nim, nama=nama, prodi=prodi)
            db.session.add(m)
            inserted += 1

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'db error', 'detail': str(e)}), 500

    return jsonify({'inserted': inserted, 'updated': updated, 'errors': errors, 'rows_processed': rows_processed})