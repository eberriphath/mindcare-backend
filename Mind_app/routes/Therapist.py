from flask import Blueprint, request, jsonify
from model import db, User, Therapist
from flask_bcrypt import check_password_hash

therapist_bp = Blueprint("therapist", __name__, url_prefix="/therapist")

@therapist_bp.route("/login", methods=["POST"])
def therapist_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email, role="therapist").first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    therapist = Therapist.query.filter_by(user_id=user.id).first()
    if not therapist:
        return jsonify({"error": "Therapist profile not found"}), 404

    token = f"token-therapist-{user.id}"

    return jsonify({
        "message": "✅ Therapist login successful!",
        "user": user.serialize(),
        "therapist": therapist.serialize(),
        "access_token": token
    }), 200
