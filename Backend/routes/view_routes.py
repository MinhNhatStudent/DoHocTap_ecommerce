from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
import requests
import json
from models.product import SanPham
from models.cart import Cart
from models.database import db

view_bp = Blueprint('view_bp', __name__)

def get_image_url(hinh_anh):
    """
    Helper function to get proper image URL
    Returns full URL if it starts with http/https, otherwise prepends static path
    """
    if not hinh_anh:
        return url_for('static', filename='img/noimage.jpg')
    
    if hinh_anh.startswith(('http://', 'https://')):
        return hinh_anh
    else:
        return url_for('static', filename=f'img/{hinh_anh}')

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

@view_bp.route('/cart', methods=['GET', 'POST'])
def cart():
    """
    Trang giỏ hàng - GET: hiển thị giỏ hàng, POST: thêm sản phẩm vào giỏ hàng
    """
    if request.method == 'POST':
        # Xử lý thêm sản phẩm vào giỏ hàng
        try:
            from models.cart import Cart
            
            # Lấy dữ liệu từ JSON request
            data = request.get_json()
            if not data:
                return jsonify({'error': 'Không có dữ liệu được gửi'}), 400
                
            # Lấy user_id từ session, nếu không có thì sử dụng mặc định hoặc từ request
            user_id = session.get('user_id', data.get('user_id', 1))
            product_id = data.get('product_id')
            quantity = data.get('quantity', 1)
            
            if not product_id:
                return jsonify({'error': 'Thiếu thông tin sản phẩm'}), 400
            
            # Kiểm tra xem sản phẩm có tồn tại không
            product = SanPham.query.get(product_id)
            if not product:
                return jsonify({'error': 'Sản phẩm không tồn tại'}), 404
            
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
            return jsonify({
                'status': 'success', 
                'message': 'Sản phẩm đã được thêm vào giỏ hàng!'
            })
            
        except Exception as e:
            print(f"Error adding to cart: {e}")
            return jsonify({'error': f'Có lỗi xảy ra: {str(e)}'}), 500
    
    # GET request - hiển thị trang giỏ hàng
    # Lấy user_id từ session, nếu không có thì sử dụng mặc định
    user_id = session.get('user_id', 1)
    
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
          # Lấy sản phẩm đề xuất dựa trên giỏ hàng và lịch sử người dùng
        try:
            # Sử dụng API vectorize để lấy đề xuất cá nhân hóa
            response = requests.get(f'http://localhost:5000/api/vectorize/user/{user_id}?count=4')
            
            if response.status_code == 200:
                recommended_data = response.json()
                
                if recommended_data:
                    recommended_ids = [item['ProductID'] for item in recommended_data]
                    recommended_products = SanPham.query.filter(SanPham.ProductID.in_(recommended_ids)).all()
                    
                    # Sắp xếp sản phẩm theo thứ tự như trong API
                    product_dict = {product.ProductID: product for product in recommended_products}
                    recommended_products = [product_dict[id] for id in recommended_ids if id in product_dict]
                else:
                    recommended_products = SanPham.query.order_by(db.func.random()).limit(4).all()
            else:
                # Nếu API không khả dụng, fallback về sản phẩm phổ biến
                from services.recommend import RecommendationService
                recommendation_service = RecommendationService()
                recommended_data = recommendation_service.get_popular_products(4)
                
                if recommended_data:
                    recommended_ids = [item['ProductID'] for item in recommended_data]
                    recommended_products = SanPham.query.filter(SanPham.ProductID.in_(recommended_ids)).all()
                    product_dict = {product.ProductID: product for product in recommended_products}
                    recommended_products = [product_dict[id] for id in recommended_ids if id in product_dict]
                else:
                    recommended_products = SanPham.query.order_by(db.func.random()).limit(4).all()
                    
        except Exception as e:
            print(f"Error getting personalized recommendations: {e}")
            # Fallback về sản phẩm ngẫu nhiên
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
    # Kiểm tra nếu user đã đăng nhập
    if 'user_id' in session:
        flash('Bạn đã đăng nhập rồi!', 'info')
        return redirect(url_for('view_bp.index'))
    
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if not email or not password:
            flash('Vui lòng điền đầy đủ thông tin đăng nhập!', 'danger')
            return render_template('dangnhap.html', page_title="Đăng nhập")
        
        try:
            # Sử dụng direct database query thay vì API call
            from models.user import NguoiDung
            user = NguoiDung.query.filter_by(Email=email).first()
            
            if not user:
                flash('Email không tồn tại trong hệ thống!', 'danger')
                return render_template('dangnhap.html', page_title="Đăng nhập")
            
            # Kiểm tra mật khẩu (trong thực tế nên sử dụng hash)
            if user.Pass != password:
                flash('Mật khẩu không đúng!', 'danger')
                return render_template('dangnhap.html', page_title="Đăng nhập")
            
            # Lưu thông tin người dùng vào session
            session['user_id'] = user.UserID
            session['user_name'] = user.Ten
            session['user_email'] = user.Email
            session['user_role'] = user.Role
            session['logged_in'] = True
            
            # Thiết lập thời gian session nếu remember me
            if remember:
                session.permanent = True
            
            flash('Đăng nhập thành công!', 'success')
            
            # Redirect to next page if specified, otherwise to index
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('view_bp.index'))
            
        except Exception as e:
            print(f"Login error: {e}")
            flash(f'Có lỗi xảy ra: {str(e)}', 'danger')
    
    return render_template('dangnhap.html', page_title="Đăng nhập")

@view_bp.route('/register', methods=['GET', 'POST'])
def register():
    """
    Trang đăng ký
    """
    # Kiểm tra nếu user đã đăng nhập
    if 'user_id' in session:
        flash('Bạn đã đăng nhập rồi!', 'info')
        return redirect(url_for('view_bp.index'))
    
    if request.method == 'POST':
        ten = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        password_confirm = request.form.get('password_confirm')
        age = request.form.get('age')
        terms = request.form.get('terms')
        
        # Validate required fields
        if not ten or not email or not password or not password_confirm:
            flash('Vui lòng điền đầy đủ thông tin bắt buộc!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        # Validate email format
        import re
        email_regex = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
        if not re.match(email_regex, email):
            flash('Vui lòng nhập địa chỉ email hợp lệ!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        # Validate password length
        if len(password) < 6:
            flash('Mật khẩu phải có ít nhất 6 ký tự!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        # Validate password confirmation
        if password != password_confirm:
            flash('Mật khẩu xác nhận không khớp!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        # Validate terms acceptance
        if not terms:
            flash('Vui lòng đồng ý với điều khoản dịch vụ!', 'danger')
            return render_template('dangky.html', page_title="Đăng ký")
        
        # Validate age if provided
        if age:
            try:
                age = int(age)
                if age < 13 or age > 100:
                    flash('Tuổi phải trong khoảng từ 13 đến 100!', 'danger')
                    return render_template('dangky.html', page_title="Đăng ký")
            except ValueError:
                flash('Tuổi phải là một số hợp lệ!', 'danger')
                return render_template('dangky.html', page_title="Đăng ký")
        
        try:
            # Check if email already exists using direct database query
            from models.user import NguoiDung
            existing_user = NguoiDung.query.filter_by(Email=email).first()
            if existing_user:
                flash('Email này đã được sử dụng! Vui lòng chọn email khác.', 'danger')
                return render_template('dangky.html', page_title="Đăng ký")
            
            # Create new user directly in database
            new_user = NguoiDung(
                Ten=ten,
                Email=email,
                Pass=password,  # In production, should hash this password
                Role='user',
                Age=age if age else None
            )
            db.session.add(new_user)
            db.session.commit()
            
            flash('Đăng ký thành công! Vui lòng đăng nhập.', 'success')
            return redirect(url_for('view_bp.login'))
            
        except Exception as e:
            db.session.rollback()
            print(f"Registration error: {e}")
            flash('Có lỗi xảy ra khi đăng ký. Vui lòng thử lại!', 'danger')
    
    return render_template('dangky.html', page_title="Đăng ký")

@view_bp.route('/logout')
def logout():
    """
    Đăng xuất người dùng
    """
    if 'user_id' in session:
        user_name = session.get('user_name', 'người dùng')
        session.clear()
        flash(f'Đã đăng xuất thành công! Hẹn gặp lại {user_name}.', 'success')
    else:
        flash('Bạn chưa đăng nhập!', 'info')
    
    return redirect(url_for('view_bp.index'))

# Helper function to check if user is logged in
def login_required(f):
    """Decorator để kiểm tra đăng nhập"""
    from functools import wraps
    
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Vui lòng đăng nhập để truy cập trang này!', 'warning')
            return redirect(url_for('view_bp.login', next=request.url))
        return f(*args, **kwargs)
    return decorated_function

# Context processor to make user info available in all templates
@view_bp.app_context_processor
def inject_user():
    """Inject user information into all templates"""
    return dict(
        current_user={
            'id': session.get('user_id'),
            'name': session.get('user_name'),
            'email': session.get('user_email'),
            'role': session.get('user_role'),
            'logged_in': session.get('logged_in', False)
        },
        get_image_url=get_image_url
    )

@view_bp.route('/store')
def store():
    """
    Trang cửa hàng với chức năng lọc sản phẩm theo thương hiệu, giá và thời gian
    """
    # Lấy các tham số lọc từ query string
    search_query = request.args.get('search', '')
    brand_filter = request.args.get('brand', '')
    min_price = request.args.get('min_price', type=float)
    max_price = request.args.get('max_price', type=float)
    sort_by = request.args.get('sort', 'newest')  # newest, price_asc, price_desc, name
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 12, type=int)
    
    # Bắt đầu với query cơ bản
    query = SanPham.query
    
    # Áp dụng lọc tìm kiếm
    if search_query:
        query = query.filter(SanPham.Ten.ilike(f'%{search_query}%'))
    
    # Áp dụng lọc theo thương hiệu
    if brand_filter:
        query = query.filter(SanPham.NhanHang.ilike(f'%{brand_filter}%'))
    
    # Áp dụng lọc theo giá
    if min_price is not None:
        query = query.filter(SanPham.Gia >= min_price)
    if max_price is not None:
        query = query.filter(SanPham.Gia <= max_price)
    
    # Áp dụng sắp xếp
    if sort_by == 'newest':
        query = query.order_by(SanPham.ProductID.desc())
    elif sort_by == 'price_asc':
        query = query.order_by(SanPham.Gia.asc())
    elif sort_by == 'price_desc':
        query = query.order_by(SanPham.Gia.desc())
    elif sort_by == 'name':
        query = query.order_by(SanPham.Ten.asc())
    else:
        query = query.order_by(SanPham.ProductID.desc())
    
    # Phân trang
    products = query.paginate(
        page=page, 
        per_page=per_page, 
        error_out=False
    )
    
    # Lấy danh sách các thương hiệu để hiển thị trong filter
    brands = db.session.query(SanPham.NhanHang).distinct().filter(SanPham.NhanHang.isnot(None)).all()
    brands = [brand[0] for brand in brands if brand[0]]
    
    # Lấy khoảng giá để hiển thị price slider
    price_range = db.session.query(
        db.func.min(SanPham.Gia).label('min_price'),
        db.func.max(SanPham.Gia).label('max_price')
    ).first()
    
    # Lấy số lượng sản phẩm theo từng thương hiệu
    brand_counts = {}
    for brand in brands:
        count = SanPham.query.filter(SanPham.NhanHang.ilike(f'%{brand}%')).count()
        brand_counts[brand] = count
    
    return render_template('store.html',
                         products=products,
                         brands=brands,
                         brand_counts=brand_counts,
                         price_range=price_range,
                         current_filters={
                             'search': search_query,
                             'brand': brand_filter,
                             'min_price': min_price,
                             'max_price': max_price,
                             'sort': sort_by,
                             'per_page': per_page
                         })

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
