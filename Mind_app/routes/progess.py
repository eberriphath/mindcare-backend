from flask import Blueprint, jsonify, request
from model import Progress, db
from flask_jwt_extended import jwt_required

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')

@progress_bp.get('/')
@jwt_required()
def get_progress():
    all_progress = Progress.query.all()
    return jsonify([p.serialize() for p in all_progress]), 200

@progress_bp.post('/')
@jwt_required()
def create_progress():
    data = request.get_json()
    new_progress = Progress(
        client_id=data.get('client_id'),
        session_id=data.get('session_id'),
        mood=data.get('mood'),
        reflections=data.get('reflections')
    )
    db.session.add(new_progress)
    db.session.commit()
    return jsonify(new_progress.serialize()), 201
