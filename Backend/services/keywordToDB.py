import logging
from models.product_keywords import SanPham_TuKhoa
from models.database import db

# Cấu hình logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def save_keywords_to_db(product_keywords):
    """Lưu từ khóa vào bảng SanPham_TuKhoa với tối ưu hóa truy vấn và xử lý lỗi."""
    new_keywords = []
    
    try:
        for product in product_keywords:
            product_id = product['ProductID']
            
            # Lấy danh sách từ khóa hiện có dưới dạng set
            existing_keywords = set(
                row[0] for row in db.session.query(SanPham_TuKhoa.TuKhoa).filter_by(ProductID=product_id).all()
            )
            
            # Chỉ thêm các từ khóa chưa tồn tại
            for keyword in product['Keywords']:
                if keyword not in existing_keywords:
                    new_keywords.append(SanPham_TuKhoa(ProductID=product_id, TuKhoa=keyword))
        
        # Batch insert tất cả từ mới
        if new_keywords:
            db.session.bulk_save_objects(new_keywords)
            logging.info(f"Thêm {len(new_keywords)} từ khóa mới vào cơ sở dữ liệu.")
        
        # Commit một lần
        db.session.commit()
    except Exception as e:

        db.session.rollback()
        logging.error(f"Lỗi khi lưu từ khóa vào cơ sở dữ liệu: {e}")
        raise e