from flask import Flask 
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api
from flask_cors import CORS
from datetime import  timedelta
from flask_jwt_extended import  JWTManager
from model import User, Client, Admin, Therapist, Notification, Centre, Session, Progress, db

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mindcare.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config["JWT_SECRET_KEY"] = "please-remember-to-change-me"
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
jwt = JWTManager(app)

db.init_app(app)
migrate=Migrate(app,db)
CORS(app)
bcrypt=Bcrypt(app)
api = Api(app)