#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from reportlab.lib.pagesizes import landscape, A8
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
from io import BytesIO
from PIL import Image
import os

class PDFGenerator:
    def __init__(self):
        # KTM size: 85.6mm x 53.98mm (ISO/IEC 7810)
        # At 72 DPI: 217px x 137px, but we use higher quality
        self.card_width = 217  # points (85.6mm)
        self.card_height = 137  # points (53.98mm)
    
    def generate_ktm_bytes(self, mahasiswa_data, background_path=None, font_color='#000000'):
        """Generate KTM PDF dalam format bytes"""
        # Create PDF in memory
        pdf_buffer = BytesIO()
        
        # Use custom page size sesuai KTM
        page_size = (self.card_width, self.card_height)
        c = canvas.Canvas(pdf_buffer, pagesize=page_size)
        
        # Draw background jika ada
        if background_path and os.path.exists(background_path):
            try:
                img = Image.open(background_path)
                # Scale image ke ukuran KTM
                img = img.resize((self.card_width, self.card_height), Image.Resampling.LANCZOS)
                
                # Simpan temporary image
                temp_img_path = '/tmp/ktm_bg.jpg'
                img.save(temp_img_path)
                
                # Draw background image
                c.drawImage(temp_img_path, 0, 0, width=self.card_width, height=self.card_height)
            except:
                pass
        else:
            # Draw white background
            c.setFillColorRGB(1, 1, 1)
            c.rect(0, 0, self.card_width, self.card_height, fill=1)
        
        # Convert hex color ke RGB
        font_color = font_color.lstrip('#')
        r = int(font_color[0:2], 16) / 255
        g = int(font_color[2:4], 16) / 255
        b = int(font_color[4:6], 16) / 255
        c.setFillColorRGB(r, g, b)
        
        # Draw border
        c.setLineWidth(1)
        c.setStrokeColorRGB(r, g, b)
        c.rect(2, 2, self.card_width - 4, self.card_height - 4)
        
        # Draw text
        c.setFont('Helvetica-Bold', 7)
        c.drawString(8, self.card_height - 12, 'KARTU TANDA MAHASISWA')
        
        c.setFont('Helvetica', 6)
        y_pos = self.card_height - 25
        
        # NIM
        c.drawString(8, y_pos, f"NIM: {mahasiswa_data.get('nim', '')}")
        y_pos -= 8
        
        # Nama (split jika terlalu panjang)
        nama = mahasiswa_data.get('nama', '')
        if len(nama) > 25:
            c.drawString(8, y_pos, nama[:25])
            y_pos -= 6
            c.drawString(8, y_pos, nama[25:])
        else:
            c.drawString(8, y_pos, nama)
        y_pos -= 8
        
        # Prodi
        prodi = mahasiswa_data.get('prodi', '')
        if len(prodi) > 30:
            c.drawString(8, y_pos, prodi[:30])
            y_pos -= 6
            c.drawString(8, y_pos, prodi[30:])
        else:
            c.drawString(8, y_pos, prodi)
        y_pos -= 8
        
        # Tanggal Lahir
        if mahasiswa_data.get('tanggal_lahir'):
            c.drawString(8, y_pos, f"TTL: {mahasiswa_data.get('tanggal_lahir', '')}")
        
        # Draw foto jika ada
        foto_path = mahasiswa_data.get('foto_path')
        if foto_path and os.path.exists(foto_path):
            try:
                c.drawImage(foto_path, self.card_width - 45, y_pos - 35, width=40, height=50)
            except:
                pass
        
        c.save()
        pdf_buffer.seek(0)
        return pdf_buffer
