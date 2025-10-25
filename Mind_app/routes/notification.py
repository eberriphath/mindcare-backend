from flask import Blueprint, jsonify, request
from model import Notification, db

notifications_bp = Blueprint('notifications', __name__, url_prefix='/notifications')

@notifications_bp.get('/')
def get_notifications():
    notifications = Notification.query.all()
    return jsonify([n.serialize() for n in notifications]), 200

@notifications_bp.post('/')
def create_notification():
    data = request.get_json()
    new_notification = Notification(
        user_id=data.get('user_id'),
        message=data.get('message'),
        type=data.get('type'),
        status=data.get('status', 'unread')
    )
    db.session.add(new_notification)
    db.session.commit()
    return jsonify(new_notification.serialize()), 201
