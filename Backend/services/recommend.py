import json
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models.product import SanPham
from models.product_embed import SanPhamEmbed
from models.interaction import TuongTac
from .embed_service import ProductEmbedding
from models.database import db
from .evaluation import RecommendationEvaluator
from models.orders import DonHang
from models.order_item import SanPhamTrongDonHang
from datetime import datetime, timedelta

class RecommendationService:
    def __init__(self):
        self.embedding_service = ProductEmbedding()
        self.evaluator = RecommendationEvaluator()
    
    def get_product_embedding(self, product_id):
        """Lấy vector nhúng của sản phẩm từ cơ sở dữ liệu"""
        embed_record = SanPhamEmbed.query.filter_by(ProductID=product_id).first()
        if not embed_record:
            return None
        return np.array(json.loads(embed_record.Embedding))
    
    def recommend_similar_products(self, product_id, top_n=5, use_hybrid=False):
        """Đề xuất các sản phẩm tương tự dựa trên sản phẩm đã cho"""
        # Lấy embedding của sản phẩm gốc
        source_embedding = self.get_product_embedding(product_id)
        if source_embedding is None:
            return []
        
        # Lấy tất cả các sản phẩm và embedding
        all_embeds = SanPhamEmbed.query.all()
        products = []
        embeddings = []
        
        for embed in all_embeds:
            if embed.ProductID != product_id:  # Không đề xuất sản phẩm gốc
                embedding = np.array(json.loads(embed.Embedding))
                embeddings.append(embedding)
                products.append(embed.ProductID)
        
        if not embeddings:
            return []
        
        # Tính toán độ tương đồng cosine
        embeddings = np.array(embeddings)
        similarities = cosine_similarity([source_embedding], embeddings)[0]
        
        # Sử dụng hybrid scoring nếu được yêu cầu
        if use_hybrid:
            # Lấy thông tin sản phẩm gốc
            source_product = SanPham.query.get(product_id)
            
            # Điều chỉnh điểm dựa trên thông tin sản phẩm
            adjusted_similarities = similarities.copy()
            
            for i, prod_id in enumerate(products):
                product = SanPham.query.get(prod_id)
                if product:
                    # Tăng điểm cho cùng nhãn hàng
                    if product.NhanHang == source_product.NhanHang:
                        adjusted_similarities[i] += 0.05
                    
                    # Tăng điểm cho cùng danh mục
                    if hasattr(product, 'Loai') and hasattr(source_product, 'Loai'):
                        if product.Loai == source_product.Loai:
                            adjusted_similarities[i] += 0.1
            
            # Sắp xếp lại với điểm đã điều chỉnh
            product_similarity = list(zip(products, adjusted_similarities))
        else:
            # Sắp xếp theo độ tương đồng cosine
            product_similarity = list(zip(products, similarities))
        
        product_similarity.sort(key=lambda x: x[1], reverse=True)
        
        # Lấy top N sản phẩm tương tự nhất
        top_products = product_similarity[:top_n]
        
        # Lấy thông tin chi tiết của sản phẩm
        result = []
        for prod_id, similarity in top_products:
            product = SanPham.query.get(prod_id)
            if product:
                result.append({
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'NhanHang': product.NhanHang,
                    'Gia': float(product.Gia),
                    'HinhAnh': product.HinhAnh,
                    'Similarity': float(similarity)
                })
        
        return result
    
    def recommend_for_user(self, user_id, top_n=5, evaluate=False):
        """Đề xuất sản phẩm cho người dùng dựa trên lịch sử tương tác"""
        # Lấy các sản phẩm người dùng đã xem
        user_interactions = TuongTac.query.filter_by(UserID=user_id).order_by(TuongTac.InteractionTime.desc()).all()
        
        if not user_interactions:
            # Nếu không có tương tác, trả về các sản phẩm phổ biến
            recommendations = self.get_popular_products(top_n)
            if not evaluate:
                return recommendations
            else:
                # Không có tương tác, không thể đánh giá
                return {
                    'recommendations': recommendations,
                    'metrics': {
                        'ndcg': 0,
                        'precision': 0,
                        'relevance_scores': [0] * len(recommendations)
                    }
                }
        
        # Phân loại tương tác theo loại
        cart_items = [i for i in user_interactions if i.InteractionType == 'cart']
        wishlist_items = [i for i in user_interactions if i.InteractionType == 'wishlist']
        viewed_items = [i for i in user_interactions if i.InteractionType == 'view']
        
        # Ưu tiên theo loại tương tác (giỏ hàng > wishlist > xem)
        source_items = cart_items or wishlist_items or viewed_items
        recent_product_id = source_items[0].ProductID
        
        # Đề xuất sản phẩm tương tự với sản phẩm gần đây nhất, sử dụng hybrid scoring
        recommendations = self.recommend_similar_products(recent_product_id, top_n, use_hybrid=True)
        
        # Nếu không yêu cầu đánh giá, trả về kết quả trực tiếp
        if not evaluate:
            return recommendations
        
        # Nếu yêu cầu đánh giá, tính toán các metrics
        product_ids = [rec['ProductID'] for rec in recommendations]
        
        # Lấy điểm liên quan cho các sản phẩm được đề xuất
        relevance_scores = self.evaluator.get_relevance_scores(user_id, product_ids)
        
        # Tính NDCG
        ndcg = self.evaluator.calculate_ndcg(relevance_scores)
        
        # Tính Precision - coi sản phẩm có điểm liên quan >= 0.2 là phù hợp
        relevant_items = [product_ids[i] for i, score in enumerate(relevance_scores) if score >= 0.2]
        precision = self.evaluator.calculate_precision(relevant_items, product_ids)
        
        # Trả về kết quả kèm metrics
        return {
            'recommendations': recommendations,
            'metrics': {
                'ndcg': ndcg,
                'precision': precision,
                'relevance_scores': relevance_scores
            }
        }
    
    def get_popular_products(self, top_n=5):
        """Lấy các sản phẩm phổ biến nhất dựa trên số lượng tương tác"""
        popular_products = TuongTac.query.with_entities(
            TuongTac.ProductID, 
            db.func.count(TuongTac.InteractionID).label('interaction_count')
        ).group_by(TuongTac.ProductID).order_by(
            db.text('interaction_count DESC')
        ).limit(top_n).all()
        
        result = []
        for prod_id, _ in popular_products:
            product = SanPham.query.get(prod_id)
            if product:
                result.append({
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'NhanHang': product.NhanHang,
                    'Gia': float(product.Gia),
                    'HinhAnh': product.HinhAnh
                })
        
        return result
    
    def get_bestseller_products(self, top_n=5, days=30):
       

        # Tính ngày bắt đầu để lọc trong khoảng thời gian xác định
        start_date = datetime.now() - timedelta(days=days)
        
        # Truy vấn lấy sản phẩm bán chạy trong thời gian xác định
        bestsellers = db.session.query(
            SanPhamTrongDonHang.ProductID,
            db.func.sum(SanPhamTrongDonHang.SoLuong).label('total_sold')
        ).join(
            DonHang, SanPhamTrongDonHang.OrderID == DonHang.OrdersID
        ).filter(
            DonHang.NgayDat >= start_date,
            DonHang.TrangThai == 'completed'  # Chỉ tính các đơn hàng đã hoàn thành
        ).group_by(
            SanPhamTrongDonHang.ProductID
        ).order_by(
            db.text('total_sold DESC')
        ).limit(top_n).all()
        
        result = []
        for prod_id, total_sold in bestsellers:
            product = SanPham.query.get(prod_id)
            if product:
                result.append({
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'NhanHang': product.NhanHang,
                    'Gia': float(product.Gia),
                    'HinhAnh': product.HinhAnh,
                    'TotalSold': total_sold
                })
        
        # Nếu không có dữ liệu bán hàng, sử dụng sản phẩm phổ biến
        if not result:
            popular_products = self.get_popular_products(top_n)
            return [
                {**product, 'TotalSold': 0} 
                for product in popular_products
            ]
            
        return result
    

    