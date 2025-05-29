from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import requests
import json
from models.product import SanPham
from models.cart import Cart
from models.database import db

view_bp = Blueprint('view_bp', __name__)

@view_bp.route('/')
def index():
    """
    Trang chủ hiển thị danh sách sản phẩm và sản phẩm mới nhất
    """
    # Lấy danh sách tất cả sản phẩm
    all_products = SanPham.query.all()
    
    # Lấy danh sách sản phẩm mới nhất (giả định sản phẩm có ID cao hơn là mới hơn)
    newest_products = SanPham.query.order_by(SanPham.ProductID.desc()).limit(8).all()
    # Tạm thời sử dụng trực tiếp class RecommendationService để lấy sản phẩm phổ biến
    try:
        from services.recommend import RecommendationService
        recommendation_service = RecommendationService()
        
        # Gọi trực tiếp phương thức của service
        popular_data = recommendation_service.get_popular_products(8)
        
        if popular_data:
            # Lấy các product từ database dựa trên ID
            popular_ids = [item['ProductID'] for item in popular_data]
            popular_products = SanPham.query.filter(SanPham.ProductID.in_(popular_ids)).all()
            
            # Sắp xếp sản phẩm theo thứ tự như trong API
            product_dict = {product.ProductID: product for product in popular_products}
            popular_products = [product_dict[id] for id in popular_ids if id in product_dict]
        else:
            popular_products = []
    except Exception as e:
        print(f"Error getting popular products: {e}")
        popular_products = []
        
    # Lấy sản phẩm bán chạy - dựa trên các tương tác loại cart và các đơn hàng
    try:
        # Đơn giản hóa cho demo: sử dụng sản phẩm có nhiều tương tác 'cart' nhất
        from sqlalchemy import func
        from models.interaction import TuongTac
        
        bestseller_ids = db.session.query(TuongTac.ProductID, func.count(TuongTac.InteractionID).label('interaction_count'))\
                        .filter(TuongTac.InteractionType == 'cart')\
                        .group_by(TuongTac.ProductID)\
                        .order_by(db.desc('interaction_count'))\
                        .limit(8)\
                        .all()
        
        bestseller_ids = [item[0] for item in bestseller_ids]
        bestseller_products = SanPham.query.filter(SanPham.ProductID.in_(bestseller_ids)).all() if bestseller_ids else []
        
        # Nếu không đủ 8 sản phẩm bán chạy, bổ sung thêm
        if len(bestseller_products) < 8:
            # Lấy ID của sản phẩm đã có trong danh sách
            existing_ids = [product.ProductID for product in bestseller_products]
            
            # Lấy thêm các sản phẩm khác cho đủ 8
            additional_products = SanPham.query.filter(~SanPham.ProductID.in_(existing_ids))\
                                .order_by(db.func.random())\
                                .limit(8 - len(bestseller_products))\
                                .all()
            
            bestseller_products.extend(additional_products)
    except Exception as e:
        print(f"Error getting bestsellers: {e}")
        bestseller_products = SanPham.query.order_by(db.func.random()).limit(8).all()
    
    # Lấy sản phẩm theo nhãn hiệu cụ thể
    thienlong_products = SanPham.query.filter(SanPham.NhanHang.ilike('%thiên long%')).limit(8).all()
    copyplus_products = SanPham.query.filter(SanPham.NhanHang.ilike('%copy plus%')).limit(8).all()
    parker_products = SanPham.query.filter(SanPham.NhanHang.ilike('%parker%')).limit(8).all()
    
    return render_template('index.html', 
                           all_products=all_products, 
                           newest_products=newest_products,
                           popular_products=popular_products,
                           bestseller_products=bestseller_products,
                           thienlong_products=thienlong_products,
                           copyplus_products=copyplus_products,
                           parker_products=parker_products)

@view_bp.route('/product/<int:product_id>')
def product_detail(product_id):
    """
    Trang chi tiết sản phẩm, hiển thị thông tin sản phẩm và sản phẩm liên quan
    """
    # Lấy thông tin sản phẩm
    product = SanPham.query.get_or_404(product_id)    # Lấy các sản phẩm liên quan
    recommendation_error = None
    try:
        response = requests.get(f'http://localhost:5000/api/vectorize/similar/{product_id}?count=4')
        if response.status_code == 200:
            similar_products_data = response.json()
            similar_product_ids = [item['ProductID'] for item in similar_products_data]
            similar_products = SanPham.query.filter(SanPham.ProductID.in_(similar_product_ids)).all()
        else:
            raise Exception(f"API returned status code: {response.status_code}")
    except Exception as e:
        # Nếu có lỗi khi gọi API, hiển thị một số sản phẩm ngẫu nhiên
        print(f"Error calling recommendation API: {e}")
        recommendation_error = "Không thể tải sản phẩm tương tự từ hệ thống đề xuất. Hiển thị sản phẩm thay thế."
        similar_products = SanPham.query.filter(SanPham.ProductID != product_id).order_by(db.func.random()).limit(4).all()
    
    # Tạo tương tác xem sản phẩm (giả sử user_id=1)
    try:
        requests.post('http://localhost:5000/interactions', json={
            'user_id': 1,  # Giả sử user_id là 1 cho demo
            'product_id': product_id,
            'interaction_type': 'view'
        })
    except:
        pass  # Bỏ qua lỗi nếu không thể tạo tương tác
    
    return render_template('product.html', product=product, similar_products=similar_products, recommendation_error=recommendation_error)

@view_bp.route('/cart')
def cart():
    """
    Trang giỏ hàng
    """
    # Giả sử user_id=1 cho demo
    user_id = 1
    
    try:
        # Lấy sản phẩm trong giỏ hàng trực tiếp từ database
        from models.cart import Cart
        cart_items_raw = Cart.query.filter_by(UserID=user_id).all()
        
        # Lấy chi tiết sản phẩm trong giỏ
        cart_items = []
        total = 0
        
        for item in cart_items_raw:
            product = SanPham.query.get(item.ProductID)
            if product:
                item_total = float(product.Gia) * item.SoLuong
                cart_items.append({
                    'CartID': item.CartID,
                    'ProductID': product.ProductID,
                    'Ten': product.Ten,
                    'NhanHang': product.NhanHang,
                    'Gia': float(product.Gia),
                    'SoLuong': item.SoLuong,
                    'HinhAnh': product.HinhAnh,
                    'item_total': item_total
                })
                total += item_total
        
        # Lấy sản phẩm đề xuất dựa trên giỏ hàng
        try:
            # Lấy sản phẩm đề xuất cho người dùng
            from services.recommend import RecommendationService
            recommendation_service = RecommendationService()
            
            # Lấy sản phẩm phổ biến làm đề xuất
            recommended_data = recommendation_service.get_popular_products(4)
            
            if recommended_data:
                recommended_ids = [item['ProductID'] for item in recommended_data]
                recommended_products = SanPham.query.filter(SanPham.ProductID.in_(recommended_ids)).all()
                
                # Sắp xếp sản phẩm theo thứ tự như trong API
                product_dict = {product.ProductID: product for product in recommended_products}
                recommended_products = [product_dict[id] for id in recommended_ids if id in product_dict]
            else:
                recommended_products = SanPham.query.order_by(db.func.random()).limit(4).all()
        except Exception as e:
            print(f"Error getting recommendations: {e}")
            recommended_products = SanPham.query.order_by(db.func.random()).limit(4).all()
        
        return render_template(
            'cart.html', 
            cart_items=cart_items, 
            total=total, 
            recommended_products=recommended_products
        )
    except Exception as e:
        print(f"Error: {e}")
        return render_template('cart.html', cart_items=[], total=0, recommended_products=[])

@view_bp.route('/login', methods=['GET', 'POST'])
def login():
    """
    Trang đăng nhập
    """
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        try:
            # Gọi API kiểm tra đăng nhập
            response = requests.post('http://localhost:5000/users/login', json={
                'email': email,
                'password': password
            })
            
            data = response.json()
            
            if data.get('status') == 'success':
                # Lưu thông tin người dùng vào session
                session['user_id'] = data['user']['UserID']
                session['user_name'] = data['user']['Ten']
                session['user_email'] = data['user']['Email']
                session['user_role'] = data['user']['VaiTro']
                
                flash('Đăng nhập thành công!', 'success')
                return redirect(url_for('view_bp.index'))
            else:
                flash('Email hoặc mật khẩu không đúng!', 'danger')
        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('dangnhap.html', page_title="Đăng nhập")

@view_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Trang đăng ký
    """
    if request.method == 'POST':
        ten = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        
        # Kiểm tra xác nhận mật khẩu
        if password != password_confirm:
            flash('Mật khẩu xác nhận không khớp!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        try:
            # Gọi API đăng ký
            response = requests.post('http://localhost:5000/users', json={
                'Ten': ten,
                'Email': email,
                'MatKhau': password,
                'VaiTro': 'user',
                'Tuoi': 25  # Giá trị mặc định
            })
            
            data = response.json()
            
            if response.status_code == 201 or response.status_code == 200:
                flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
                return redirect(url_for('view_bp.login'))
            else:
                flash(f'Có lỗi xảy ra: {data.get("message", "Lỗi không xác định")}', 'danger')
        except Exception as e:
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('dangky.html', page_title="Đăng ký")

@view_bp.route('/logout')
def logout():
    """
    Đăng xuất người dùng
    """
    session.clear()
    flash('Đã đăng xuất thành công!', 'success')
    return redirect(url_for('view_bp.index'))

@view_bp.route('/store')
def store():
    """
    Trang cửa hàng hiển thị tất cả sản phẩm
    """
    search_query = request.args.get('search', '')
    
    # Nếu có từ khóa tìm kiếm
    if search_query:
        products = SanPham.query.filter(SanPham.Ten.like(f'%{search_query}%')).all()
    else:
        products = SanPham.query.all()      # Tạm thời sử dụng trực tiếp class RecommendationService để lấy sản phẩm phổ biến
    try:
        from services.recommend import RecommendationService
        recommendation_service = RecommendationService()
        
        # Gọi trực tiếp phương thức của service
        popular_data = recommendation_service.get_popular_products(8)
        
        if popular_data:
            # Lấy các product từ database dựa trên ID
            popular_ids = [item['ProductID'] for item in popular_data]
            popular_products = SanPham.query.filter(SanPham.ProductID.in_(popular_ids)).all()
            
            # Sắp xếp sản phẩm theo thứ tự như trong API
            product_dict = {product.ProductID: product for product in popular_products}
            popular_products = [product_dict[id] for id in popular_ids if id in product_dict]
        else:
            popular_products = SanPham.query.order_by(db.func.random()).limit(4).all()
    except Exception as e:
        print(f"Error getting popular products: {e}")
        popular_products = SanPham.query.order_by(db.func.random()).limit(4).all()
    
    return render_template('store.html', products=products, popular_products=popular_products)

@view_bp.route('/api/cart/<int:cart_id>', methods=['PUT'])
def update_cart_item(cart_id):
    """
    API để cập nhật số lượng sản phẩm trong giỏ hàng (AJAX)
    """
    try:
        from models.cart import Cart
        
        data = request.get_json()
        quantity = data.get('SoLuong', 1)
        
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'message': 'Sản phẩm trong giỏ hàng không tồn tại!'}, 404
        
        cart_item.SoLuong = quantity
        db.session.commit()
        
        return {'message': 'Số lượng sản phẩm đã được cập nhật thành công!'}
    except Exception as e:
        return {'message': f'Có lỗi xảy ra: {str(e)}'}, 500

@view_bp.route('/api/cart/<int:cart_id>', methods=['DELETE'])
def remove_cart_item(cart_id):
    """
    API để xóa sản phẩm khỏi giỏ hàng (AJAX)
    """
    try:
        from models.cart import Cart
        
        cart_item = Cart.query.get(cart_id)
        if not cart_item:
            return {'message': 'Sản phẩm trong giỏ hàng không tồn tại!'}, 404
        
        db.session.delete(cart_item)
        db.session.commit()
        
        return {'message': 'Sản phẩm đã được xóa khỏi giỏ hàng!'}
    except Exception as e:
        return {'message': f'Có lỗi xảy ra: {str(e)}'}, 500

@view_bp.route('/api/cart/', methods=['POST'])
def add_to_cart_ajax():
    """
    API để thêm sản phẩm vào giỏ hàng (AJAX)
    """
    try:
        from models.cart import Cart
        
        data = request.get_json()
        user_id = data.get('UserID', 1)  # Default to user 1 for demo
        product_id = data.get('ProductID')
        quantity = data.get('SoLuong', 1)
        
        # Kiểm tra xem sản phẩm đã có trong giỏ hàng chưa
        existing_item = Cart.query.filter_by(UserID=user_id, ProductID=product_id).first()
        
        if existing_item:
            # Nếu đã có, tăng số lượng
            existing_item.SoLuong += quantity
        else:
            # Nếu chưa có, tạo mới
            new_cart_item = Cart(
                UserID=user_id,
                ProductID=product_id,
                SoLuong=quantity
            )
            db.session.add(new_cart_item)
        
        db.session.commit()
        
        return {'message': 'Sản phẩm đã được thêm vào giỏ hàng!'}
    except Exception as e:
        return {'message': f'Có lỗi xảy ra: {str(e)}'}, 500
