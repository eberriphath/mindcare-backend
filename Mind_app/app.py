from flask import Flask, jsonify, request
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_restful import Api, Resource
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_jwt_extended import JWTManager
from flask_mail import Mail, Message
from model import db
from dotenv import load_dotenv
import os
load_dotenv()


app = Flask(__name__)


app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///mindcare.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False


db.init_app(app)
migrate = Migrate(app, db)
bcrypt = Bcrypt(app)
CORS(app)
api = Api(app)
jwt = JWTManager(app)
mail = Mail(app)


@app.route('/send')
def send():
    message = Message(
        subject="Hello from MindCare App",
        recipients=["test.mailtrap1234@gmail.com"],
        sender=('Paul from MindCare', 'paul@mailtrap.club')
    )
    message.body = "This is a test email sent from the MindCare Flask application using Mailtrap."
    mail.send(message)
    return "Email sent successfully!"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
