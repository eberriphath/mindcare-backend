from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta

from model import db, User, Client, Admin, Therapist, Notification, Centre, Session, Progress

# Import Blueprints
from routes.users import user_bp
from routes.clients import client_bp
from routes.therapists import therapist_bp
from routes.admin import admin_bp
from routes.center import centres_bp 
from routes.session import sessions_bp 
from routes.progess import progress_bp
from routes.notification import notifications_bp


# -------------------- APP CONFIG -------------------- #
app = Flask(__name__)

# --- Database (Supabase/PostgreSQL) ---
app.config['SQLALCHEMY_DATABASE_URI'] = (
    "postgresql+psycopg2://postgres.sggwzzmuagyrpxhdljid:JFU5ZfOEbimX5VbP@"
    "aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# --- JWT Config ---
app.config["JWT_SECRET_KEY"] = "your-secret-key"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

# -------------------- INITIALIZATIONS -------------------- #
db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
jwt = JWTManager(app)

# -------------------- BLUEPRINT REGISTRATION -------------------- #
app.register_blueprint(user_bp)
app.register_blueprint(client_bp)
app.register_blueprint(therapist_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(centres_bp)


# -------------------- MAIN ENTRY -------------------- #
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
