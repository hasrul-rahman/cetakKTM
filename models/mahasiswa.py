#!/usr/bin/env python3
# -*- coding: utf-8 -*-

class Mahasiswa:
    """Model untuk data mahasiswa"""
    
    def __init__(self, nim, nama, prodi, tanggal_lahir='', alamat='', foto_path=None):
        self.nim = nim
        self.nama = nama
        self.prodi = prodi
        self.tanggal_lahir = tanggal_lahir
        self.alamat = alamat
        self.foto_path = foto_path
    
    def to_dict(self):
        return {
            'nim': self.nim,
            'nama': self.nama,
            'prodi': self.prodi,
            'tanggal_lahir': self.tanggal_lahir,
            'alamat': self.alamat,
            'foto_path': self.foto_path
        }
    
    @staticmethod
    def from_dict(data):
        return Mahasiswa(
            nim=data.get('nim'),
            nama=data.get('nama'),
            prodi=data.get('prodi'),
            tanggal_lahir=data.get('tanggal_lahir', ''),
            alamat=data.get('alamat', ''),
            foto_path=data.get('foto_path')
        )
