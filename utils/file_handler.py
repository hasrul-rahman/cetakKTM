#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from pathlib import Path
from werkzeug.utils import secure_filename
from PIL import Image
import io

ALLOWED_IMAGE_EXTENSIONS = {'jpg', 'jpeg', 'png', 'gif', 'bmp'}
ALLOWED_EXCEL_EXTENSIONS = {'xlsx', 'xls'}
MAX_FILE_SIZE = 500 * 1024  # 500 KB

class FileHandler:
    def __init__(self, upload_dir='uploads'):
        self.upload_dir = upload_dir
        self.foto_dir = os.path.join(upload_dir, 'foto')
        self.background_dir = os.path.join(upload_dir, 'background')
        
        Path(self.foto_dir).mkdir(parents=True, exist_ok=True)
        Path(self.background_dir).mkdir(parents=True, exist_ok=True)
    
    def validate_image_file(self, file):
        """Validasi file gambar"""
        if not file or file.filename == '':
            return False, 'File tidak dipilih'
        
        # Check file extension
        file_ext = file.filename.rsplit('.', 1)[-1].lower()
        if file_ext not in ALLOWED_IMAGE_EXTENSIONS:
            return False, f'Format file tidak didukung. Gunakan: {ALLOWED_IMAGE_EXTENSIONS}'
        
        # Check file size
        file.seek(0, os.SEEK_END)
        file_size = file.tell()
        file.seek(0)
        
        if file_size > MAX_FILE_SIZE:
            return False, f'Ukuran file terlalu besar (max 500 KB, file Anda: {file_size / 1024 / 1024:.2f} MB)'
        
        return True, None
    
    def save_student_photo(self, file, nim):
        """Simpan foto mahasiswa dengan compression"""
        is_valid, error = self.validate_image_file(file)
        if not is_valid:
            return None, error
        
        try:
            # Buka gambar dengan PIL untuk compression
            img = Image.open(file)
            
            # Convert RGBA to RGB jika perlu
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Resize jika terlalu besar (max 400x500)
            img.thumbnail((400, 500), Image.Resampling.LANCZOS)
            
            # Simpan dengan compression
            filename = f"{secure_filename(nim)}.jpg"
            filepath = os.path.join(self.foto_dir, filename)
            
            # Save with optimization
            img.save(filepath, 'JPEG', quality=85, optimize=True)
            
            return f'uploads/foto/{filename}', None
        
        except Exception as e:
            return None, f'Error memproses gambar: {str(e)}'
    
    def save_ktm_background(self, file):
        """Simpan background KTM dengan compression"""
        is_valid, error = self.validate_image_file(file)
        if not is_valid:
            return None, error
        
        try:
            img = Image.open(file)
            
            # Convert ke RGB
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Resize ke ukuran KTM (85.6mm x 53.98mm at 300dpi = 1012x639 pixels)
            img = img.resize((1012, 639), Image.Resampling.LANCZOS)
            
            filename = 'ktm_background.jpg'
            filepath = os.path.join(self.background_dir, filename)
            
            img.save(filepath, 'JPEG', quality=90, optimize=True)
            
            return f'uploads/background/{filename}', None
        
        except Exception as e:
            return None, f'Error memproses background: {str(e)}'
    
    def validate_excel_file(self, file):
        """Validasi file Excel"""
        if not file or file.filename == '':
            return False, 'File tidak dipilih'
        
        file_ext = file.filename.rsplit('.', 1)[-1].lower()
        if file_ext not in ALLOWED_EXCEL_EXTENSIONS:
            return False, f'Format file harus Excel (.xlsx atau .xls)'
        
        return True, None
    
    def delete_file(self, filepath):
        """Hapus file"""
        try:
            if filepath and os.path.exists(filepath):
                os.remove(filepath)
                return True
        except Exception as e:
            pass
        return False
