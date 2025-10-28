from flask import Blueprint, jsonify, request
from model import Notification, db
from flask_jwt_extended import jwt_required

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')


@notifications_bp.get('/')
@jwt_required()
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([n.serialize() for n in notifications]), 200


@notifications_bp.get('/<int:id>')
@jwt_required()
def get_notification(id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404
    return jsonify(notification.serialize()), 200


@notifications_bp.post('/')
@jwt_required()
def create_notification():
    data = request.get_json()
    
    required_fields = ['user_id', 'message', 'type']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_notification = Notification(
        user_id=data['user_id'],
        message=data['message'],
        type=data['type'],
        status=data.get('status', 'unread')
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify({"message": "Notification created successfully", "notification": new_notification.serialize()}), 201


@notifications_bp.patch('/<int:id>')
@jwt_required()
def update_notification(id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    data = request.get_json()
    for field in ['user_id', 'message', 'type', 'status']:
        if field in data:
            setattr(notification, field, data[field])

    db.session.commit()
    return jsonify({"message": "Notification updated successfully", "notification": notification.serialize()}), 200


@notifications_bp.delete('/<int:id>')
@jwt_required()
def delete_notification(id):
    notification = Notification.query.get(id)
    if not notification:
        return jsonify({"error": "Notification not found"}), 404

    db.session.delete(notification)
    db.session.commit()
    return jsonify({"message": "Notification deleted successfully"}), 200

