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