from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
import os

from model import db, User, Client, Admin, Therapist, Notification, Centre, Session, Progress
from routes.users import user_bp
from flask import Flask
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from datetime import timedelta
from dotenv import load_dotenv
import os

from model import db, User, Client, Admin, Therapist, Notification, Centre, Session, Progress
from routes.users import user_bp
from routes.clients import client_bp
from routes.therapists import therapist_bp
from routes.admin import admin_bp
from routes.center import centres_bp
from routes.session import sessions_bp
from routes.progess import progress_bp
from routes.notification import notifications_bp
from auth import auth_bp

load_dotenv()

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL", "sqlite:///mindcare.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "your-secret-key")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)

db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
api = Api(app)
CORS(app)
jwt = JWTManager(app)

app.register_blueprint(auth_bp)
app.register_blueprint(user_bp)
app.register_blueprint(client_bp)
app.register_blueprint(therapist_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(centres_bp)

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        print("Database tables created successfully!")
        print("Connected to:", app.config["SQLALCHEMY_DATABASE_URI"])
    app.run(debug=True)
