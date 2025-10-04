from flask import jsonify, request
from models import db, Room

# ---------------------------
# Lấy danh sách phòng
# ---------------------------
def get_rooms():
    rooms = Room.query.all()
    result = []
    for room in rooms:
        result.append({
            "id": room.id,
            "cinema_id": room.cinema_id,
            "name": room.name,
            "total_seats": room.total_seats
        })
    return jsonify(result)

# ---------------------------
# Lấy chi tiết phòng
# ---------------------------
def get_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    return jsonify({
        "id": room.id,
        "cinema_id": room.cinema_id,
        "name": room.name,
        "total_seats": room.total_seats
    })

# ---------------------------
# Thêm phòng
# ---------------------------
def create_room():
    data = request.get_json()
    if not data or not all(k in data for k in ("cinema_id", "name", "total_seats")):
        return jsonify({"message": "Missing required fields"}), 400

    new_room = Room(
        cinema_id=data["cinema_id"],
        name=data["name"],
        total_seats=data["total_seats"]
    )
    db.session.add(new_room)
    db.session.commit()
    return jsonify({"message": "Room created successfully", "room_id": new_room.id}), 201

# ---------------------------
# Cập nhật phòng
# ---------------------------
def update_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    data = request.get_json()
    if "name" in data:
        room.name = data["name"]
    if "total_seats" in data:
        room.total_seats = data["total_seats"]

    db.session.commit()
    return jsonify({"message": "Room updated successfully"})

# ---------------------------
# Xóa phòng
# ---------------------------
def delete_room(room_id):
    room = Room.query.get(room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    db.session.delete(room)
    db.session.commit()
    return jsonify({"message": "Room deleted successfully"})
