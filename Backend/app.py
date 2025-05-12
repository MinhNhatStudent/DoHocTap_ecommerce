from flask import Flask
from flask_cors import CORS
from models.database import db
from routes.swagger_routes import swagger_bp 
from sqlalchemy.sql import text

app = Flask(__name__)
CORS(app)

# Cấu hình kết nối MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:@localhost/hetuvan'
# ten tai khoan la host-dia chi localhost, ko co pass, ten csdl la hetuvan
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db.init_app(app)

@app.route('/reset-database', methods=['POST'])
def reset_database():
    """Xóa và tạo lại toàn bộ cơ sở dữ liệu"""
    with app.app_context():
        db.drop_all()  # Xóa toàn bộ bảng
        db.create_all()  # Tạo lại bảng dựa trên mô hình
    return {"message": "Cơ sở dữ liệu đã được reset thành công!"}, 200

with app.app_context():
    try:
        db.session.execute(text('SELECT 1'))
        print("Kết nối cơ sở dữ liệu thành công!")
    except Exception as e:
        print(f"Lỗi kết nối cơ sở dữ liệu: {e}")


app.register_blueprint(swagger_bp)  

if __name__ == '__main__':
    app.run(debug=True)