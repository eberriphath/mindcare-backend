from flask import Blueprint, jsonify, request
from model import Progress, db
from flask_jwt_extended import jwt_required

progress_bp = Blueprint('progress', __name__, url_prefix='/progress')


@progress_bp.get('/')
@jwt_required()
def get_progress():
    all_progress = Progress.query.all()
    return jsonify([p.serialize() for p in all_progress]), 200


@progress_bp.get('/<int:id>')
@jwt_required()
def get_single_progress(id):
    progress = Progress.query.get(id)
    if not progress:
        return jsonify({"error": "Progress entry not found"}), 404
    return jsonify(progress.serialize()), 200


@progress_bp.post('/')
@jwt_required()
def create_progress():
    data = request.get_json()
    
    required_fields = ['client_id', 'session_id', 'mood', 'reflections']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_progress = Progress(
        client_id=data['client_id'],
        session_id=data['session_id'],
        mood=data['mood'],
        reflections=data['reflections']
    )
    db.session.add(new_progress)
    db.session.commit()
    return jsonify({"message": "Progress created successfully", "progress": new_progress.serialize()}), 201


@progress_bp.patch('/<int:id>')
@jwt_required()
def update_progress(id):
    progress = Progress.query.get(id)
    if not progress:
        return jsonify({"error": "Progress entry not found"}), 404

    data = request.get_json()
    for field in ['client_id', 'session_id', 'mood', 'reflections']:
        if field in data:
            setattr(progress, field, data[field])

    db.session.commit()
    return jsonify({"message": "Progress updated successfully", "progress": progress.serialize()}), 200


@progress_bp.delete('/<int:id>')
@jwt_required()
def delete_progress(id):
    progress = Progress.query.get(id)
    if not progress:
        return jsonify({"error": "Progress entry not found"}), 404

    db.session.delete(progress)
    db.session.commit()
    return jsonify({"message": "Progress deleted successfully"}), 200
