from flask import jsonify, request
from models import db, Showtime, Movie, Room, Ticket, Seat

# -------------------------------
# Lấy danh sách tất cả suất chiếu
# -------------------------------
def get_showtimes():
    showtimes = Showtime.query.all()
    result = []
    for s in showtimes:
        result.append({
            "id": s.id,
            "movie_id": s.movie_id,
            "room_id": s.room_id,
            "start_time": s.start_time.isoformat()
        })
    return jsonify(result)

# -------------------------------
# Lấy chi tiết 1 suất chiếu
# -------------------------------
def get_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    return jsonify({
        "id": showtime.id,
        "movie_id": showtime.movie_id,
        "room_id": showtime.room_id,
        "start_time": showtime.start_time.isoformat()
    })

# -------------------------------
# Tạo mới suất chiếu
# -------------------------------
def create_showtime():
    data = request.get_json()
    required_fields = ("movie_id", "room_id", "start_time")
    if not data or not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    movie = Movie.query.get(data["movie_id"])
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    room = Room.query.get(data["room_id"])
    if not room:
        return jsonify({"message": "Room not found"}), 404

    new_showtime = Showtime(
        movie_id=data["movie_id"],
        room_id=data["room_id"],
        start_time=data["start_time"]
    )
    db.session.add(new_showtime)
    db.session.commit()

    return jsonify({"message": "Showtime created successfully", "id": new_showtime.id}), 201

# -------------------------------
# Cập nhật suất chiếu
# -------------------------------
def update_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    data = request.get_json()

    if "movie_id" in data:
        movie = Movie.query.get(data["movie_id"])
        if not movie:
            return jsonify({"message": "Movie not found"}), 404
        showtime.movie_id = data["movie_id"]

    if "room_id" in data:
        room = Room.query.get(data["room_id"])
        if not room:
            return jsonify({"message": "Room not found"}), 404
        showtime.room_id = data["room_id"]

    if "start_time" in data:
        showtime.start_time = data["start_time"]

    db.session.commit()
    return jsonify({"message": "Showtime updated successfully"})

# -------------------------------
# Xóa suất chiếu
# -------------------------------
def delete_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    db.session.delete(showtime)
    db.session.commit()
    return jsonify({"message": "Showtime deleted successfully"})

# -------------------------------
# Lấy ghế trống theo suất chiếu
# -------------------------------
def get_available_seats(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    seats = Seat.query.filter_by(room_id=showtime.room_id).all()
    booked_tickets = Ticket.query.filter_by(showtime_id=showtime.id).all()
    booked_seat_ids = {ticket.seat_id for ticket in booked_tickets}

    available_seats = []
    for seat in seats:
        available_seats.append({
            "id": seat.id,
            "seat_number": seat.seat_number,
            "seat_type": seat.seat_type,
            "is_available": seat.id not in booked_seat_ids
        })

    return jsonify(available_seats)
