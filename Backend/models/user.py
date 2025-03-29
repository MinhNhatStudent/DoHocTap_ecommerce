from .database import db

class NguoiDung(db.Model):
    __tablename__ = 'NguoiDung'
    UserID = db.Column(db.Integer, primary_key=True)
    Ten = db.Column(db.String(100), nullable=False)
    Email = db.Column(db.String(100), unique=True, nullable=False)
    Pass = db.Column(db.String(255), nullable=False)
    Role = db.Column(db.Enum('user', 'admin'), default='user')
    Age = db.Column(db.Integer)
    CreatedAt = db.Column(db.DateTime, default=db.func.current_timestamp())