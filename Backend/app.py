from flask import Flask, request, jsonify
from flask_cors import CORS
from models.database import db
from routes.swagger_routes import swagger_bp 
from routes.view_routes import view_bp
from routes.recommend_routes import recommend_bp
from sqlalchemy.sql import text
from services.embed_service import ProductEmbedding

# Khởi tạo Flask app với đường dẫn tĩnh và template
app = Flask(__name__, 
            static_folder='static',  # Thư mục chứa các file tĩnh (CSS, JS, hình ảnh)
            template_folder='templates'  # Thư mục chứa các template HTML
           )
CORS(app)
app.secret_key = 'hetuvan-secret-key-2023'  # Thêm secret key cho session

# Cấu hình kết nối MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/hetuvan'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("Kết nối cơ sở dữ liệu thành công!")
    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")

# Đăng ký các blueprints - đăng ký view_bp trước để tránh xung đột với swagger_bp
app.register_blueprint(view_bp)
app.register_blueprint(swagger_bp)
app.register_blueprint(recommend_bp, url_prefix='/recommend_bp')

# Đã cấu hình đường dẫn tĩnh khi khởi tạo Flask app


if __name__ == '__main__':
    app.run(debug=True)