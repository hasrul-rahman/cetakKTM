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
from models.mahasiswa import Mahasiswa

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__, template_folder='templates', static_folder='static')
CORS(app)

# Initialize database and PDF generator
try:
    db = Database()
    pdf_gen = PDFGenerator()
    logger.info("Database and PDF generator initialized successfully")
except Exception as e:
    logger.error(f"Error initializing database: {str(e)}")
    raise

@app.route('/')
def index():
    """Render main page"""
    try:
        return render_template('index.html')
    except Exception as e:
        logger.error(f"Error rendering index: {str(e)}")
        return jsonify({'error': str(e)}), 500

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

@app.route('/api/ktm/generate', methods=['POST'])
def generate_pdf():
    """Generate KTM PDF"""
    try:
        data = request.get_json()
        mahasiswa_data = {
            'nim': data.get('nim', ''),
            'nama': data.get('nama', ''),
            'prodi': data.get('prodi', ''),
            'tanggal_lahir': data.get('tanggal_lahir', '')
        }
        
        if not all([mahasiswa_data['nim'], mahasiswa_data['nama'], mahasiswa_data['prodi']]):
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        # Generate PDF in memory
        pdf_buffer = pdf_gen.generate_ktm_bytes(mahasiswa_data)
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
            'tanggal_lahir': data.get('tanggal_lahir', '')
        }
        
        if not all([mahasiswa_data['nim'], mahasiswa_data['nama'], mahasiswa_data['prodi']]):
            return jsonify({'error': 'NIM, Nama, dan Prodi harus diisi'}), 400
        
        # Generate PDF in memory for preview
        pdf_buffer = pdf_gen.generate_ktm_bytes(mahasiswa_data)
        logger.info(f"PDF preview for NIM: {mahasiswa_data['nim']}")
        
        return send_file(
            pdf_buffer,
            mimetype='application/pdf'
        )
    
    except Exception as e:
        logger.error(f"Error previewing PDF: {str(e)}")
        return jsonify({'error': str(e)}), 500

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
