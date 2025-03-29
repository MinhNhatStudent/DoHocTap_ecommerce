from .database import db

class SanPham(db.Model):
    __tablename__ = 'SanPham'
    ProductID = db.Column(db.Integer, primary_key=True)
    Ten = db.Column(db.String(100), nullable=False)
    Loai = db.Column(db.String(50), nullable=False)
    MoTa = db.Column(db.Text)
    Gia = db.Column(db.Numeric(10, 2), nullable=False)
    SoLuong = db.Column(db.Integer, nullable=False)
    HinhAnh = db.Column(db.String(255))