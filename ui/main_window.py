#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QLabel, QLineEdit, QPushButton, QTextEdit, QMessageBox,
    QTabWidget, QTableWidget, QTableWidgetItem, QFileDialog
)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QFont, QIcon
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import Database
from utils.pdf_generator import PDFGenerator
from models.mahasiswa import Mahasiswa

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.db = Database()
        self.pdf_gen = PDFGenerator()
        self.current_mahasiswa = None
        self.init_ui()
    
    def init_ui(self):
        """Inisialisasi interface"""
        self.setWindowTitle('Aplikasi Cetak KTM - Kartu Tanda Mahasiswa')
        self.setGeometry(100, 100, 900, 600)
        
        # Tab Widget
        tabs = QTabWidget()
        
        # Tab 1: Cetak KTM
        tab_print = self.create_print_tab()
        tabs.addTab(tab_print, 'Cetak KTM')
        
        # Tab 2: Data Mahasiswa
        tab_data = self.create_data_tab()
        tabs.addTab(tab_data, 'Kelola Data Mahasiswa')
        
        self.setCentralWidget(tabs)
    
    def create_print_tab(self):
        """Buat tab untuk mencetak KTM"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Judul
        title = QLabel('CETAK KTM (KARTU TANDA MAHASISWA)')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Input NIM
        layout.addLayout(self.create_input_nim_layout())
        
        # Data Display
        layout.addLayout(self.create_data_display_layout())
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.btn_preview = QPushButton('Preview KTM')
        self.btn_preview.setEnabled(False)
        self.btn_preview.clicked.connect(self.preview_ktm)
        button_layout.addWidget(self.btn_preview)
        
        self.btn_print = QPushButton('Cetak PDF')
        self.btn_print.setEnabled(False)
        self.btn_print.clicked.connect(self.print_pdf)
        button_layout.addWidget(self.btn_print)
        
        self.btn_clear = QPushButton('Hapus')
        self.btn_clear.clicked.connect(self.clear_form)
        button_layout.addWidget(self.btn_clear)
        
        layout.addLayout(button_layout)
        layout.addStretch()
        
        tab.setLayout(layout)
        return tab
    
    def create_input_nim_layout(self):
        """Layout untuk input NIM"""
        layout = QHBoxLayout()
        
        label = QLabel('Input NIM:')
        label.setFont(QFont('Arial', 10))
        layout.addWidget(label)
        
        self.input_nim = QLineEdit()
        self.input_nim.setPlaceholderText('Masukkan NIM Mahasiswa...')
        self.input_nim.returnPressed.connect(self.search_mahasiswa)
        layout.addWidget(self.input_nim)
        
        self.btn_search = QPushButton('Cari')
        self.btn_search.clicked.connect(self.search_mahasiswa)
        layout.addWidget(self.btn_search)
        
        return layout
    
    def create_data_display_layout(self):
        """Layout untuk menampilkan data"""
        layout = QVBoxLayout()
        
        # NIM
        nim_layout = QHBoxLayout()
        nim_layout.addWidget(QLabel('NIM:'))
        self.label_nim = QLabel('-')
        self.label_nim.setFont(QFont('Arial', 10, QFont.Bold))
        nim_layout.addWidget(self.label_nim)
        nim_layout.addStretch()
        layout.addLayout(nim_layout)
        
        # Nama
        nama_layout = QHBoxLayout()
        nama_layout.addWidget(QLabel('Nama:'))
        self.label_nama = QLabel('-')
        self.label_nama.setFont(QFont('Arial', 10, QFont.Bold))
        nama_layout.addWidget(self.label_nama)
        nama_layout.addStretch()
        layout.addLayout(nama_layout)
        
        # Prodi
        prodi_layout = QHBoxLayout()
        prodi_layout.addWidget(QLabel('Program Studi:'))
        self.label_prodi = QLabel('-')
        self.label_prodi.setFont(QFont('Arial', 10, QFont.Bold))
        prodi_layout.addWidget(self.label_prodi)
        prodi_layout.addStretch()
        layout.addLayout(prodi_layout)
        
        return layout
    
    def create_data_tab(self):
        """Buat tab untuk mengelola data mahasiswa"""
        tab = QWidget()
        layout = QVBoxLayout()
        
        # Judul
        title = QLabel('KELOLA DATA MAHASISWA')
        title.setFont(QFont('Arial', 14, QFont.Bold))
        layout.addWidget(title)
        
        # Form tambah data
        form_layout = QHBoxLayout()
        
        form_layout.addWidget(QLabel('NIM:'))
        self.form_nim = QLineEdit()
        form_layout.addWidget(self.form_nim)
        
        form_layout.addWidget(QLabel('Nama:'))
        self.form_nama = QLineEdit()
        form_layout.addWidget(self.form_nama)
        
        form_layout.addWidget(QLabel('Prodi:'))
        self.form_prodi = QLineEdit()
        form_layout.addWidget(self.form_prodi)
        
        btn_add = QPushButton('Tambah')
        btn_add.clicked.connect(self.add_mahasiswa)
        form_layout.addWidget(btn_add)
        
        layout.addLayout(form_layout)
        
        # Tabel data
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(['NIM', 'Nama', 'Program Studi'])
        self.table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(self.table)
        
        # Tombol refresh
        btn_refresh = QPushButton('Refresh Data')
        btn_refresh.clicked.connect(self.refresh_table)
        layout.addWidget(btn_refresh)
        
        tab.setLayout(layout)
        self.refresh_table()
        
        return tab
    
    def search_mahasiswa(self):
        """Mencari data mahasiswa berdasarkan NIM"""
        nim = self.input_nim.text().strip()
        
        if not nim:
            QMessageBox.warning(self, 'Peringatan', 'Silakan masukkan NIM!')
            return
        
        data = self.db.search_mahasiswa_by_nim(nim)
        
        if data:
            self.current_mahasiswa = data
            self.label_nim.setText(data['nim'])
            self.label_nama.setText(data['nama'])
            self.label_prodi.setText(data['prodi'])
            self.btn_preview.setEnabled(True)
            self.btn_print.setEnabled(True)
        else:
            QMessageBox.warning(self, 'Tidak Ditemukan', f'Data mahasiswa dengan NIM {nim} tidak ditemukan!')
            self.clear_form()
    
    def preview_ktm(self):
        """Preview KTM"""
        if not self.current_mahasiswa:
            QMessageBox.warning(self, 'Peringatan', 'Silakan cari data mahasiswa terlebih dahulu!')
            return
        
        QMessageBox.information(self, 'Preview KTM', 
            f"NIM: {self.current_mahasiswa['nim']}\n"
            f"Nama: {self.current_mahasiswa['nama']}\n"
            f"Prodi: {self.current_mahasiswa['prodi']}")
    
    def print_pdf(self):
        """Cetak KTM ke PDF"""
        if not self.current_mahasiswa:
            QMessageBox.warning(self, 'Peringatan', 'Silakan cari data mahasiswa terlebih dahulu!')
            return
        
        try:
            filename = f"KTM_{self.current_mahasiswa['nim']}.pdf"
            filepath = self.pdf_gen.generate_ktm(self.current_mahasiswa, filename)
            
            QMessageBox.information(self, 'Berhasil', f'KTM berhasil dicetak!\n\nFile tersimpan di: {filepath}')
            
            # Buka folder output
            os.startfile(self.pdf_gen.output_dir) if os.name == 'nt' else os.system(f'open {self.pdf_gen.output_dir}')
        
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'Gagal mencetak PDF: {str(e)}')
    
    def clear_form(self):
        """Menghapus form"""
        self.input_nim.clear()
        self.label_nim.setText('-')
        self.label_nama.setText('-')
        self.label_prodi.setText('-')
        self.current_mahasiswa = None
        self.btn_preview.setEnabled(False)
        self.btn_print.setEnabled(False)
    
    def add_mahasiswa(self):
        """Menambah data mahasiswa baru"""
        nim = self.form_nim.text().strip()
        nama = self.form_nama.text().strip()
        prodi = self.form_prodi.text().strip()
        
        if not nim or not nama or not prodi:
            QMessageBox.warning(self, 'Peringatan', 'Silakan isi semua field!')
            return
        
        if self.db.insert_mahasiswa(nim, nama, prodi):
            QMessageBox.information(self, 'Berhasil', 'Data mahasiswa berhasil ditambahkan!')
            self.form_nim.clear()
            self.form_nama.clear()
            self.form_prodi.clear()
            self.refresh_table()
        else:
            QMessageBox.warning(self, 'Gagal', f'NIM {nim} sudah terdaftar!')
    
    def refresh_table(self):
        """Refresh tabel data mahasiswa"""
        data = self.db.get_all_mahasiswa()
        self.table.setRowCount(0)
        
        for row, item in enumerate(data):
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(item['nim']))
            self.table.setItem(row, 1, QTableWidgetItem(item['nama']))
            self.table.setItem(row, 2, QTableWidgetItem(item['prodi']))
