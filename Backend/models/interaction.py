from .database import db

class TuongTac(db.Model):
    __tablename__ = 'TuongTac'
    InteractionID = db.Column(db.Integer, primary_key=True)
    GhiChu = db.Column(db.Text)
    UserID = db.Column(db.Integer, db.ForeignKey('NguoiDung.UserID'), nullable=False)
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), nullable=False)
    InteractionType = db.Column(db.Enum('view', 'cart', 'wishlist'), nullable=False)
    Rating = db.Column(db.SmallInteger, nullable=True)  # Giá trị từ 1 đến 5
    InteractionTime = db.Column(db.DateTime, default=db.func.current_timestamp())
    SoLanXem = db.Column(db.Integer, default=1)
    ThoiGianXem = db.Column(db.Integer, default=0)

    # Quan hệ với bảng NguoiDung
    user = db.relationship('NguoiDung', backref='interactions', lazy=True)
    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='interactions', lazy=True)