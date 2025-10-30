from flask import Blueprint, request, jsonify
from model import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__, url_prefix="/auth")


@auth_bp.post('/register')
def register():
    data = request.get_json()
    full_name = data.get('full_name')
    email = data.get('email')
    password = data.get('password')

    if not all([full_name, email, password]):
        return jsonify({"error": "All fields (full_name, email, password) are required"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400
    if User.query.filter_by(full_name=full_name).first():
        return jsonify({"error": "Full name already registered"}), 400

    new_user = User(full_name=full_name, email=email)
    new_user.password = password  

    db.session.add(new_user)
    db.session.commit()

    access_token = create_access_token(identity=new_user.id)

    return jsonify({
        "message": "User registered successfully",
        "user": new_user.serialize(),
        "access_token": access_token
    }), 201

@auth_bp.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.authenticate(password):
        return jsonify({"error": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)

    return jsonify({
        "message": "Login successful",
        "user": user.serialize(),
        "access_token": access_token
    }), 200


@auth_bp.get('/profile')
@jwt_required()
def profile():
    current_user_id = get_jwt_identity()
    user = User.query.get(current_user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "message": "Profile fetched successfully",
        "user": user.serialize()
    }), 200