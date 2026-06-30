#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import landscape, A5
from reportlab.lib.units import cm, mm
from reportlab.pdfgen import canvas
from reportlab.lib.colors import HexColor, black, white
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Paragraph
from datetime import datetime
import os
from pathlib import Path

class PDFGenerator:
    """Generator untuk membuat PDF KTM"""
    
    def __init__(self, output_dir='output'):
        self.output_dir = output_dir
        Path(output_dir).mkdir(exist_ok=True)
    
    def generate_ktm(self, mahasiswa_data, filename=None):
        """
        Generate PDF KTM dari data mahasiswa
        
        Args:
            mahasiswa_data (dict): Data mahasiswa dengan keys: nim, nama, prodi
            filename (str): Nama file output (jika None, menggunakan NIM)
        
        Returns:
            str: Path ke file PDF yang dibuat
        """
        if filename is None:
            filename = f"KTM_{mahasiswa_data['nim']}.pdf"
        
        output_path = os.path.join(self.output_dir, filename)
        
        # Ukuran KTM standar (landscape A5)
        width, height = landscape(A5)
        
        c = canvas.Canvas(output_path, pagesize=landscape(A5))
        
        # Background - warna biru
        c.setFillColor(HexColor('#1e40af'))
        c.rect(0, 0, width, height, fill=1, stroke=0)
        
        # Border
        c.setStrokeColor(HexColor('#fbbf24'))
        c.setLineWidth(2)
        c.rect(0.5*cm, 0.5*cm, width - 1*cm, height - 1*cm)
        
        # Header
        c.setFillColor(white)
        c.setFont('Helvetica-Bold', 16)
        c.drawCentredString(width/2, height - 1.5*cm, 'KARTU TANDA MAHASISWA')
        
        c.setFont('Helvetica', 10)
        c.drawCentredString(width/2, height - 2*cm, 'UNIVERSITAS PENDIDIKAN')
        
        # Garis pemisah
        c.setStrokeColor(HexColor('#fbbf24'))
        c.setLineWidth(1)
        c.line(1*cm, height - 2.3*cm, width - 1*cm, height - 2.3*cm)
        
        # Foto placeholder
        c.setFillColor(white)
        c.rect(1.5*cm, height - 4*cm, 2.5*cm, 3*cm, fill=1)
        c.setFillColor(black)
        c.setFont('Helvetica', 8)
        c.drawCentredString(2.75*cm, height - 3.5*cm, '[FOTO]')
        
        # Data Mahasiswa
        data_x = 4.5*cm
        data_y = height - 2.8*cm
        line_height = 0.5*cm
        
        c.setFillColor(white)
        c.setFont('Helvetica', 9)
        
        # NIM
        c.drawString(data_x, data_y, 'NIM')
        c.drawString(data_x + 2*cm, data_y, ':')
        c.setFont('Helvetica-Bold', 9)
        c.drawString(data_x + 2.5*cm, data_y, mahasiswa_data['nim'])
        
        # Nama
        c.setFont('Helvetica', 9)
        data_y -= line_height
        c.drawString(data_x, data_y, 'Nama')
        c.drawString(data_x + 2*cm, data_y, ':')
        c.setFont('Helvetica-Bold', 9)
        c.drawString(data_x + 2.5*cm, data_y, mahasiswa_data['nama'])
        
        # Program Studi
        c.setFont('Helvetica', 9)
        data_y -= line_height
        c.drawString(data_x, data_y, 'Program Studi')
        c.drawString(data_x + 2*cm, data_y, ':')
        c.setFont('Helvetica-Bold', 9)
        c.drawString(data_x + 2.5*cm, data_y, mahasiswa_data['prodi'])
        
        # Tanggal Lahir (jika ada)
        if mahasiswa_data.get('tanggal_lahir'):
            c.setFont('Helvetica', 9)
            data_y -= line_height
            c.drawString(data_x, data_y, 'Tgl. Lahir')
            c.drawString(data_x + 2*cm, data_y, ':')
            c.setFont('Helvetica-Bold', 9)
            c.drawString(data_x + 2.5*cm, data_y, mahasiswa_data['tanggal_lahir'])
        
        # Footer - Tanggal cetak
        c.setFont('Helvetica', 8)
        c.drawString(1.5*cm, 0.7*cm, f"Dicetak: {datetime.now().strftime('%d/%m/%Y %H:%M')}")
        
        c.save()
        return output_path
