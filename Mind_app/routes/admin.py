from flask import Blueprint, jsonify, request
from model import db, Admin


admin_bp = Blueprint('admin', __name__)


@admin_bp.get('/admins')
def get_admins():
    admins = Admin.query.all()
    return jsonify([admin.serialize() for admin in admins]), 200



@admin_bp.get('/admins/<int:id>')
def get_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({"error": "Admin not found"}), 404
    return jsonify(admin.serialize()), 200



@admin_bp.post('/admins')
def create_admin():
    data = request.get_json()

    
    required_fields = ['user_id']
    if not all(field in data for field in required_fields):
        return jsonify({"error": "Missing required fields"}), 400

    new_admin = Admin(
        user_id=data['user_id'],
        permissions=data.get('permissions')
    )

    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"message": "Admin created successfully", "admin": new_admin.serialize()}), 201



@admin_bp.patch('/admins/<int:id>')
def update_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    data = request.get_json()
    if 'permissions' in data:
        admin.permissions = data['permissions']

    db.session.commit()
    return jsonify({"message": "Admin updated successfully", "admin": admin.serialize()}), 200



@admin_bp.delete('/admins/<int:id>')
def delete_admin(id):
    admin = Admin.query.get(id)
    if not admin:
        return jsonify({"error": "Admin not found"}), 404

    db.session.delete(admin)
    db.session.commit()
    return jsonify({"message": "Admin deleted successfully"}), 200
