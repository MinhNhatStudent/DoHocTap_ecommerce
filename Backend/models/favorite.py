from .database import db

class YeuThich(db.Model):
    __tablename__ = 'YeuThich'
    UserID = db.Column(db.Integer, db.ForeignKey('NguoiDung.UserID'), primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), primary_key=True)
    NgayThem = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Quan hệ với bảng NguoiDung
    user = db.relationship('NguoiDung', backref='favorites', lazy=True)
    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='favorited_by', lazy=True)