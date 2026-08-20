#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sqlite3
import os
from pathlib import Path

class Database:
    def __init__(self, db_path='data/ktm.db'):
        self.db_path = db_path
        Path('data').mkdir(exist_ok=True)
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
                foto BLOB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_connection(self):
        """Mendapatkan koneksi ke database"""
        return sqlite3.connect(self.db_path)
    
    def insert_mahasiswa(self, nim, nama, prodi, tanggal_lahir='', alamat='', foto=None):
        """Menambahkan data mahasiswa baru"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute('''
                INSERT INTO mahasiswa (nim, nama, prodi, tanggal_lahir, alamat, foto)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nim, nama, prodi, tanggal_lahir, alamat, foto))
            
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
            SELECT nim, nama, prodi, tanggal_lahir, alamat, foto 
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
                'foto': result[5]
            }
        return None
    
    def get_all_mahasiswa(self):
        """Mendapatkan semua data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('SELECT nim, nama, prodi FROM mahasiswa ORDER BY created_at DESC')
        results = cursor.fetchall()
        conn.close()
        
        return [{
            'nim': row[0],
            'nama': row[1],
            'prodi': row[2]
        } for row in results]
    
    def update_mahasiswa(self, nim, nama, prodi, tanggal_lahir='', alamat=''):
        """Memperbarui data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('''
            UPDATE mahasiswa 
            SET nama = ?, prodi = ?, tanggal_lahir = ?, alamat = ?
            WHERE nim = ?
        ''', (nama, prodi, tanggal_lahir, alamat, nim))
        
        conn.commit()
        conn.close()
    
    def delete_mahasiswa(self, nim):
        """Menghapus data mahasiswa"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute('DELETE FROM mahasiswa WHERE nim = ?', (nim,))
        conn.commit()
        conn.close()
