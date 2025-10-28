from flask import Blueprint, jsonify, request
from model import db, Therapist
from flask_jwt_extended import jwt_required

therapist_bp = Blueprint('therapist', __name__, url_prefix="/therapist")


@therapist_bp.get('/')
@jwt_required()
def get_therapists():
    therapists = Therapist.query.all()
    return jsonify([therapist.serialize() for therapist in therapists]), 200


@therapist_bp.get('/<int:id>')
@jwt_required()
def get_therapist(id):
    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"error": "Therapist not found"}), 404
    return jsonify(therapist.serialize()), 200


@therapist_bp.post('/')
@jwt_required()
def create_therapist():
    data = request.get_json()
    required_fields = ['specialization', 'experience_years', 'availability', 'user_id', 'centre_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_therapist = Therapist(
        specialization=data['specialization'],
        experience_years=data['experience_years'],
        availability=data['availability'],
        user_id=data['user_id'],
        centre_id=data['centre_id']
    )

    db.session.add(new_therapist)
    db.session.commit()
    return jsonify({"message": "Therapist created successfully", "therapist": new_therapist.serialize()}), 201


@therapist_bp.patch('/<int:id>')
@jwt_required()
def update_therapist(id):
    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"error": "Therapist not found"}), 404

    data = request.get_json()
    if 'specialization' in data:
        therapist.specialization = data['specialization']
    if 'experience_years' in data:
        therapist.experience_years = data['experience_years']
    if 'availability' in data:
        therapist.availability = data['availability']

    db.session.commit()
    return jsonify({"message": "Therapist updated successfully", "therapist": therapist.serialize()}), 200


@therapist_bp.delete('/<int:id>')
@jwt_required()
def delete_therapist(id):
    therapist = Therapist.query.get(id)
    if not therapist:
        return jsonify({"error": "Therapist not found"}), 404

    db.session.delete(therapist)
    db.session.commit()
    return jsonify({"message": "Therapist deleted successfully"}), 200
