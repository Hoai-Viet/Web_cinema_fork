from datetime import datetime, date, timedelta
from flask import jsonify, request
from flask_jwt_extended import (
    create_access_token, create_refresh_token,
    jwt_required, get_jwt_identity
)
from models import db, User
import re

# ====================== SIGNUP ======================
def signup_user(data):
    required_fields = ["username", "email", "password", "confirm_password", "birthdate"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"message": "Passwords do not match"}), 400

    # Validate password strength (optional)
    if len(data["password"]) < 6:
        return jsonify({"message": "Password must be at least 6 characters"}), 400

    # Validate birthdate
    try:
        birthdate = datetime.strptime(data["birthdate"], "%Y-%m-%d").date()
    except ValueError:
        return jsonify({"message": "Invalid birthdate format. Use YYYY-MM-DD"}), 400

    today = date.today()
    age = today.year - birthdate.year - ((today.month, today.day) < (birthdate.month, birthdate.day))
    if age < 12:
        return jsonify({"message": "You must be at least 12 years old to sign up"}), 400

    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"], 
        birthday=birthdate
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({"message": "User created successfully", "user_id": user.id}), 201


# ====================== LOGIN ======================
def login_user(data):
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.password == data["password"]:
        # Tạo JWT token
        access_token = create_access_token(identity=user.id, expires_delta=timedelta(hours=1))
        refresh_token = create_refresh_token(identity=user.id)

        return jsonify({
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email
            }
        }), 200

    return jsonify({"message": "Invalid credentials"}), 401


# ====================== REFRESH TOKEN ======================
@jwt_required(refresh=True)
def refresh_access_token():
    current_user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=current_user_id, expires_delta=timedelta(hours=1))
    return jsonify({"access_token": new_access_token}), 200


# ====================== GET PROFILE ======================
@jwt_required()
def get_user_profile():
    user_id = get_jwt_identity()
    user = User.query.get(user_id)

    if not user:
        return jsonify({"message": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthday": str(user.birthday)
    }), 200


# ====================== FORGOT PASSWORD ======================
def forgot_password(data):
    if not data or "email" not in data:
        return jsonify({"message": "Missing email"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if not user:
        return jsonify({"message": "Email not found"}), 404

    if "new_password" not in data or "confirm_password" not in data:
        return jsonify({"message": "Please provide new_password and confirm_password"}), 400

    if data["new_password"] != data["confirm_password"]:
        return jsonify({"message": "Passwords do not match"}), 400

    user.password = data["new_password"]
    db.session.commit()
    return jsonify({"message": "Password reset successful"}), 200

def refresh_token():
    user_id = get_jwt_identity()
    new_access_token = create_access_token(identity=user_id)
    return jsonify({
        "access_token": new_access_token
    }), 200
    
def logout_user():
    return jsonify({"message": "Logout successful (client should discard JWT)"}), 200