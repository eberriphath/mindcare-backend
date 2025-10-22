from flask import Blueprint, jsonify, request
from model import User, db, bcrypt
from flask_jwt_extended import create_access_token, jwt_required
from datetime import timedelta


user_bp = Blueprint('user', __name__, url_prefix="/user")


@user_bp.post('/register')
def register_user():
    data = request.get_json()
    name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not name or not email or not password:
        return jsonify({"message": "All fields are required."}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"message": "Email already registered."}), 400

    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    new_user = User(full_name=name, email=email, password_hash=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registration successful!"}), 201



@user_bp.post('/login')
def login_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user = User.query.filter_by(email=email).first()
    if not user or not bcrypt.check_password_hash(user.password_hash, password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
    return jsonify({
        "message": "Login successful!",
        "access_token": access_token,
        "user": user.serialize()
    }), 200



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

