from .database import db

class Cart(db.Model):
    __tablename__ = 'Cart'
    CartID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('NguoiDung.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), nullable=False)
    SoLuong = db.Column(db.Integer, nullable=False)
    NgayThem = db.Column(db.DateTime, default=db.func.current_timestamp())

    # Quan hệ với bảng NguoiDung
    user = db.relationship('NguoiDung', backref='cart_items', lazy=True)
    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='cart_items', lazy=True)