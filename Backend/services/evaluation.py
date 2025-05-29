import numpy as np
import math
from models.interaction import TuongTac
from models.database import db

class RecommendationEvaluator:
    @staticmethod
    def calculate_dcg(relevance_scores):
        """Tính Discounted Cumulative Gain (DCG)"""
        dcg = 0
        for i, rel in enumerate(relevance_scores):
            # Sử dụng công thức: DCG = Σ(rel_i / log2(i+2))
            # i+2 vì index bắt đầu từ 0, và log2(1) = 0
            dcg += rel / math.log2(i + 2)
        return dcg

    @staticmethod
    def calculate_ndcg(relevance_scores):
        """Tính Normalized Discounted Cumulative Gain (NDCG)"""
        dcg = RecommendationEvaluator.calculate_dcg(relevance_scores)
        
        # Sắp xếp các điểm liên quan theo thứ tự giảm dần để tính IDCG
        ideal_scores = sorted(relevance_scores, reverse=True)
        idcg = RecommendationEvaluator.calculate_dcg(ideal_scores)
        
        # Tránh chia cho 0
        if idcg == 0:
            return 0
            
        return dcg / idcg

    @staticmethod
    def calculate_precision(relevant_items, recommended_items):
        """Tính Precision của các đề xuất"""
        if not recommended_items:
            return 0
            
        # Số lượng mục liên quan trong các đề xuất
        hits = sum(1 for item in recommended_items if item in relevant_items)
        return hits / len(recommended_items)

    @staticmethod
    def get_relevance_scores(user_id, recommended_product_ids):
        """Lấy điểm liên quan dựa trên tương tác người dùng với sản phẩm"""
        relevance_scores = []
        
        for product_id in recommended_product_ids:
            # Tìm tương tác của người dùng với sản phẩm này
            interactions = TuongTac.query.filter_by(
                UserID=user_id, 
                ProductID=product_id
            ).all()
            
            if not interactions:
                # Không có tương tác, điểm liên quan = 0
                relevance_scores.append(0)
                continue
                
            # Tính điểm liên quan dựa trên loại tương tác và đánh giá
            score = 0
            
            # Ưu tiên theo đánh giá (nếu có)
            ratings = [i.Rating for i in interactions if i.Rating is not None]
            if ratings:
                # Chuẩn hóa đánh giá về thang 0-1
                avg_rating = sum(ratings) / len(ratings)
                score = max(score, avg_rating / 5.0)
            
            # Tăng điểm cho tương tác giỏ hàng (ưu tiên cao)
            cart_interactions = sum(1 for i in interactions if i.InteractionType == 'cart')
            if cart_interactions > 0:
                score = max(score, 0.8)
            
            # Tăng điểm cho tương tác wishlist (ưu tiên trung bình)
            wishlist_interactions = sum(1 for i in interactions if i.InteractionType == 'wishlist')
            if wishlist_interactions > 0:
                score = max(score, 0.5)
            
            # Tăng điểm cho tương tác xem (ưu tiên thấp)
            view_interactions = sum(1 for i in interactions if i.InteractionType == 'view')
            if view_interactions > 0:
                score = max(score, 0.2)
            
            relevance_scores.append(score)
            
        return relevance_scores