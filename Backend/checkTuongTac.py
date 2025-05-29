import sys
import os

# Thêm thư mục gốc của dự án vào path để import
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import app Flask và các model
from app import app  # Đảm bảo bạn có file app.py với Flask app
from models.interaction import TuongTac

# Tạo ngữ cảnh ứng dụng để truy vấn database
with app.app_context():
    # Kiểm tra số lượng tương tác
    user_interactions = TuongTac.query.filter_by(UserID=4).all()
    print(f"Số lượng tương tác của user4: {len(user_interactions)}")
    
    # Xem chi tiết tương tác
    for i in user_interactions:
        print(f"ProductID: {i.ProductID}, Type: {i.InteractionType}")