from flask import Blueprint, jsonify, request
from model import Centre, db


centres_bp = Blueprint('centres', __name__, url_prefix='/centres')

@centres_bp.get('/')
def get_centres():
    centres = Centre.query.all()
    return jsonify([c.serialize() for c in centres]), 200

@centres_bp.post('/')

def create_centre():
    data = request.get_json()
    new_centre = Centre(
        name=data.get('name'),
        address=data.get('address'),
        town=data.get('town'),
        contact=data.get('contact'),
        description=data.get('description'),
        latitude=data.get('latitude'),
        longitude=data.get('longitude')
    )
    db.session.add(new_centre)
    db.session.commit()
    return jsonify(new_centre.serialize()), 201
