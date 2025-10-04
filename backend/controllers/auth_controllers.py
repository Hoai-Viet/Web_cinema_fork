from models import db, User
from datetime import datetime, date
from flask import jsonify, session

def signup_user(data):
    required_fields = ["username", "email", "password", "confirm_password", "birthdate"]
    for field in required_fields:
        if field not in data:
            return jsonify({"message": f"{field} is required"}), 400

    if User.query.filter_by(email=data["email"]).first():
        return jsonify({"message": "Email already exists"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"message": "Passwords do not match"}), 400

    # Xử lý ngày sinh
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
        password=data["password"],  # plain text (demo)
        birthday=birthdate
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"message": "User created", "id": user.id}), 201


def login_user(data):
    if not data or not all(k in data for k in ("email", "password")):
        return jsonify({"message": "Missing email or password"}), 400

    user = User.query.filter_by(email=data["email"]).first()
    if user and user.password == data["password"]:
        session["user_id"] = user.id
        return jsonify({"message": "Login successful", "user_id": user.id}), 200
    return jsonify({"message": "Invalid credentials"}), 401


def logout_user():
    session.pop("user_id", None)
    return jsonify({"message": "Logout successful"}), 200


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
