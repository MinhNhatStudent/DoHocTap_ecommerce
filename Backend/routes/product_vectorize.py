from flask import request
from flask_restx import Namespace, Resource, fields
from models.database import db
from services.recommend import RecommendationService
from services.embed_service import ProductEmbedding

# Tạo namespace
vectorize_ns = Namespace('vectorize', description='Product vectorization and recommendation APIs')

# Model cho sản phẩm tương tự (với điểm tương đồng)
similar_product_model = vectorize_ns.model('SimilarProduct', {
    'ProductID': fields.Integer(required=True, description='ID sản phẩm'),
    'Ten': fields.String(required=True, description='Tên sản phẩm'),
    'NhanHang': fields.String(required=True, description='Nhãn hàng'),
    'Gia': fields.Float(required=True, description='Giá sản phẩm'),
    'HinhAnh': fields.String(required=True, description='Đường dẫn hình ảnh'),
    'Similarity': fields.Float(required=True, description='Điểm tương đồng')
})

# Model cho sản phẩm thông thường
product_model = vectorize_ns.model('RecommendedProduct', {
    'ProductID': fields.Integer(required=True, description='ID sản phẩm'),
    'Ten': fields.String(required=True, description='Tên sản phẩm'),
    'NhanHang': fields.String(required=True, description='Nhãn hàng'),
    'Gia': fields.Float(required=True, description='Giá sản phẩm'),
    'HinhAnh': fields.String(required=True, description='Đường dẫn hình ảnh')
})

# Model cho metrics đánh giá
metrics_model = vectorize_ns.model('Metrics', {
    'ndcg': fields.Float(description='Normalized Discounted Cumulative Gain'),
    'precision': fields.Float(description='Precision của đề xuất'),
    'relevance_scores': fields.List(fields.Float, description='Điểm liên quan cho từng sản phẩm')
})

# Model cho đề xuất kèm metrics
recommend_with_metrics_model = vectorize_ns.model('RecommendWithMetrics', {
    'recommendations': fields.List(fields.Nested(similar_product_model), description='Danh sách sản phẩm đề xuất'),
    'metrics': fields.Nested(metrics_model)
})

# API cập nhật vector nhúng
@vectorize_ns.route('/update-embeddings')
class UpdateEmbeddings(Resource):
    @vectorize_ns.doc('update_embeddings')
    def post(self):
        """Cập nhật vector nhúng cho tất cả sản phẩm"""
        embedding_service = ProductEmbedding()
        # Truyền application context
        from flask import current_app
        embedding_service.update_all_embeddings(current_app)
        return {"message": "Đã cập nhật vector nhúng cho tất cả sản phẩm!"}, 200

# API cập nhật vector nhúng cho một sản phẩm cụ thể    
@vectorize_ns.route('/update-embedding/<int:product_id>')
@vectorize_ns.param('product_id', 'ID của sản phẩm cần cập nhật vector nhúng')
class UpdateProductEmbedding(Resource):
    @vectorize_ns.doc('update_product_embedding')
    def post(self, product_id):
        """Cập nhật vector nhúng cho một sản phẩm cụ thể"""
        from models.product import SanPham
        from models.product_embed import SanPhamEmbed
        from flask import current_app
        import json
        
        with current_app.app_context():
            # Lấy thông tin sản phẩm
            product = SanPham.query.get(product_id)
            if not product:
                return {"error": f"Không tìm thấy sản phẩm với ID {product_id}"}, 404
                
            # Tạo vector nhúng
            embedding_service = ProductEmbedding()
            embedding = embedding_service.embed_product(product)
            
            # Kiểm tra xem sản phẩm đã có embedding chưa
            existing_embed = SanPhamEmbed.query.filter_by(ProductID=product_id).first()
            
            if existing_embed:
                existing_embed.Embedding = json.dumps(embedding.tolist())
            else:
                new_embed = SanPhamEmbed(
                    ProductID=product_id,
                    Embedding=json.dumps(embedding.tolist())
                )
                db.session.add(new_embed)
            
            db.session.commit()
            
            return {"message": f"Đã cập nhật vector nhúng cho sản phẩm ID {product_id}"}, 200

    

# API lấy sản phẩm tương tự
@vectorize_ns.route('/similar/<int:product_id>')
@vectorize_ns.param('product_id', 'ID của sản phẩm')
class SimilarProducts(Resource):
    @vectorize_ns.doc('get_similar_products')
    @vectorize_ns.param('count', 'Số lượng sản phẩm tương tự', default=5)
    @vectorize_ns.marshal_list_with(similar_product_model)
    def get(self, product_id):
        """Lấy danh sách sản phẩm tương tự với sản phẩm đã cho"""
        count = int(request.args.get('count', 10))
        recommendation_service = RecommendationService()
        similar_products = recommendation_service.recommend_similar_products(product_id, count)
        return similar_products


# API lấy đề xuất cho người dùng
@vectorize_ns.route('/user/<int:user_id>')
@vectorize_ns.param('user_id', 'ID của người dùng')
class UserRecommendations(Resource):
    @vectorize_ns.doc('get_user_recommendations')
    @vectorize_ns.param('count', 'Số lượng sản phẩm đề xuất', default=5)
    @vectorize_ns.marshal_list_with(product_model)
    def get(self, user_id):
        """Lấy đề xuất sản phẩm cho người dùng dựa trên lịch sử tương tác"""
        count = int(request.args.get('count', 5))
        recommendation_service = RecommendationService()
        recommendations = recommendation_service.recommend_for_user(user_id, count)
        return recommendations
    


# API lấy sản phẩm phổ biến
@vectorize_ns.route('/popular')
class PopularProducts(Resource):
    @vectorize_ns.doc('get_popular_products')
    @vectorize_ns.param('count', 'Số lượng sản phẩm phổ biến', default=5)
    @vectorize_ns.marshal_list_with(product_model)
    def get(self):
        """Lấy danh sách sản phẩm phổ biến nhất"""
        count = int(request.args.get('count', 5))
        recommendation_service = RecommendationService()
        popular_products = recommendation_service.get_popular_products(count)
        return popular_products
    

# API lấy đề xuất cho người dùng kèm đánh giá
@vectorize_ns.route('/user/<int:user_id>/evaluate')
@vectorize_ns.param('user_id', 'ID của người dùng')
class UserRecommendationsWithEvaluation(Resource):
    @vectorize_ns.doc('get_user_recommendations_with_evaluation')
    @vectorize_ns.param('count', 'Số lượng sản phẩm đề xuất', default=5)
    @vectorize_ns.response(200, 'Thành công', recommend_with_metrics_model)
    def get(self, user_id):
        """Lấy đề xuất sản phẩm cho người dùng kèm theo đánh giá hiệu quả"""
        count = int(request.args.get('count', 10))
        recommendation_service = RecommendationService()
        recommendations_with_metrics = recommendation_service.recommend_for_user(
            user_id, count, evaluate=True
        )
        return recommendations_with_metrics
    

# Thêm vào cuối file

# API debug để kiểm tra tương tác của người dùng
@vectorize_ns.route('/debug/user/<int:user_id>/interactions')
@vectorize_ns.param('user_id', 'ID của người dùng')
class DebugUserInteractions(Resource):
    @vectorize_ns.doc('debug_user_interactions')
    def get(self, user_id):
        """Kiểm tra tương tác của người dùng"""
        from models.interaction import TuongTac
        
        interactions = TuongTac.query.filter_by(UserID=user_id).all()
        result = {
            'user_id': user_id,
            'interaction_count': len(interactions),
            'interactions': []
        }
        
        for i in interactions:
            result['interactions'].append({
                'id': i.InteractionID,
                'product_id': i.ProductID,
                'type': i.InteractionType,
                'time': i.InteractionTime.strftime('%Y-%m-%d %H:%M:%S') if i.InteractionTime else None
            })
            
        return result

# API để kiểm tra chi tiết metrics
@vectorize_ns.route('/debug/metrics/<int:user_id>')
@vectorize_ns.param('user_id', 'ID của người dùng')
class DebugMetrics(Resource):
    @vectorize_ns.doc('debug_metrics')
    @vectorize_ns.param('count', 'Số lượng sản phẩm đề xuất', default=5)
    def get(self, user_id):
        """Kiểm tra chi tiết tính toán metrics"""
        count = int(request.args.get('count', 5))
        recommendation_service = RecommendationService()
        
        # Lấy đề xuất
        recommendations = recommendation_service.recommend_for_user(user_id, count)
        product_ids = [r['ProductID'] for r in recommendations]
        
        # Kiểm tra tương tác với từng sản phẩm
        from models.interaction import TuongTac
        interactions_by_product = {}
        
        for pid in product_ids:
            interactions = TuongTac.query.filter_by(UserID=user_id, ProductID=pid).all()
            interactions_by_product[str(pid)] = {
                'count': len(interactions),
                'types': [i.InteractionType for i in interactions]
            }
        
        # Lấy điểm liên quan
        evaluator = recommendation_service.evaluator
        relevance_scores = evaluator.get_relevance_scores(user_id, product_ids)
        
        return {
            'user_id': user_id,
            'recommendations': product_ids,
            'relevance_scores': relevance_scores,
            'interactions_by_product': interactions_by_product,
            'ndcg': evaluator.calculate_ndcg(relevance_scores),
            'precision': evaluator.calculate_precision(
                [pid for i, pid in enumerate(product_ids) if relevance_scores[i] >= 0.5],
                product_ids
            )
        }

# API để thêm tương tác thử nghiệm
@vectorize_ns.route('/debug/add-test-interaction/<int:user_id>')
@vectorize_ns.param('user_id', 'ID của người dùng')
class AddTestInteraction(Resource):
    @vectorize_ns.doc('add_test_interaction')
    @vectorize_ns.param('product_id', 'ID sản phẩm (để trống sẽ dùng sản phẩm được đề xuất)', required=False)
    @vectorize_ns.param('type', 'Loại tương tác (cart/wishlist/view)', default='cart')
    def post(self, user_id):
        """Thêm tương tác thử nghiệm cho người dùng"""
        from datetime import datetime
        from models.interaction import TuongTac
        
        product_id = request.args.get('product_id')
        interaction_type = request.args.get('type', 'cart')
        
        if not product_id:
            # Lấy sản phẩm được đề xuất
            recommendation_service = RecommendationService()
            recommendations = recommendation_service.recommend_for_user(user_id, 1)
            if not recommendations:
                return {"error": "Không có sản phẩm được đề xuất"}, 400
            product_id = recommendations[0]['ProductID']
        
        # Tạo tương tác mới
        new_interaction = TuongTac(
            UserID=user_id,
            ProductID=product_id,
            InteractionType=interaction_type,
            InteractionTime=datetime.now()
        )
        db.session.add(new_interaction)
        db.session.commit()
        
        return {
            "message": f"Đã thêm tương tác {interaction_type} cho user {user_id} với sản phẩm {product_id}"
        }
    
    # API lấy sản phẩm bán chạy nhất
@vectorize_ns.route('/bestsellers')
class BestsellerProducts(Resource):
    @vectorize_ns.doc('get_bestseller_products')
    @vectorize_ns.param('count', 'Số lượng sản phẩm bán chạy', default=5)
    @vectorize_ns.param('days', 'Số ngày gần đây để tính', default=30)
    @vectorize_ns.marshal_with(vectorize_ns.model('BestsellerProduct', {
        'ProductID': fields.Integer(required=True),
        'Ten': fields.String(required=True),
        'NhanHang': fields.String(required=True),
        'Gia': fields.Float(required=True),
        'HinhAnh': fields.String(required=True),
        'TotalSold': fields.Integer(required=True, description='Tổng số lượng đã bán')
    }))
    def get(self):
        """Lấy danh sách sản phẩm bán chạy nhất"""
        count = int(request.args.get('count', 5))
        days = int(request.args.get('days', 30))
        recommendation_service = RecommendationService()
        bestsellers = recommendation_service.get_bestseller_products(count, days)
        return bestsellers