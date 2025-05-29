from flask_restx import Namespace, Resource, fields
from models.user import NguoiDung
from models.database import db

# Tạo namespace cho người dùng
user_ns = Namespace('users', description='User related operations')

# Định nghĩa model dữ liệu cho Swagger
user_model = user_ns.model('User', {
    'Ten': fields.String(required=True, description='Tên người dùng'),
    'Email': fields.String(required=True, description='Email người dùng'),
    'Pass': fields.String(required=True, description='Mật khẩu người dùng'),
    'Role': fields.String(default='user', description='Vai trò người dùng'),
    'Age': fields.Integer(description='Tuổi người dùng')
})

# Định nghĩa model đăng nhập cho Swagger
login_model = user_ns.model('Login', {
    'email': fields.String(required=True, description='Email người dùng'),
    'password': fields.String(required=True, description='Mật khẩu người dùng')
})

@user_ns.route('/')
class UserList(Resource):
    @user_ns.doc('get_users')
    def get(self):
        """Lấy danh sách người dùng"""
        users = NguoiDung.query.all()
        return [{
            'UserID': user.UserID,
            'Ten': user.Ten,
            'Email': user.Email,
            'Role': user.Role,
            'Age': user.Age
        } for user in users]

    @user_ns.expect(user_model)
    @user_ns.doc('add_user')
    def post(self):
        """Thêm người dùng mới"""
        data = user_ns.payload
        new_user = NguoiDung(
            Ten=data['Ten'],
            Email=data['Email'],
            Pass=data['Pass'],
            Role=data.get('Role', 'user'),
            Age=data.get('Age')
        )
        db.session.add(new_user)
        db.session.commit()
        return {'message': 'Người dùng đã được thêm thành công!', 'UserID': new_user.UserID}, 201

@user_ns.route('/<int:user_id>')
@user_ns.param('user_id', 'ID của người dùng')
class User(Resource):
    @user_ns.doc('get_user_by_id')
    def get(self, user_id):
        """Lấy thông tin người dùng theo ID"""
        user = NguoiDung.query.get(user_id)
        if not user:
            return {'message': 'Người dùng không tồn tại!'}, 404
        return {
            'UserID': user.UserID,
            'Ten': user.Ten,
            'Email': user.Email,
            'Role': user.Role,
            'Age': user.Age
        }

    @user_ns.doc('delete_user')
    def delete(self, user_id):
        """Xóa người dùng theo ID"""
        user = NguoiDung.query.get(user_id)
        if not user:
            return {'message': 'Người dùng không tồn tại!'}, 404
        db.session.delete(user)
        db.session.commit()
        return {'message': 'Người dùng đã được xóa thành công!'}

    @user_ns.expect(user_model)
    @user_ns.doc('update_user')
    def put(self, user_id):
        """Cập nhật thông tin người dùng"""
        user = NguoiDung.query.get(user_id)
        if not user:
            return {'message': 'Người dùng không tồn tại!'}, 404
        data = user_ns.payload
        user.Ten = data.get('Ten', user.Ten)
        user.Email = data.get('Email', user.Email)
        user.Pass = data.get('Pass', user.Pass)
        user.Role = data.get('Role', user.Role)
        user.Age = data.get('Age', user.Age)
        db.session.commit()
        return {'message': 'Thông tin người dùng đã được cập nhật thành công!'}

@user_ns.route('/login')
class UserLogin(Resource):
    @user_ns.expect(login_model)
    @user_ns.doc('user_login')
    def post(self):
        """Đăng nhập người dùng"""
        data = user_ns.payload
        email = data.get('email')
        password = data.get('password')
        
        if not email or not password:
            return {'status': 'error', 'message': 'Email và mật khẩu không được để trống!'}, 400
        
        # Tìm người dùng theo email
        user = NguoiDung.query.filter_by(Email=email).first()
        
        if not user:
            return {'status': 'error', 'message': 'Email không tồn tại trong hệ thống!'}, 404
        
        # Kiểm tra mật khẩu (trong thực tế nên sử dụng hash)
        if user.Pass != password:
            return {'status': 'error', 'message': 'Mật khẩu không đúng!'}, 401
        
        return {
            'status': 'success',
            'message': 'Đăng nhập thành công!',
            'user': {
                'UserID': user.UserID,
                'Ten': user.Ten,
                'Email': user.Email,
                'VaiTro': user.Role,
                'Tuoi': user.Age
            }
        }, 200