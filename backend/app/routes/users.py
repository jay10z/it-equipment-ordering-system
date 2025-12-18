from flask import Blueprint, jsonify
from app import db
from app.models import User
from flask_jwt_extended import jwt_required, get_jwt_identity

bp = Blueprint('users', __name__)

def is_admin():
    """Helper function to check if current user is admin"""
    try:
        current_user_id = int(get_jwt_identity())
        user = User.query.get(current_user_id)
        return user and user.is_admin
    except:
        return False

@bp.route('/', methods=['GET'])
@jwt_required()
def get_users():
    """Get all users (Admin only)"""
    if not is_admin():
        return jsonify({'message': 'Admin access required'}), 403
    
    users = User.query.all()
    return jsonify([u.to_dict() for u in users]), 200

# Future: Add delete user endpoint?
