from flask import Blueprint, request, jsonify
from model import db, MoodEntry
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

mood_bp = Blueprint('mood', __name__, url_prefix='/mood')



@mood_bp.get('/')
@jwt_required()
def get_mood_entries():
    current_user_id = get_jwt_identity()
    entries = MoodEntry.query.filter_by(user_id=current_user_id).all()
    return jsonify([entry.serialize() for entry in entries]), 200



@mood_bp.get('/<int:id>')
@jwt_required()
def get_mood_entry(id):
    current_user_id = get_jwt_identity()
    entry = MoodEntry.query.filter_by(id=id, user_id=current_user_id).first()
    if not entry:
        return jsonify({"error": "Mood entry not found"}), 404
    return jsonify(entry.serialize()), 200



@mood_bp.post('/')
@jwt_required()
def create_mood_entry():
    current_user_id = get_jwt_identity()
    data = request.get_json()
    
    required_fields = ['mood', 'journal']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Mood and journal are required"}), 400

    new_entry = MoodEntry(
        user_id=current_user_id,
        mood=data['mood'],
        journal=data['journal'],
        date=datetime.utcnow()
    )

 

    db.session.add(new_entry)
    db.session.commit()
    return jsonify({"message": "Mood entry created", "entry": new_entry.serialize()}), 201



@mood_bp.put('/<int:id>')
@jwt_required()
def update_mood_entry(id):
    current_user_id = get_jwt_identity()
    entry = MoodEntry.query.filter_by(id=id, user_id=current_user_id).first()
    if not entry:
        return jsonify({"error": "Mood entry not found"}), 404

    data = request.get_json()
    if 'mood' in data:
        entry.mood = data['mood']
    if 'journal' in data:
        entry.journal = data['journal']


    db.session.commit()
    return jsonify({"message": "Mood entry updated", "entry": entry.serialize()}), 200



@mood_bp.delete('/<int:id>')
@jwt_required()
def delete_mood_entry(id):
    current_user_id = get_jwt_identity()
    entry = MoodEntry.query.filter_by(id=id, user_id=current_user_id).first()
    if not entry:
        return jsonify({"error": "Mood entry not found"}), 404

    db.session.delete(entry)
    db.session.commit()
    return jsonify({"message": "Mood entry deleted"}), 200
