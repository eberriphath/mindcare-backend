import os
from flask import Flask, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from model import db
from auth import auth_bp

# Load .env file
load_dotenv()

# Optional blueprints
try:
    from routes.Client import client_bp
    from routes.Therapist import therapist_bp
    from routes.Admin import admin_bp
    from routes.Centre import centre_bp
except ModuleNotFoundError as e:
    print(f"⚠️ Warning: {e}")

def create_app():
    # Ensure instance folder exists
    instance_path = os.path.join(os.path.dirname(__file__), "instance")
    os.makedirs(instance_path, exist_ok=True)

    app = Flask(__name__, instance_path=instance_path)
    CORS(app)

    # ✅ Load configurations
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL", "sqlite:///" + os.path.join(instance_path, "mindcare.db")
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "supersecretkey")
    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "mindcarejwtsecret")

    # ✅ Initialize extensions
    db.init_app(app)
    Migrate(app, db)
    JWTManager(app)

    # ✅ Register blueprints
    app.register_blueprint(auth_bp)
    for bp in [client_bp, therapist_bp, admin_bp, centre_bp]:
        try:
            app.register_blueprint(bp)
        except Exception as e:
            print(f"Skipping blueprint {bp}: {e}")

    @app.route("/portal")
    def home():
        return jsonify({"message": "✅ MindCare API is running!"})

    # ✅ Create tables if not exist
    with app.app_context():
        db.create_all()

    return app


if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
