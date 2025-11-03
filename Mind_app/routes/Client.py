from flask import Blueprint, request, jsonify
from model import db, User, Client
from flask_bcrypt import check_password_hash

client_bp = Blueprint("client_bp", __name__, url_prefix="/client")

@client_bp.route("/login", methods=["POST"])
def client_login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password are required"}), 400

    user = User.query.filter_by(email=email, role="client").first()
    if not user or not check_password_hash(user.password, password):
        return jsonify({"error": "Invalid credentials"}), 400

    client = Client.query.filter_by(user_id=user.id).first()
    if not client:
        return jsonify({"error": "Client profile not found"}), 404

    token = f"token-client-{user.id}"

    return jsonify({
        "message": "✅ Client login successful!",
        "user": user.serialize(),
        "client": client.serialize(),
        "access_token": token
    }), 200
