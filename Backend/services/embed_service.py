import json
import numpy as np
from sentence_transformers import SentenceTransformer
from .preprocess import TextPreprocessor
from models.product_embed import SanPhamEmbed
from models.database import db

class ProductEmbedding:
    def __init__(self, model_name='sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2'):
        self.model = SentenceTransformer(model_name)
        self.preprocessor = TextPreprocessor()
    
    def embed_text(self, text):
        """Tạo vector nhúng cho văn bản"""
        preprocessed_text = self.preprocessor.preprocess(text)
        if not preprocessed_text:
            return np.zeros(384)  # Trả về vector 0 nếu text rỗng
        embedding = self.model.encode(preprocessed_text)
        return embedding
    
    def embed_product(self, product):
        """Tạo vector nhúng cho sản phẩm từ mô tả và tiêu đề"""
        # Kết hợp tiêu đề và mô tả
        text = f"{product.Ten} {product.MoTa}"
        embedding = self.embed_text(text)
        return embedding
    
    def update_all_embeddings(self, app):
        """Cập nhật vector nhúng cho tất cả sản phẩm"""
        from models.product import SanPham
        
        with app.app_context():
            products = SanPham.query.all()
            batch_size = 50  # Xử lý theo lô 50 sản phẩm
            
            for i in range(0, len(products), batch_size):
                batch = products[i:i+batch_size]
                for product in batch:
                    embedding = self.embed_product(product)
                    
                    # Kiểm tra xem sản phẩm đã có embedding chưa
                    existing_embed = SanPhamEmbed.query.filter_by(ProductID=product.ProductID).first()
                    
                    if existing_embed:
                        existing_embed.Embedding = json.dumps(embedding.tolist())
                    else:
                        new_embed = SanPhamEmbed(
                            ProductID=product.ProductID,
                            Embedding=json.dumps(embedding.tolist())
                        )
                        db.session.add(new_embed)
                    
                    print(f"Đã nhúng sản phẩm: {product.Ten}")
                
                # Commit sau mỗi batch
                db.session.commit()
                print(f"Đã xử lý {i+len(batch)}/{len(products)} sản phẩm")
            
            print("Hoàn thành cập nhật vector nhúng cho tất cả sản phẩm!")