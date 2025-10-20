from flask import Blueprint, jsonify, request
from model import User, db
from flask_jwt_extended import jwt_required, get_jwt_identity

user_bp = Blueprint('user', __name__)

@user_bp.get('/users')
@jwt_required()  
def get_users():
    users = User.query.all()
    return jsonify([user.serialize() for user in users]), 200



@user_bp.get('/users/<int:id>')
@jwt_required()
def get_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify(user.serialize()), 200



@user_bp.patch('/users/<int:id>')
@jwt_required()
def update_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    data = request.get_json()
    if 'full_name' in data:
        user.full_name = data['full_name']
    if 'email' in data:
        user.email = data['email']
    if 'role' in data:
        user.role = data['role']

    db.session.commit()
    return jsonify({"message": "User updated successfully", "user": user.serialize()}), 200



@user_bp.delete('/users/<int:id>')
@jwt_required()
def delete_user(id):
    user = User.query.get(id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "User deleted successfully"}), 200
