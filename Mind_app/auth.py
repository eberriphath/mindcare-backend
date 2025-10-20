from flask import Blueprint, jsonify, request
from model import User, bcrypt, db
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity, get_jwt

auth_bp = Blueprint('auth', __name__)

# Register Route
@auth_bp.post('/register')
def register():
    data = request.get_json()
    
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return jsonify({"error": "Missing required fields"}), 400

    username = data['username']
    email = data['email']
    user = User.query.filter_by(username=username).first()
    existing_email = User.query.filter_by(email=email).first()

    if user:
        return {'error': 'Username already exists, please choose another one'}, 404
    if existing_email:
        return {'error': 'Email already exists, please use a different email address'}, 404

    # Don't hash password manually, let the setter handle it
    new_user = User(username=username, email=email, password=data['password'])
    db.session.add(new_user)
    db.session.commit()

    # Commenting out OTP-related email function
    # send_user_signup_mail(new_user)  # OTP email function can be commented out for now

    
    return jsonify({
        "message": "User registered successfully",
        "user": new_user.serialize()
    }), 200

@auth_bp.post('/login')
def login(): 
    
        username = request.json.get("username")
        password = request.json.get("password")
        id=request.json.get("id")
        user = User.query.filter_by(username=username).first()
        if not user:
            return {"message": "User not found"}, 404
        if not user.authenticate(password):
            return {"message": "Invalid password"}, 401

        access_token = create_access_token(identity=str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))  

        return jsonify({

          
            "access": access_token,
            "refresh": refresh_token
    }), 200