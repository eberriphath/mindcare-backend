from flask import Blueprint, jsonify, request
from model import Centre, db
from flask_jwt_extended import jwt_required

centres_bp = Blueprint('centres', __name__, url_prefix='/centres')


@centres_bp.get('/')
@jwt_required()
def get_centres():
    centres = Centre.query.all()
    return jsonify([c.serialize() for c in centres]), 200


@centres_bp.post('/')
@jwt_required()
def create_centre():
    data = request.get_json()
    
    required_fields = ['name', 'address', 'town', 'contact', 'description', 'latitude', 'longitude']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_centre = Centre(
        name=data['name'],
        address=data['address'],
        town=data['town'],
        contact=data['contact'],
        description=data['description'],
        latitude=data['latitude'],
        longitude=data['longitude']
    )
    db.session.add(new_centre)
    db.session.commit()
    return jsonify({"message": "Centre created successfully", "centre": new_centre.serialize()}), 201
