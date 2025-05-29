from flask import Blueprint, jsonify, request
from services.recommend import RecommendationService



# Đây chỉ là một ví dụ về cách định nghĩa các route cho hệ thống gợi ý sản phẩm
# Để sử dụng chức năng recommendation, bạn hãy sử dụng qua file product_vectorize.py

recommend_bp = Blueprint('recommend_bp', __name__)
recommendation_service = RecommendationService()

@recommend_bp.route('/similar/<int:product_id>', methods=['GET'])
def get_similar_products(product_id):
    """Lấy các sản phẩm tương tự với sản phẩm đã cho"""
    count = request.args.get('count', 5, type=int)
    similar_products = recommendation_service.recommend_similar_products(product_id, count)
    return jsonify(similar_products)

@recommend_bp.route('/user/<int:user_id>', methods=['GET'])
def get_recommendations_for_user(user_id):
    """Lấy đề xuất sản phẩm cho người dùng"""
    count = request.args.get('count', 5, type=int)
    recommendations = recommendation_service.recommend_for_user(user_id, count)
    return jsonify(recommendations)

@recommend_bp.route('/popular', methods=['GET'])
def get_popular_products():
    """Lấy các sản phẩm phổ biến"""
    count = request.args.get('count', 5, type=int)
    popular_products = recommendation_service.get_popular_products(count)
    return jsonify(popular_products)