#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from pathlib import Path

class Database:
    def __init__(self, db_path='data/ktm.db'):
        self.db_path = db_path
        Path('data').mkdir(exist_ok=True)
        Path('uploads/foto').mkdir(parents=True, exist_ok=True)
        Path('uploads/background').mkdir(parents=True, exist_ok=True)
        self.init_database()
    
    def init_database(self):
        """Inisialisasi database dan buat tabel jika belum ada"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS mahasiswa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nim TEXT UNIQUE NOT NULL,
                nama TEXT NOT NULL,
                prodi TEXT NOT NULL,
                tanggal_lahir TEXT,
                alamat TEXT,
                foto_path TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS ktm_settings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                background_path TEXT,
                font_color TEXT DEFAULT '#000000',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Insert default background settings jika belum ada
        cursor.execute('SELECT COUNT(*) FROM ktm_settings')
        if cursor.fetchone()[0] == 0:
            cursor.execute('''
                INSERT INTO ktm_settings (background_path, font_color)
                VALUES (?, ?)
            ''', (None, '#000000'))
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Mendapatkan koneksi ke database"""
        return sqlite3.connect(self.db_path)
    
    def insert_mahasiswa(self, nim, nama, prodi, tanggal_lahir='', alamat='', foto_path=None):
        """Menambahkan data mahasiswa baru"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO mahasiswa (nim, nama, prodi, tanggal_lahir, alamat, foto_path)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nim, nama, prodi, tanggal_lahir, alamat, foto_path))
            
            conn.commit()
            conn.close()
            return True
        except sqlite3.IntegrityError:
            return False
    
    def search_mahasiswa_by_nim(self, nim):
        """Mencari data mahasiswa berdasarkan NIM"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            SELECT nim, nama, prodi, tanggal_lahir, alamat, foto_path
            FROM mahasiswa 
            WHERE nim = ?
        ''', (nim,))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'nim': result[0],
                'nama': result[1],
                'prodi': result[2],
                'tanggal_lahir': result[3] or '',
                'alamat': result[4] or '',
                'foto_path': result[5] or None
            }
        return None
    
    def get_all_mahasiswa(self):
        """Mendapatkan semua data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT nim, nama, prodi, foto_path FROM mahasiswa ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'nim': row[0],
            'nama': row[1],
            'prodi': row[2],
            'foto_path': row[3]
        } for row in results]
    
    def update_mahasiswa(self, nim, nama, prodi, tanggal_lahir='', alamat='', foto_path=None):
        """Memperbarui data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        if foto_path is None:
            cursor.execute('''
                UPDATE mahasiswa 
                SET nama = ?, prodi = ?, tanggal_lahir = ?, alamat = ?, updated_at = CURRENT_TIMESTAMP
                WHERE nim = ?
            ''', (nama, prodi, tanggal_lahir, alamat, nim))
        else:
            cursor.execute('''
                UPDATE mahasiswa 
                SET nama = ?, prodi = ?, tanggal_lahir = ?, alamat = ?, foto_path = ?, updated_at = CURRENT_TIMESTAMP
                WHERE nim = ?
            ''', (nama, prodi, tanggal_lahir, alamat, foto_path, nim))
        
        conn.commit()
        conn.close()
    
    def update_mahasiswa_foto(self, nim, foto_path):
        """Memperbarui foto mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mahasiswa 
            SET foto_path = ?, updated_at = CURRENT_TIMESTAMP
            WHERE nim = ?
        ''', (foto_path, nim))
        
        conn.commit()
        conn.close()
    
    def delete_mahasiswa(self, nim):
        """Menghapus data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM mahasiswa WHERE nim = ?', (nim,))
        conn.commit()
        conn.close()
    
    def get_ktm_settings(self):
        """Mendapatkan settings KTM"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT id, background_path, font_color FROM ktm_settings LIMIT 1')
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return {
                'id': result[0],
                'background_path': result[1],
                'font_color': result[2]
            }
        return None
    
    def update_ktm_background(self, background_path):
        """Memperbarui background KTM"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE ktm_settings 
            SET background_path = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (background_path,))
        
        conn.commit()
        conn.close()
    
    def update_ktm_font_color(self, font_color):
        """Memperbarui warna font KTM"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE ktm_settings 
            SET font_color = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = 1
        ''', (font_color,))
        
        conn.commit()
        conn.close()
    
    def insert_bulk_mahasiswa(self, mahasiswa_list):
        """Menambahkan data mahasiswa secara massal (dari Excel)"""
        conn = self.get_connection()
        cursor = conn.cursor()
        results = {'success': 0, 'failed': 0, 'errors': []}
        
        for idx, data in enumerate(mahasiswa_list, 1):
            try:
                nim = data.get('nim', '').strip()
                nama = data.get('nama', '').strip()
                prodi = data.get('prodi', '').strip()
                tanggal_lahir = data.get('tanggal_lahir', '').strip() or None
                alamat = data.get('alamat', '').strip() or None
                
                if not nim or not nama or not prodi:
                    results['failed'] += 1
                    results['errors'].append(f"Baris {idx}: NIM, Nama, atau Prodi kosong")
                    continue
                
                cursor.execute('''
                    INSERT INTO mahasiswa (nim, nama, prodi, tanggal_lahir, alamat)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nim, nama, prodi, tanggal_lahir, alamat))
                
                results['success'] += 1
            except sqlite3.IntegrityError:
                results['failed'] += 1
                results['errors'].append(f"Baris {idx}: NIM {data.get('nim')} sudah terdaftar")
            except Exception as e:
                results['failed'] += 1
                results['errors'].append(f"Baris {idx}: {str(e)}")
        
        conn.commit()
        conn.close()
        return results
