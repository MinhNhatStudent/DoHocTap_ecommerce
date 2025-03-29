from .database import db

class DonHang(db.Model):
    __tablename__ = 'DonHang'
    OrdersID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('NguoiDung.UserID'), nullable=False)
    TongTien = db.Column(db.Numeric(10, 2), nullable=False)
    NgayDat = db.Column(db.DateTime, default=db.func.current_timestamp())
    TrangThai = db.Column(db.Enum('pending', 'completed', 'cancelled'), default='pending')

    # Quan hệ với bảng NguoiDung
    user = db.relationship('NguoiDung', backref='orders', lazy=True)