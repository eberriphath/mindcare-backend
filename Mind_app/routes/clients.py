from flask import Blueprint, jsonify, request
from model import db, Client
from flask_jwt_extended import jwt_required

client_bp = Blueprint('client', __name__)


@client_bp.get('/clients')
@jwt_required()
def get_clients():
    clients = Client.query.all()
    return jsonify([client.serialize() for client in clients]), 200



@client_bp.get('/clients/<int:id>')
@jwt_required()
def get_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404
    return jsonify(client.serialize()), 200



@client_bp.post('/clients')
@jwt_required()
def create_client():
    data = request.get_json()

    
    required_fields = ['date_of_birth', 'contact', 'gender', 'user_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    
    new_client = Client(
        date_of_birth=data['date_of_birth'],
        contact=data['contact'],
        gender=data['gender'],
        user_id=data['user_id']
    )

    db.session.add(new_client)
    db.session.commit()
    return jsonify({"message": "Client created successfully", "client": new_client.serialize()}), 201

@client_bp.patch('/clients/<int:id>')
@jwt_required()
def update_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    data = request.get_json()
    if 'date_of_birth' in data:
        client.date_of_birth = data['date_of_birth']
    if 'contact' in data:
        client.contact = data['contact']
    if 'gender' in data:
        client.gender = data['gender']

    db.session.commit()
    return jsonify({"message": "Client updated successfully", "client": client.serialize()}), 200


@client_bp.delete('/clients/<int:id>')
@jwt_required()
def delete_client(id):
    client = Client.query.get(id)
    if not client:
        return jsonify({"error": "Client not found"}), 404

    db.session.delete(client)
    db.session.commit()
    return jsonify({"message": "Client deleted successfully"}), 200
