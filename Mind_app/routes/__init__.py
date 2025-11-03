from flask import Flask
from model import db

def create_app():
    app = Flask(__name__)
    
    # Example SQLite configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mindcare.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Import blueprints/routes here if needed
    # from .auth import auth_bp
    # app.register_blueprint(auth_bp)

    # Create tables automatically
    with app.app_context():
        db.create_all()  # <-- This creates all tables defined in models

    return app
