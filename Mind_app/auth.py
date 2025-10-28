from flask import Blueprint, request, jsonify
from model import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token  

bcrypt = Bcrypt()
auth_bp = Blueprint('auth', __name__)


@auth_bp.post('/register')
def register():
    data = request.get_json()
    full_name = data.get('name')
    email = data.get('email')
    password = data.get('password')

    if not all([full_name, email, password]):
        return jsonify({"message": "Missing fields"}), 400

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({"message": "User already exists"}), 400

    new_user = User(full_name=full_name, email=email)
    new_user.password = password
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "User registered successfully"}), 201



@auth_bp.post('/login')
def login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not all([email, password]):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not user.authenticate(password):
        return jsonify({"message": "Invalid email or password"}), 401

    access_token = create_access_token(identity=user.id)  
    return jsonify({
        "access_token": access_token,
        "user": user.serialize()
    }), 200
