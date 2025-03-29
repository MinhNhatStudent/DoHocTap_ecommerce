from flask_restx import Namespace, Resource, fields
from models.orders import DonHang
from models.order_item import SanPhamTrongDonHang
from models.product import SanPham
from models.database import db

# Tạo namespace cho Orders
order_ns = Namespace('orders', description='Order related operations')

# Định nghĩa model dữ liệu cho Swagger
order_item_model = order_ns.model('OrderItem', {
    'ProductID': fields.Integer(required=True, description='ID của sản phẩm'),
    'SoLuong': fields.Integer(required=True, description='Số lượng sản phẩm')
})

order_model = order_ns.model('Order', {
    'UserID': fields.Integer(required=True, description='ID của người dùng'),
    'Items': fields.List(fields.Nested(order_item_model), description='Danh sách sản phẩm trong đơn hàng'),
    'TongTien': fields.Float(required=True, description='Tổng tiền của đơn hàng')
})

@order_ns.route('/')
class OrderList(Resource):
    @order_ns.expect(order_model)
    @order_ns.doc('create_order')
    def post(self):
        """Tạo đơn hàng mới"""
        data = order_ns.payload
        new_order = DonHang(
            UserID=data['UserID'],
            TongTien=data['TongTien'],
            TrangThai='pending'
        )
        db.session.add(new_order)
        db.session.commit()

        # Thêm sản phẩm vào bảng SanPhamTrongDonHang
        for item in data['Items']:
            order_item = SanPhamTrongDonHang(
                OrderID=new_order.OrdersID,
                ProductID=item['ProductID'],
                SoLuong=item['SoLuong']
            )
            db.session.add(order_item)
        db.session.commit()

        return {'message': 'Đơn hàng đã được tạo thành công!', 'OrderID': new_order.OrdersID}, 201

@order_ns.route('/<int:user_id>')
@order_ns.param('user_id', 'ID của người dùng')
class UserOrders(Resource):
    @order_ns.doc('get_user_orders')
    def get(self, user_id):
        """Lấy danh sách đơn hàng của người dùng"""
        orders = DonHang.query.filter_by(UserID=user_id).all()
        result = []
        for order in orders:
            items = SanPhamTrongDonHang.query.filter_by(OrderID=order.OrdersID).all()
            item_details = []
            for item in items:
                product = SanPham.query.get(item.ProductID)
                if product:
                    item_details.append({
                        'ProductID': product.ProductID,
                        'Ten': product.Ten,
                        'SoLuong': item.SoLuong,
                        'Gia': float(product.Gia)
                    })
            result.append({
                'OrderID': order.OrdersID,
                'UserID': order.UserID,
                'TongTien': float(order.TongTien),
                'NgayDat': order.NgayDat,
                'TrangThai': order.TrangThai,
                'Items': item_details
            })
        return result

@order_ns.route('/<int:order_id>')
@order_ns.param('order_id', 'ID của đơn hàng')
class Order(Resource):
    @order_ns.expect(order_model)
    @order_ns.doc('update_order_status')
    def put(self, order_id):
        """Cập nhật trạng thái đơn hàng"""
        order = DonHang.query.get(order_id)
        if not order:
            return {'message': 'Đơn hàng không tồn tại!'}, 404
        data = order_ns.payload
        order.TrangThai = data.get('TrangThai', order.TrangThai)
        db.session.commit()
        return {'message': 'Trạng thái đơn hàng đã được cập nhật thành công!'}

    @order_ns.doc('delete_order')
    def delete(self, order_id):
        """Xóa đơn hàng"""
        order = DonHang.query.get(order_id)
        if not order:
            return {'message': 'Đơn hàng không tồn tại!'}, 404
        db.session.delete(order)
        db.session.commit()
        return {'message': 'Đơn hàng đã được xóa thành công!'}