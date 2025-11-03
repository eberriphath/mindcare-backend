from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default="user")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    client = db.relationship("Client", backref="user", uselist=False)
    therapist = db.relationship("Therapist", backref="user", uselist=False)
    admin = db.relationship("Admin", backref="user", uselist=False)

    def serialize(self):
        return {
            "id": self.id,
            "full_name": self.full_name,
            "email": self.email,
            "role": self.role,
            "created_at": self.created_at.isoformat(),
        }


class Client(db.Model):
    __tablename__ = "clients"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    date_of_birth = db.Column(db.String(20))
    contact = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    


class Centre(db.Model):
    __tablename__ = "centres"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    address = db.Column(db.String(255))
    contact = db.Column(db.String(255))
    email = db.Column(db.String(255))      # If you need email
    website = db.Column(db.String(255))    # If you need website
    description = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=db.func.now())


class Therapist(db.Model):
    __tablename__ = "therapists"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    specialization = db.Column(db.String(100))
    experience_years = db.Column(db.Integer)
    centre_id = db.Column(db.Integer, db.ForeignKey("centres.id"))


class Admin(db.Model):
    __tablename__ = "admins"
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"))
    permissions = db.Column(db.String(200), default="all")

