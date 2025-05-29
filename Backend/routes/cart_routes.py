from flask_restx import Namespace, Resource, fields
from models.cart import Cart
from models.product import SanPham
from models.database import db

# Tạo namespace cho Cart
cart_ns = Namespace('cart', description='Cart related operations')

# Định nghĩa model dữ liệu cho Swagger
cart_model = cart_ns.model('Cart', {
    'UserID': fields.Integer(required=True, description='ID của người dùng'),
    'ProductID': fields.Integer(required=True, description='ID của sản phẩm'),
    'SoLuong': fields.Integer(required=True, description='Số lượng sản phẩm')
})

@cart_ns.route('/')
class CartList(Resource):
    @cart_ns.expect(cart_model)
    @cart_ns.doc('add_to_cart')
    def post(self):
        """Thêm sản phẩm vào giỏ hàng"""
        data = cart_ns.payload
        new_cart_item = Cart(
            UserID=data['UserID'],
            ProductID=data['ProductID'],
            SoLuong=data['SoLuong']
        )
        db.session.add(new_cart_item)
        db.session.commit()
        return {'message': 'Sản phẩm đã được thêm vào giỏ hàng!', 'CartID': new_cart_item.CartID}, 201

@cart_ns.route('/<int:user_id>')
@cart_ns.param('user_id', 'ID của người dùng')
class UserCart(Resource):
    @cart_ns.doc('get_user_cart')
    def get(self, user_id):
        """Lấy danh sách sản phẩm trong giỏ hàng của người dùng"""
        cart_items = Cart.query.filter_by(UserID=user_id).all()
        result = []
        for item in cart_items:
            product = SanPham.query.get(item.ProductID)
            if product:
                result.append({
                    'CartID': item.CartID,
                    'UserID': item.UserID,
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'NhanHang': product.NhanHang,
                    'Gia': float(product.Gia),
                    'SoLuong': item.SoLuong,
                    'HinhAnh': product.HinhAnh
                })
        return result

@cart_ns.route('/<int:cart_id>')
@cart_ns.param('cart_id', 'ID của sản phẩm trong giỏ hàng')
class CartItem(Resource):
    @cart_ns.expect(cart_model)
    @cart_ns.doc('update_cart_item')
    def put(self, cart_id):
        """Cập nhật số lượng sản phẩm trong giỏ hàng"""
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'message': 'Sản phẩm trong giỏ hàng không tồn tại!'}, 404
        data = cart_ns.payload
        cart_item.SoLuong = data['SoLuong']
        db.session.commit()
        return {'message': 'Số lượng sản phẩm đã được cập nhật thành công!'}

    @cart_ns.doc('delete_cart_item')
    def delete(self, cart_id):
        """Xóa sản phẩm khỏi giỏ hàng"""
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'message': 'Sản phẩm trong giỏ hàng không tồn tại!'}, 404
        db.session.delete(cart_item)
        db.session.commit()
        return {'message': 'Sản phẩm đã được xóa khỏi giỏ hàng!'}