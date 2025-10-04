from flask import Blueprint, request, jsonify
from models import db, Cinema, Room

cinema_routes = Blueprint("cinema_routes", __name__)

# Lấy danh sách rạp chiếu phim
@cinema_routes.route("/cinemas", methods=["GET"])
def get_cinemas():
    cinemas = Cinema.query.all()
    result = []
    for c in cinemas:
        result.append({
            "id": c.id,
            "name": c.name,
            "address": c.address,
            "phone": c.phone
        })
    return jsonify(result)


# Lấy chi tiết 1 rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["GET"])
def get_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    return jsonify({
        "id": cinema.id,
        "name": cinema.name,
        "address": cinema.address,
        "phone": cinema.phone
    })


# Thêm rạp chiếu mới
@cinema_routes.route("/cinemas", methods=["POST"])
def create_cinema():
    data = request.get_json()
    required_fields = ("name", "address")
    if not data or not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    new_cinema = Cinema(
        name=data["name"],
        address=data["address"],
        phone=data.get("phone")
    )
    db.session.add(new_cinema)
    db.session.commit()

    return jsonify({"message": "Cinema created successfully", "id": new_cinema.id}), 201


# Cập nhật rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["PUT"])
def update_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    data = request.get_json()
    if "name" in data:
        cinema.name = data["name"]
    if "address" in data:
        cinema.address = data["address"]
    if "phone" in data:
        cinema.phone = data["phone"]

    db.session.commit()
    return jsonify({"message": "Cinema updated successfully"})


# Xóa rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["DELETE"])
def delete_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    db.session.delete(cinema)
    db.session.commit()
    return jsonify({"message": "Cinema deleted successfully"})

# Lấy danh sách phòng theo cinema
@cinema_routes.route("/cinemas/<cinema_id>/rooms", methods=["GET"])
def get_rooms_by_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    rooms = Room.query.filter_by(cinema_id=cinema_id).all()
    result = []
    for r in rooms:
        result.append({
            "id": r.id,
            "name": r.name,
            "total_seats": r.total_seats
        })

    return jsonify({
        "cinema_id": cinema.id,
        "cinema_name": cinema.name,
        "rooms": result
    })
