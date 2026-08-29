#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify, send_file
from flask_cors import CORS
import os
from datetime import datetime
from io import BytesIO
import logging

from database import Database
from utils.pdf_generator import PDFGenerator
from utils.file_handler import FileHandler
from utils.excel_handler import ExcelHandler
from models.mahasiswa import Mahasiswa

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Configure upload folder
UPLOAD_FOLDER = 'uploads'
MAX_FILE_SIZE = 500 * 1024  # 500 KB

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = MAX_FILE_SIZE

# Initialize database, PDF generator, and file handler
try:
    db = Database()
    pdf_gen = PDFGenerator()
    file_handler = FileHandler()
    logger.info("Database, PDF generator, and file handler initialized successfully")
except Exception as e:
    logger.error(f"Error initializing components: {str(e)}")
    raise

@app.route('/')
def index():
    """Render main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== MAHASISWA ENDPOINTS ==========

@app.route('/api/mahasiswa/search', methods=['POST'])
def search_mahasiswa():
    """Search student by NIM"""
    try:
        data = request.get_json()
        nim = data.get('nim', '').strip()
        
        if not nim:
            return jsonify({'error': 'NIM harus diisi'}), 400
        
        result = db.search_mahasiswa_by_nim(nim)
        
        if result:
            return jsonify(result), 200
        else:
            return jsonify({'error': f'Data mahasiswa dengan NIM {nim} tidak ditemukan'}), 404
    
    except Exception as e:
        logger.error(f"Error searching mahasiswa: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mahasiswa/all', methods=['GET'])
def get_all_mahasiswa():
    """Get all students"""
    try:
        data = db.get_all_mahasiswa()
        return jsonify(data), 200
    except Exception as e:
        logger.error(f"Error getting all mahasiswa: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mahasiswa/add', methods=['POST'])
def add_mahasiswa():
    """Add new student"""
    try:
        data = request.get_json()
        nim = data.get('nim', '').strip()
        nama = data.get('nama', '').strip()
        prodi = data.get('prodi', '').strip()
        tanggal_lahir = data.get('tanggal_lahir', '')
        alamat = data.get('alamat', '')
        
        if not nim or not nama or not prodi:
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        if db.insert_mahasiswa(nim, nama, prodi, tanggal_lahir, alamat):
            logger.info(f"Mahasiswa added: {nim}")
            return jsonify({'message': 'Data mahasiswa berhasil ditambahkan'}), 201
        else:
            return jsonify({'error': f'NIM {nim} sudah terdaftar'}), 409
    
    except Exception as e:
        logger.error(f"Error adding mahasiswa: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mahasiswa/update', methods=['PUT'])
def update_mahasiswa():
    """Update student data"""
    try:
        data = request.get_json()
        nim = data.get('nim', '').strip()
        nama = data.get('nama', '').strip()
        prodi = data.get('prodi', '').strip()
        tanggal_lahir = data.get('tanggal_lahir', '')
        alamat = data.get('alamat', '')
        
        if not nim or not nama or not prodi:
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        db.update_mahasiswa(nim, nama, prodi, tanggal_lahir, alamat)
        logger.info(f"Mahasiswa updated: {nim}")
        return jsonify({'message': 'Data mahasiswa berhasil diperbarui'}), 200
    
    except Exception as e:
        logger.error(f"Error updating mahasiswa: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mahasiswa/delete', methods=['DELETE'])
def delete_mahasiswa():
    """Delete student"""
    try:
        data = request.get_json()
        nim = data.get('nim', '').strip()
        
        if not nim:
            return jsonify({'error': 'NIM harus diisi'}), 400
        
        db.delete_mahasiswa(nim)
        logger.info(f"Mahasiswa deleted: {nim}")
        return jsonify({'message': 'Data mahasiswa berhasil dihapus'}), 200
    
    except Exception as e:
        logger.error(f"Error deleting mahasiswa: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== PHOTO UPLOAD ENDPOINTS ==========

@app.route('/api/mahasiswa/upload-foto', methods=['POST'])
def upload_foto():
    """Upload foto mahasiswa"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'File tidak ditemukan'}), 400
        
        if 'nim' not in request.form:
            return jsonify({'error': 'NIM tidak ditemukan'}), 400
        
        file = request.files['file']
        nim = request.form['nim'].strip()
        
        # Validasi bahwa mahasiswa ada
        mahasiswa = db.search_mahasiswa_by_nim(nim)
        if not mahasiswa:
            return jsonify({'error': f'Mahasiswa dengan NIM {nim} tidak ditemukan'}), 404
        
        # Save foto
        foto_path, error = file_handler.save_student_photo(file, nim)
        if error:
            return jsonify({'error': error}), 400
        
        # Update database
        db.update_mahasiswa_foto(nim, foto_path)
        logger.info(f"Foto uploaded for NIM: {nim}")
        
        return jsonify({
            'message': 'Foto berhasil diupload',
            'foto_path': foto_path
        }), 200
    
    except Exception as e:
        logger.error(f"Error uploading foto: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== KTM SETTINGS ENDPOINTS ==========

@app.route('/api/ktm/settings', methods=['GET'])
def get_ktm_settings():
    """Get KTM settings"""
    try:
        settings = db.get_ktm_settings()
        return jsonify(settings or {}), 200
    except Exception as e:
        logger.error(f"Error getting KTM settings: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ktm/upload-background', methods=['POST'])
def upload_ktm_background():
    """Upload KTM background"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'File tidak ditemukan'}), 400
        
        file = request.files['file']
        
        # Save background
        bg_path, error = file_handler.save_ktm_background(file)
        if error:
            return jsonify({'error': error}), 400
        
        # Update database
        db.update_ktm_background(bg_path)
        logger.info(f"KTM background updated")
        
        return jsonify({
            'message': 'Background KTM berhasil diubah',
            'background_path': bg_path
        }), 200
    
    except Exception as e:
        logger.error(f"Error uploading background: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ktm/font-color', methods=['PUT'])
def update_font_color():
    """Update KTM font color"""
    try:
        data = request.get_json()
        font_color = data.get('font_color', '#000000')
        
        if not font_color.startswith('#'):
            font_color = '#' + font_color
        
        db.update_ktm_font_color(font_color)
        logger.info(f"KTM font color updated: {font_color}")
        
        return jsonify({
            'message': 'Warna font berhasil diubah',
            'font_color': font_color
        }), 200
    
    except Exception as e:
        logger.error(f"Error updating font color: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== PDF GENERATION ENDPOINTS ==========

@app.route('/api/ktm/generate', methods=['POST'])
def generate_pdf():
    """Generate KTM PDF"""
    try:
        data = request.get_json()
        mahasiswa_data = {
            'nim': data.get('nim', ''),
            'nama': data.get('nama', ''),
            'prodi': data.get('prodi', ''),
            'tanggal_lahir': data.get('tanggal_lahir', ''),
            'foto_path': data.get('foto_path')
        }
        
        if not all([mahasiswa_data['nim'], mahasiswa_data['nama'], mahasiswa_data['prodi']]):
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        # Get KTM settings
        settings = db.get_ktm_settings()
        bg_path = settings.get('background_path') if settings else None
        font_color = settings.get('font_color') if settings else '#000000'
        
        # Generate PDF in memory
        pdf_buffer = pdf_gen.generate_ktm_bytes(mahasiswa_data, bg_path, font_color)
        logger.info(f"PDF generated for NIM: {mahasiswa_data['nim']}")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f"KTM_{mahasiswa_data['nim']}.pdf"
        )
    
    except Exception as e:
        logger.error(f"Error generating PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/ktm/preview', methods=['POST'])
def preview_pdf():
    """Preview KTM PDF"""
    try:
        data = request.get_json()
        mahasiswa_data = {
            'nim': data.get('nim', ''),
            'nama': data.get('nama', ''),
            'prodi': data.get('prodi', ''),
            'tanggal_lahir': data.get('tanggal_lahir', ''),
            'foto_path': data.get('foto_path')
        }
        
        if not all([mahasiswa_data['nim'], mahasiswa_data['nama'], mahasiswa_data['prodi']]):
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        # Get KTM settings
        settings = db.get_ktm_settings()
        bg_path = settings.get('background_path') if settings else None
        font_color = settings.get('font_color') if settings else '#000000'
        
        # Generate PDF in memory for preview
        pdf_buffer = pdf_gen.generate_ktm_bytes(mahasiswa_data, bg_path, font_color)
        logger.info(f"PDF preview for NIM: {mahasiswa_data['nim']}")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        logger.error(f"Error previewing PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== BULK IMPORT ENDPOINTS ==========

@app.route('/api/mahasiswa/import-excel', methods=['POST'])
def import_excel():
    """Import mahasiswa dari file Excel"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'File tidak ditemukan'}), 400
        
        file = request.files['file']
        
        # Validasi file
        is_valid, error = file_handler.validate_excel_file(file)
        if not is_valid:
            return jsonify({'error': error}), 400
        
        # Parse Excel
        mahasiswa_list, error = ExcelHandler.parse_excel(file)
        if error:
            return jsonify({'error': error}), 400
        
        # Insert data
        results = db.insert_bulk_mahasiswa(mahasiswa_list)
        
        logger.info(f"Bulk import completed: {results['success']} success, {results['failed']} failed")
        
        return jsonify({
            'message': 'Import data selesai',
            'success': results['success'],
            'failed': results['failed'],
            'errors': results['errors'][:10]  # Limit errors to 10
        }), 200
    
    except Exception as e:
        logger.error(f"Error importing Excel: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/mahasiswa/import-template', methods=['GET'])
def download_import_template():
    """Download template Excel untuk import"""
    try:
        import openpyxl
        
        wb = openpyxl.Workbook()
        ws = wb.active
        ws.title = 'Mahasiswa'
        
        # Header
        headers = ['NIM', 'Nama', 'Prodi', 'Tanggal Lahir (YYYY-MM-DD)', 'Alamat']
        ws.append(headers)
        
        # Sample data
        ws.append(['123456', 'Budi Santoso', 'Teknik Informatika', '2000-01-15', 'Jl. Merdeka'])
        ws.append(['123457', 'Siti Nurhaliza', 'Sistem Informasi', '2000-02-20', 'Jl. Sudirman'])
        
        # Set column width
        ws.column_dimensions['A'].width = 15
        ws.column_dimensions['B'].width = 25
        ws.column_dimensions['C'].width = 25
        ws.column_dimensions['D'].width = 20
        ws.column_dimensions['E'].width = 30
        
        # Save to BytesIO
        output = BytesIO()
        wb.save(output)
        output.seek(0)
        
        return send_file(
            output,
            mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            as_attachment=True,
            download_name='Template_Import_Mahasiswa.xlsx'
        )
    
    except Exception as e:
        logger.error(f"Error generating template: {str(e)}")
        return jsonify({'error': str(e)}), 500

# ========== HEALTH CHECK ==========

@app.route('/health', methods=['GET'])
def health():
    """Health check endpoint"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()}), 200

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    logger.error(f"Internal server error: {str(error)}")
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False') == 'True'
    logger.info(f"Starting Flask app on port {port} (debug={debug})")
    app.run(debug=debug, host='0.0.0.0', port=port)
