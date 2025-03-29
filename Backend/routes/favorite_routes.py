from flask_restx import Namespace, Resource, fields
from models.favorite import YeuThich
from models.product import SanPham
from models.database import db

# Tạo namespace cho Favorites
favorite_ns = Namespace('favorites', description='Favorite related operations')

# Định nghĩa model dữ liệu cho Swagger
favorite_model = favorite_ns.model('Favorite', {
    'UserID': fields.Integer(required=True, description='ID của người dùng'),
    'ProductID': fields.Integer(required=True, description='ID của sản phẩm')
})

@favorite_ns.route('/')
class FavoriteList(Resource):
    @favorite_ns.expect(favorite_model)
    @favorite_ns.doc('add_favorite')
    def post(self):
        """Thêm sản phẩm vào danh sách yêu thích"""
        data = favorite_ns.payload
        new_favorite = YeuThich(
            UserID=data['UserID'],
            ProductID=data['ProductID']
        )
        db.session.add(new_favorite)
        db.session.commit()
        return {'message': 'Sản phẩm đã được thêm vào danh sách yêu thích!', 'FavoriteID': new_favorite.FavoriteID}, 201

@favorite_ns.route('/<int:user_id>')
@favorite_ns.param('user_id', 'ID của người dùng')
class UserFavorites(Resource):
    @favorite_ns.doc('get_user_favorites')
    def get(self, user_id):
        """Lấy danh sách sản phẩm yêu thích của người dùng"""
        favorites = YeuThich.query.filter_by(UserID=user_id).all()
        result = []
        for favorite in favorites:
            product = SanPham.query.get(favorite.ProductID)
            if product:
                result.append({
                    'FavoriteID': favorite.FavoriteID,
                    'UserID': favorite.UserID,
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'Loai': product.Loai,
                    'Gia': float(product.Gia),
                    'HinhAnh': product.HinhAnh
                })
        return result

@favorite_ns.route('/delete/<int:favorite_id>')
@favorite_ns.param('favorite_id', 'ID của sản phẩm yêu thích')
class Favorite(Resource):
    @favorite_ns.doc('delete_favorite')
    def delete(self, favorite_id):
        """Xóa sản phẩm khỏi danh sách yêu thích"""
        favorite = YeuThich.query.get(favorite_id)
        if not favorite:
            return {'message': 'Sản phẩm yêu thích không tồn tại!'}, 404
        db.session.delete(favorite)
        db.session.commit()
        return {'message': 'Sản phẩm đã được xóa khỏi danh sách yêu thích!'}