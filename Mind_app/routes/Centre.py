# centre.py
from flask import Blueprint, jsonify, request
from model import db, Centre

centre_bp = Blueprint('centre_bp', __name__, url_prefix='/centres')

# ------------------------------------------
# 1️⃣ Get all centres
# ------------------------------------------
@centre_bp.route('/', methods=['GET'])
def get_centres():
    centres = Centre.query.all()
    return jsonify([{
        "id": c.id,
        "name": c.name,
        "location": c.location
    } for c in centres]), 200


# ------------------------------------------
# 2️⃣ Get one centre by ID
# ------------------------------------------
@centre_bp.route('/<int:id>', methods=['GET'])
def get_centre(id):
    centre = Centre.query.get(id)
    if not centre:
        return jsonify({"error": "Centre not found"}), 404

    return jsonify({
        "id": centre.id,
        "name": centre.name,
        "location": centre.location
    }), 200


# ------------------------------------------
# 3️⃣ Create a new centre
# ------------------------------------------
@centre_bp.route('/', methods=['POST'])
def create_centre():
    data = request.get_json()
    name = data.get("name")
    location = data.get("location")

    if not name or not location:
        return jsonify({"error": "Name and location are required"}), 400

    new_centre = Centre(name=name, location=location)
    db.session.add(new_centre)
    db.session.commit()

    return jsonify({
        "message": "Centre created successfully",
        "centre": {
            "id": new_centre.id,
            "name": new_centre.name,
            "location": new_centre.location
        }
    }), 201


# ------------------------------------------
# 4️⃣ Update a centre
# ------------------------------------------
@centre_bp.route('/<int:id>', methods=['PATCH'])
def update_centre(id):
    centre = Centre.query.get(id)
    if not centre:
        return jsonify({"error": "Centre not found"}), 404

    data = request.get_json()
    centre.name = data.get("name", centre.name)
    centre.location = data.get("location", centre.location)

    db.session.commit()

    return jsonify({
        "message": "Centre updated successfully",
        "centre": {
            "id": centre.id,
            "name": centre.name,
            "location": centre.location
        }
    }), 200


# ------------------------------------------
# 5️⃣ Delete a centre
# ------------------------------------------
@centre_bp.route('/<int:id>', methods=['DELETE'])
def delete_centre(id):
    centre = Centre.query.get(id)
    if not centre:
        return jsonify({"error": "Centre not found"}), 404

    db.session.delete(centre)
    db.session.commit()

    return jsonify({"message": "Centre deleted successfully"}), 200
