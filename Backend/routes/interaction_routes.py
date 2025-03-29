from flask_restx import Namespace, Resource, fields
from models.interaction import TuongTac
from models.database import db

# Tạo namespace cho tương tác
interaction_ns = Namespace('interactions', description='Interaction related operations')

# Định nghĩa model dữ liệu cho Swagger
interaction_model = interaction_ns.model('Interaction', {
    'UserID': fields.Integer(required=True, description='ID của người dùng'),
    'ProductID': fields.Integer(required=True, description='ID của sản phẩm'),
    'InteractionType': fields.String(required=True, description='Loại tương tác (view, wishlist, rating)'),
    'Rating': fields.Integer(description='Đánh giá sản phẩm (1-5)'),
    'SoLanXem': fields.Integer(description='Số lần xem sản phẩm'),
    'ThoiGianXem': fields.Integer(description='Thời gian xem sản phẩm (giây)')
})

@interaction_ns.route('/')
class InteractionList(Resource):
    @interaction_ns.expect(interaction_model)
    @interaction_ns.doc('add_interaction')
    def post(self):
        """Ghi nhận tương tác mới"""
        data = interaction_ns.payload
        new_interaction = TuongTac(
            UserID=data['UserID'],
            ProductID=data['ProductID'],
            InteractionType=data['InteractionType'],
            Rating=data.get('Rating'),
            SoLanXem=data.get('SoLanXem', 1),
            ThoiGianXem=data.get('ThoiGianXem', 0)
        )
        db.session.add(new_interaction)
        db.session.commit()
        return {'message': 'Tương tác đã được ghi nhận thành công!', 'InteractionID': new_interaction.InteractionID}, 201

@interaction_ns.route('/<int:user_id>')
@interaction_ns.param('user_id', 'ID của người dùng')
class UserInteractions(Resource):
    @interaction_ns.doc('get_user_interactions')
    def get(self, user_id):
        """Lấy danh sách tương tác của người dùng"""
        interactions = TuongTac.query.filter_by(UserID=user_id).all()
        return [{
            'InteractionID': interaction.InteractionID,
            'UserID': interaction.UserID,
            'ProductID': interaction.ProductID,
            'InteractionType': interaction.InteractionType,
            'Rating': interaction.Rating,
            'SoLanXem': interaction.SoLanXem,
            'ThoiGianXem': interaction.ThoiGianXem
        } for interaction in interactions]

@interaction_ns.route('/delete/<int:interaction_id>')
@interaction_ns.param('interaction_id', 'ID của tương tác')
class Interaction(Resource):
    @interaction_ns.doc('delete_interaction')
    def delete(self, interaction_id):
        """Xóa một tương tác"""
        interaction = TuongTac.query.get(interaction_id)
        if not interaction:
            return {'message': 'Tương tác không tồn tại!'}, 404
        db.session.delete(interaction)
        db.session.commit()
        return {'message': 'Tương tác đã được xóa thành công!'}