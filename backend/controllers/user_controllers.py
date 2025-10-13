from flask import jsonify
from models import db, User

def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "phone": user.phone,
        "avatar": user.avatar
    }), 200

def update_user_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    
    for field in ["username", "email", "phone", "avatar"]:
        if field in data:
            setattr(user, field, data[field])
    
    db.session.commit()
    return jsonify({"message": "Profile updated successfully"}), 200

def delete_user_account(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": "Account deleted successfully"}), 200
