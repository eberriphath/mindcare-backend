from flask import Blueprint, jsonify, request
from model import Session, db
from flask_jwt_extended import jwt_required

sessions_bp = Blueprint('sessions', __name__, url_prefix='/sessions')


@sessions_bp.get('/')
@jwt_required()
def get_sessions():
    sessions = Session.query.all()
    return jsonify([s.serialize() for s in sessions]), 200


@sessions_bp.get('/<int:id>')
@jwt_required()
def get_session(id):
    session = Session.query.get(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404
    return jsonify(session.serialize()), 200


@sessions_bp.post('/')
@jwt_required()
def create_session():
    data = request.get_json()
    
    required_fields = ['client_id', 'therapist_id', 'centre_id', 'date', 'time']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_session = Session(
        client_id=data['client_id'],
        therapist_id=data['therapist_id'],
        centre_id=data['centre_id'],
        date=data['date'],
        time=data['time'],
        status=data.get('status', 'scheduled'),
        notes=data.get('notes')
    )
    db.session.add(new_session)
    db.session.commit()
    return jsonify({"message": "Session created successfully", "session": new_session.serialize()}), 201


@sessions_bp.patch('/<int:id>')
@jwt_required()
def update_session(id):
    session = Session.query.get(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    data = request.get_json()
    for field in ['client_id', 'therapist_id', 'centre_id', 'date', 'time', 'status', 'notes']:
        if field in data:
            setattr(session, field, data[field])

    db.session.commit()
    return jsonify({"message": "Session updated successfully", "session": session.serialize()}), 200


@sessions_bp.delete('/<int:id>')
@jwt_required()
def delete_session(id):
    session = Session.query.get(id)
    if not session:
        return jsonify({"error": "Session not found"}), 404

    db.session.delete(session)
    db.session.commit()
    return jsonify({"message": "Session deleted successfully"}), 200
