from flask import Blueprint

recommend_bp = Blueprint('recommend_bp', __name__)

@recommend_bp.route('/', methods=['GET'])
def recommend():
    return {"message": "Recommendation API is working!"}