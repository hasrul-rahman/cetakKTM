#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Mahasiswa:
    """Model class untuk data mahasiswa"""
    
    def __init__(self, nim, nama, prodi, tanggal_lahir='', alamat=''):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.tanggal_lahir = tanggal_lahir
        self.alamat = alamat
    
    def to_dict(self):
        """Mengkonversi objek ke dictionary"""
        return {
            'nim': self.nim,
            'nama': self.nama,
            'prodi': self.prodi,
            'tanggal_lahir': self.tanggal_lahir,
            'alamat': self.alamat
        }
    
    def __repr__(self):
        return f"Mahasiswa(nim={self.nim}, nama={self.nama}, prodi={self.prodi})"
