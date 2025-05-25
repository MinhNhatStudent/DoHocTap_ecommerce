from flask import Blueprint
from flask_restx import Api
from routes.user_routes import user_ns
from routes.product_routes import product_ns
from routes.interaction_routes import interaction_ns
from routes.favorite_routes import favorite_ns
from routes.cart_routes import cart_ns
from routes.order_routes import order_ns
from routes.product_vectorize import vectorize_ns  # Thêm dòng này

# Định nghĩa Blueprint cho Swagger
swagger_bp = Blueprint('swagger_bp', __name__)

# Tạo API từ Flask-RESTPlus
api = Api(
    swagger_bp,
    version='1.0',
    title='HeTuVanThongTin API',
    description='API documentation for HeTuVanThongTin',
    doc='/swagger'  # URL để truy cập Swagger UI
)

# Đăng ký namespace
api.add_namespace(user_ns, path='/users')
api.add_namespace(product_ns, path='/products')
api.add_namespace(interaction_ns, path='/interactions')
api.add_namespace(favorite_ns, path='/favorites')
api.add_namespace(cart_ns, path='/cart')
api.add_namespace(order_ns, path='/orders')
api.add_namespace(vectorize_ns, path='/vectorize')  