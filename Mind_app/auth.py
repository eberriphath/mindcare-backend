from flask import Blueprint, request, jsonify
from model import db, User, Client, Therapist, Admin, Centre
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token
from datetime import timedelta

auth_bp = Blueprint("auth", __name__, url_prefix="/auth")


# -------------------------------
# Register endpoint
# -------------------------------
@auth_bp.route("/register", methods=["POST"])
def register_user():
    data = request.get_json()
    full_name = data.get("full_name")
    email = data.get("email")
    password = data.get("password")
    role = data.get("role", "user")

    if not full_name or not email or not password:
        return jsonify({"error": "Missing required fields"}), 400

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 400

    hashed_pw = generate_password_hash(password).decode("utf-8")
    new_user = User(full_name=full_name, email=email, password=hashed_pw, role=role)
    db.session.add(new_user)
    db.session.commit()

    # Create role-specific profile
    if role == "client":
        client = Client(user_id=new_user.id, date_of_birth="2000-01-01", contact="000", gender="other")
        db.session.add(client)
    elif role == "therapist":
        centre = Centre.query.first()
        if not centre:
            centre = Centre(name="Default Centre")
            db.session.add(centre)
            db.session.commit()
        therapist = Therapist(user_id=new_user.id, specialization="General", experience_years=0, centre_id=centre.id)
        db.session.add(therapist)
    elif role == "admin":
        admin = Admin(user_id=new_user.id, permissions="all")
        db.session.add(admin)

    db.session.commit()

    return jsonify({
        "message": "✅ Registered successfully!",
        "user": new_user.serialize()
    }), 201


# -------------------------------
# Login endpoint
# -------------------------------
@auth_bp.route("/login", methods=["POST"])
def login_user():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")
    role = data.get("role")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    if role and user.role != role:
        return jsonify({"error": f"This user is not a {role}"}), 403

    access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=6))

    return jsonify({
        "message": "✅ Login successful!",
        "user": user.serialize(),
        "access_token": access_token
    }), 200
