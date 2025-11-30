from flask import jsonify, request
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime
from models import db, User, Ticket


# ================================
# GET: Thông tin user hiện tại
# ================================
def get_user_profile(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify({
        "id": user.id,
        "username": user.username,
        "email": user.email,
        "birthday": user.birthday.isoformat() if user.birthday else None,
        "created_at": user.created_at.isoformat(),
    }), 200


# ================================
# PUT: Cập nhật profile user
# ================================
def update_user_profile(user_id, data):
    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # ===== Update Email =====
    if "email" in data:
        new_email = data["email"].strip().lower()

        if not new_email:
            return jsonify({"error": "Email cannot be empty"}), 400

        exists = User.query.filter(
            User.email == new_email,
            User.id != user_id
        ).first()

        if exists:
            return jsonify({"error": "Email already exists"}), 400

        user.email = new_email

    # ===== Update Username =====
    if "username" in data:
        username = data["username"].strip()

        if len(username) < 3:
            return jsonify({"error": "Username must be at least 3 characters"}), 400

        exists = User.query.filter(
            User.username == username,
            User.id != user_id
        ).first()

        if exists:
            return jsonify({"error": "Username already exists"}), 400

        user.username = username

    # ===== Update Birthday =====
    if "birthday" in data:
        try:
            user.birthday = datetime.strptime(data["birthday"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"error": "Invalid date format. Use YYYY-MM-DD"}), 400

    # ===== Save =====
    try:
        db.session.commit()
        return jsonify({"message": "Profile updated successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


# ================================
# DELETE: Xóa tài khoản user
# ================================
def delete_user_account(user_id):
    user = User.query.get(user_id)

    if not user:
        return jsonify({"error": "User not found"}), 404

    try:
        db.session.delete(user)
        db.session.commit()
        return jsonify({"message": "Account deleted successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500


# ================================
# POST: User đổi mật khẩu
# ================================
def change_password(user_id):
    data = request.get_json()
    old_password = data.get("old_password")
    new_password = data.get("new_password")

    if not old_password or not new_password:
        return jsonify({"error": "Missing old_password or new_password"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Kiểm tra mật khẩu cũ (so sánh plaintext)
    if user.password != old_password:
        return jsonify({"error": "Old password is incorrect"}), 400

    # Validate độ dài password mới
    if len(new_password) < 6:
        return jsonify({"error": "Password must be at least 6 characters"}), 400

    try:
        # Lưu thẳng plaintext
        user.password = new_password
        db.session.commit()

        return jsonify({"message": "Password changed successfully"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Database error", "details": str(e)}), 500



# ================================
# GET: Lấy danh sách vé của user
# ================================
def get_user_tickets(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).all()

    result = []
    for t in tickets:
        result.append({
            "ticket_id": t.id,
            "showtime_id": t.showtime_id,
            "seat_id": t.seat_id,
            "ticket_type_id": t.ticket_type_id,
            "price": t.price,
            "quantity": t.quantity,
            "booked_at": t.booked_at.isoformat()
        })

    return jsonify(result), 200