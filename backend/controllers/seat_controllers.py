from flask import jsonify, request
from models import db, Seat

# ---------------------------
# Lấy danh sách ghế
# ---------------------------
def get_seats():
    seats = Seat.query.all()
    result = []
    for seat in seats:
        result.append({
            "id": seat.id,
            "room_id": seat.room_id,
            "seat_number": seat.seat_number,
            "seat_type": seat.seat_type
        })
    return jsonify(result)

# ---------------------------
# Lấy chi tiết ghế theo ID
# ---------------------------
def get_seat(seat_id):
    seat = Seat.query.get(seat_id)
    if not seat:
        return jsonify({"message": "Seat not found"}), 404

    return jsonify({
        "id": seat.id,
        "room_id": seat.room_id,
        "seat_number": seat.seat_number,
        "seat_type": seat.seat_type
    })

# ---------------------------
# Thêm ghế mới
# ---------------------------
def create_seat():
    data = request.get_json()
    if not data or not all(k in data for k in ("room_id", "seat_number", "seat_type")):
        return jsonify({"message": "Missing required fields"}), 400

    new_seat = Seat(
        room_id=data["room_id"],
        seat_number=data["seat_number"],
        seat_type=data["seat_type"]
    )
    db.session.add(new_seat)
    db.session.commit()

    return jsonify({"message": "Seat created successfully", "seat_id": new_seat.id}), 201

# ---------------------------
# Cập nhật ghế
# ---------------------------
def update_seat(seat_id):
    seat = Seat.query.get(seat_id)
    if not seat:
        return jsonify({"message": "Seat not found"}), 404

    data = request.get_json()
    if "seat_number" in data:
        seat.seat_number = data["seat_number"]
    if "seat_type" in data:
        seat.seat_type = data["seat_type"]

    db.session.commit()
    return jsonify({"message": "Seat updated successfully"})

# ---------------------------
# Xóa ghế
# ---------------------------
def delete_seat(seat_id):
    seat = Seat.query.get(seat_id)
    if not seat:
        return jsonify({"message": "Seat not found"}), 404

    db.session.delete(seat)
    db.session.commit()
    return jsonify({"message": "Seat deleted successfully"})
