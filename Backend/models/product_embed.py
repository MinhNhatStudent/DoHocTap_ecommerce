from .database import db

class SanPhamEmbed(db.Model):
    __tablename__ = 'SanPhamEmbed'
    EmbedID = db.Column(db.Integer, primary_key=True)
    ProductID = db.Column(db.Integer, db.ForeignKey('SanPham.ProductID'), nullable=False)
    Embedding = db.Column(db.Text, nullable=False)  # Lưu vector nhúng dưới dạng chuỗi JSON
    UpdatedAt = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    # Quan hệ với bảng SanPham
    product = db.relationship('SanPham', backref='embeddings', lazy=True)