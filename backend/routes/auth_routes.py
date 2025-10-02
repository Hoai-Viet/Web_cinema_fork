from flask import Blueprint, request, jsonify,session
from models import db, User
from datetime import datetime,date 

auth_routes = Blueprint("auth_routes", __name__)

# Đăng ký
@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    if not data or not all(k in data for k in ("username", "email", "password","birthday")):
        return jsonify({"message": "Missing required fields"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    user = User(
        username=data["username"],
        email=data["email"],
        password=data["password"],
        birthday=data["birthday"],
        confirm_password=data["password"]
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "id": user.id}), 201


# Đăng nhập
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.password == data["password"]:
        return jsonify({"message": "Login successful", "user_id": user.id})
    return jsonify({"message": "Invalid credentials"}), 401

@auth_routes.route("/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"})
