from flask import Blueprint, request, jsonify
from model import db, User, Admin
from flask_bcrypt import check_password_hash

admin_bp = Blueprint("admin_bp", __name__, url_prefix="/admin")

@admin_bp.route("/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email, role="admin").first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    admin = Admin.query.filter_by(user_id=user.id).first()
    if not admin:
        return jsonify({"error": "Admin profile not found"}), 404

    token = f"token-admin-{user.id}"

    return jsonify({
        "message": "✅ Admin login successful!",
        "user": user.serialize(),
        "admin": admin.serialize(),
        "access_token": token
    }), 200
