from flask import Blueprint, jsonify, request
from model import Session, db


sessions_bp = Blueprint('sessions', __name__, url_prefix='/sessions')

@sessions_bp.get('/')
def get_sessions():
    sessions = Session.query.all()
    return jsonify([s.serialize() for s in sessions]), 200

@sessions_bp.post('/')
def create_session():
    data = request.get_json()
    new_session = Session(
        client_id=data.get('client_id'),
        therapist_id=data.get('therapist_id'),
        centre_id=data.get('centre_id'),
        date=data.get('date'),
        time=data.get('time'),
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify(new_session.serialize()), 201
