from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Mahasiswa(db.Model):
    __tablename__ = 'mahasiswa'
    nim = db.Column(db.String(64), primary_key=True)
    nama = db.Column(db.String(255), nullable=False)
    prodi = db.Column(db.String(128), nullable=False)
    # store filename only (e.g., "12345.jpg") — files are in static/photos/
    photo_path = db.Column(db.String(300), nullable=True)

    def photo_url(self):
        if self.photo_path:
            from flask import url_for
            return url_for('static', filename='photos/' + self.photo_path)
        return None