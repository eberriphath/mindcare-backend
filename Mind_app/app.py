from flask import Flask
from model import db
from routes.users import user_bp
from routes.clients import client_bp
from routes.therapists import therapist_bp
from routes.admin import admin_bp
from routes.center import centres_bp 
from routes.session import sessions_bp 
from routes.progess import progress_bp
from routes.notification import notifications_bp

from flask_jwt_extended import JWTManager

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql+psycopg2://postgres.sggwzzmuagyrpxhdljid:JFU5ZfOEbimX5VbP@aws-1-eu-north-1.pooler.supabase.com:5432/postgres"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'your-secret-key'

db.init_app(app)
jwt = JWTManager(app)


app.register_blueprint(user_bp)
app.register_blueprint(client_bp)
app.register_blueprint(therapist_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(progress_bp)
app.register_blueprint(sessions_bp )
app.register_blueprint(centres_bp  )

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
