from .database import db

class SanPhamTrongDonHang(db.Model):
    __tablename__ = 'SanPhamTrongDonHang'
    OrderItemID = db.Column(db.Integer, primary_key=True)
    OrderID = db.Column(db.Integer, db.ForeignKey('DonHang.OrdersID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), nullable=False)
    SoLuong = db.Column(db.Integer, nullable=False)
    GiaThanh = db.Column(db.Numeric(10, 2), nullable=False)

    # Quan hệ với bảng DonHang
    order = db.relationship('DonHang', backref='order_items', lazy=True)
    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='order_items', lazy=True)