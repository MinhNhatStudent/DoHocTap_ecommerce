from .database import db

class SanPham_TuKhoa(db.Model):
    __tablename__ = 'SanPham_TuKhoa'
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), primary_key=True)
    TuKhoa = db.Column(db.String(50), primary_key=True)

    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='keywords', lazy=True)