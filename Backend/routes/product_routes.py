from flask_restx import Namespace, Resource, fields
from models.product import SanPham
from models.database import db

# Tạo namespace cho sản phẩm
product_ns = Namespace('products', description='Product related operations')

# Định nghĩa model dữ liệu cho Swagger
product_model = product_ns.model('Product', {
    'Ten': fields.String(required=True, description='Tên sản phẩm'),
    'Loai': fields.String(required=True, description='Loại sản phẩm'),
    'MoTa': fields.String(description='Mô tả sản phẩm'),
    'Gia': fields.Float(required=True, description='Giá sản phẩm'),
    'SoLuong': fields.Integer(required=True, description='Số lượng sản phẩm'),
    'HinhAnh': fields.String(description='Đường dẫn hình ảnh sản phẩm')
})

@product_ns.route('/')
class ProductList(Resource):
    @product_ns.doc('get_products')
    def get(self):
        """Lấy danh sách sản phẩm"""
        products = SanPham.query.all()
        return [{
            'ProductID': product.ProductID,
            'Ten': product.Ten,
            'Loai': product.Loai,
            'MoTa': product.MoTa,
            'Gia': float(product.Gia),
            'SoLuong': product.SoLuong,
            'HinhAnh': product.HinhAnh
        } for product in products]

    @product_ns.expect(product_model)
    @product_ns.doc('add_product')
    def post(self):
        """Tạo mới một sản phẩm"""
        data = product_ns.payload
        new_product = SanPham(
            Ten=data['Ten'],
            Loai=data['Loai'],
            MoTa=data.get('MoTa'),
            Gia=data['Gia'],
            SoLuong=data['SoLuong'],
            HinhAnh=data.get('HinhAnh')
        )
        db.session.add(new_product)
        db.session.commit()
        return {'message': 'Sản phẩm đã được thêm thành công!', 'ProductID': new_product.ProductID}, 201

@product_ns.route('/<int:product_id>')
@product_ns.param('product_id', 'ID của sản phẩm')
class Product(Resource):
    @product_ns.doc('get_product_by_id')
    def get(self, product_id):
        """Lấy thông tin chi tiết của một sản phẩm"""
        product = SanPham.query.get(product_id)
        if not product:
            return {'message': 'Sản phẩm không tồn tại!'}, 404
        return {
            'ProductID': product.ProductID,
            'Ten': product.Ten,
            'Loai': product.Loai,
            'MoTa': product.MoTa,
            'Gia': float(product.Gia),
            'SoLuong': product.SoLuong,
            'HinhAnh': product.HinhAnh
        }

    @product_ns.doc('delete_product')
    def delete(self, product_id):
        """Xóa một sản phẩm"""
        product = SanPham.query.get(product_id)
        if not product:
            return {'message': 'Sản phẩm không tồn tại!'}, 404
        db.session.delete(product)
        db.session.commit()
        return {'message': 'Sản phẩm đã được xóa thành công!'}

    @product_ns.expect(product_model)
    @product_ns.doc('update_product')
    def put(self, product_id):
        """Cập nhật thông tin sản phẩm"""
        product = SanPham.query.get(product_id)
        if not product:
            return {'message': 'Sản phẩm không tồn tại!'}, 404
        data = product_ns.payload
        product.Ten = data.get('Ten', product.Ten)
        product.Loai = data.get('Loai', product.Loai)
        product.MoTa = data.get('MoTa', product.MoTa)
        product.Gia = data.get('Gia', product.Gia)
        product.SoLuong = data.get('SoLuong', product.SoLuong)
        product.HinhAnh = data.get('HinhAnh', product.HinhAnh)
        db.session.commit()
        return {'message': 'Thông tin sản phẩm đã được cập nhật thành công!'}