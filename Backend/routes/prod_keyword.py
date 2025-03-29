from flask_restx import Namespace, Resource, fields
from models.product_keywords import SanPham_TuKhoa
from models.product import SanPham
from models.database import db
from services.preprocess import preprocess_text, extract_keywords_tfidf
from services.keywordToDB import save_keywords_to_db

# Tạo namespace cho Product Keywords
prod_keyword_ns = Namespace('product-keywords', description='Product Keyword related operations')

# Định nghĩa model dữ liệu cho Swagger
prod_keyword_model = prod_keyword_ns.model('ProductKeyword', {
    'ProductID': fields.Integer(required=True, description='ID của sản phẩm'),
    'TuKhoa': fields.String(required=True, description='Từ khóa của sản phẩm')
})

@prod_keyword_ns.route('/')
class ProductKeywordList(Resource):
    @prod_keyword_ns.expect(prod_keyword_model)
    @prod_keyword_ns.doc('add_product_keyword')
    def post(self):
        """Thêm từ khóa cho sản phẩm"""
        data = prod_keyword_ns.payload
        new_keyword = SanPham_TuKhoa(
            ProductID=data['ProductID'],
            TuKhoa=data['TuKhoa']
        )
        db.session.add(new_keyword)
        db.session.commit()
        return {'message': 'Từ khóa đã được thêm thành công!', 'ProductID': new_keyword.ProductID, 'TuKhoa': new_keyword.TuKhoa}, 201

@prod_keyword_ns.route('/<int:product_id>')
@prod_keyword_ns.param('product_id', 'ID của sản phẩm')
class ProductKeywords(Resource):
    @prod_keyword_ns.doc('get_product_keywords')
    def get(self, product_id):
        """Lấy danh sách từ khóa của sản phẩm"""
        keywords = SanPham_TuKhoa.query.filter_by(ProductID=product_id).all()
        return [{'ProductID': keyword.ProductID, 'TuKhoa': keyword.TuKhoa} for keyword in keywords]

@prod_keyword_ns.route('/<int:product_id>/<string:keyword>')
@prod_keyword_ns.param('product_id', 'ID của sản phẩm')
@prod_keyword_ns.param('keyword', 'Từ khóa của sản phẩm')
class ProductKeyword(Resource):
    @prod_keyword_ns.doc('delete_product_keyword')
    def delete(self, product_id, keyword):
        """Xóa từ khóa của sản phẩm"""
        keyword_entry = SanPham_TuKhoa.query.filter_by(ProductID=product_id, TuKhoa=keyword).first()
        if not keyword_entry:
            return {'message': 'Từ khóa không tồn tại!'}, 404
        db.session.delete(keyword_entry)
        db.session.commit()
        return {'message': 'Từ khóa đã được xóa thành công!'}

@prod_keyword_ns.route('/generate')
class GenerateKeywords(Resource):
    @prod_keyword_ns.doc('generate_product_keywords')
    def post(self):
        """Tự động thu thập từ khóa từ sản phẩm"""
        # Lấy danh sách sản phẩm
        products = SanPham.query.all()
        product_data = [{
            'ProductID': product.ProductID,
            'MoTa': product.MoTa
        } for product in products]
        
        # Trích xuất từ khóa
        product_keywords = extract_keywords_tfidf(product_data)
        
        # Lưu từ khóa vào cơ sở dữ liệu
        save_keywords_to_db(product_keywords)
        
        return {'message': 'Từ khóa đã được tạo và lưu thành công!'}
    
@prod_keyword_ns.route('/generate/<int:product_id>')
class GenerateKeywordsForProduct(Resource):
    def post(self, product_id):
        """Tự động thu thập từ khóa cho một sản phẩm cụ thể"""
        product = SanPham.query.get(product_id)
        if not product:
            return {'message': 'Sản phẩm không tồn tại!'}, 404
        
        product_data = [{
            'ProductID': product.ProductID,
            'MoTa': product.MoTa
        }]
        
        # Trích xuất từ khóa
        product_keywords = extract_keywords_tfidf(product_data)
        
        # Lưu từ khóa vào cơ sở dữ liệu
        save_keywords_to_db(product_keywords)
        
        return {'message': f'Từ khóa cho sản phẩm {product_id} đã được tạo và lưu thành công!'}