from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from flask_bcrypt import Bcrypt
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
bcrypt = Bcrypt()

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column("password", db.String(128), nullable=False)
    role = db.Column(db.String(50), nullable=False, default='user')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client = db.relationship('Client', back_populates='user', uselist=False, passive_deletes=True)
    admin = db.relationship('Admin', back_populates='user', uselist=False, passive_deletes=True)
    therapist = db.relationship('Therapist', back_populates='user', uselist=False, passive_deletes=True)
    notification = db.relationship('Notification', back_populates='user', passive_deletes=True)
    

    @hybrid_property
    def password(self):
        return self.password_hash

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def serialize(self):
        return {
            'id': self.id,
            'full_name': self.full_name,
            'email': self.email,
            'role': self.role,
            'created_at': self.created_at.isoformat()
        }  

    @validates('email')
    def validate_email(self, key, email):
        if not email or '@' not in email:
            raise ValueError('Invalid email address format')
        return email
    
     
class Client(db.Model, SerializerMixin):
    __tablename__ = 'clients'
    
    id = db.Column(db.Integer, primary_key=True)
    date_of_birth = db.Column(db.Date, nullable=False)
    contact = db.Column(db.String(120), unique=True, nullable=False)
    gender = db.Column(db.String(50), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    user = db.relationship('User', back_populates='client')
    sessions = db.relationship('Session', back_populates='client', passive_deletes=True)
    progress = db.relationship('Progress', back_populates='client', passive_deletes=True)

    def serialize(self):
        return {
            'id': self.id,
            'date_of_birth': self.date_of_birth.isoformat(),
            'contact': self.contact,
            'gender' : self.gender
        } 
class Admin(db.Model, SerializerMixin):
    __tablename__ = 'admins'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    permissions = db.Column(db.String(250), nullable=True)
    user = db.relationship('User', back_populates='admin')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'permissions': self.permissions
        }  
class Therapist(db.Model, SerializerMixin):
    __tablename__ = 'therapists'
    
    id = db.Column(db.Integer, primary_key=True)
    specialization = db.Column(db.String(120), nullable=False)
    experience_years = db.Column(db.Integer, nullable=False)
    availability = db.Column(db.Boolean, default=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, unique=True, index=True)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id', ondelete='CASCADE'), nullable=False, index=True) 
    user = db.relationship('User', back_populates='therapist')
    centre = db.relationship('Centre', back_populates='therapist')
    sessions = db.relationship('Session', back_populates='therapist', passive_deletes=True)

    def serialize(self):
        return {
            'id': self.id,
            'specialization': self.specialization,
            'experience_years': self.experience_years,
            'availability': self.availability
        }  
class Centre(db.Model, SerializerMixin):
    __tablename__ = 'centres'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    address = db.Column(db.String(250), nullable=False)
    town = db.Column(db.String(100), nullable=False)
    contact = db.Column(db.String(50), nullable=False)
    description = db.Column(db.Text, nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)
    therapist = db.relationship('Therapist', back_populates='centre', passive_deletes=True)
    sessions = db.relationship('Session', back_populates='centre', passive_deletes=True)

    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'address': self.address,
            'contact': self.contact,
            'description': self.description,
            'latitude': self.latitude,
            'longitude': self.longitude
        } 
class Session(db.Model, SerializerMixin):
    __tablename__ = 'sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False, index=True)
    therapist_id = db.Column(db.Integer, db.ForeignKey('therapists.id', ondelete='CASCADE'), nullable=False, index=True)
    centre_id = db.Column(db.Integer, db.ForeignKey('centres.id', ondelete='CASCADE'), nullable=False, index=True)
    date = db.Column(db.DateTime, nullable=False)
    time = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False, default='scheduled')
    notes = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    progress = db.relationship('Progress', back_populates='session', passive_deletes=True)
    client = db.relationship('Client', back_populates='sessions')
    therapist = db.relationship('Therapist', back_populates='sessions')
    centre = db.relationship('Centre', back_populates='sessions')

    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'therapist_id': self.therapist_id,
            'centre_id': self.centre_id,
            'date': self.date.isoformat(),
            'time': self.time,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat()
        } 
class Progress(db.Model, SerializerMixin):
    __tablename__ = 'progress'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('clients.id', ondelete='CASCADE'), nullable=False, index=True)
    session_id = db.Column(db.Integer, db.ForeignKey('sessions.id', ondelete='CASCADE'), nullable=False, index=True)
    mood = db.Column(db.String(50), nullable=False)
    reflections = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    client = db.relationship('Client', back_populates='progress')
    session = db.relationship('Session', back_populates='progress')

    def serialize(self):
        return {
            'id': self.id,
            'client_id': self.client_id,
            'session_id': self.session_id,
            'mood': self.mood,
            'reflections': self.reflections,
            'created_at': self.created_at.isoformat()
        }
class Notification(db.Model, SerializerMixin):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50), nullable=False)
    status = db.Column(db.String(50), nullable=False, default='unread')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user = db.relationship('User', back_populates='notification')

    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'message': self.message,
            'type': self.type,
            'status': self.status,
            'created_at': self.created_at.isoformat()
        }



    