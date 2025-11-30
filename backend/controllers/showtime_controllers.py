from flask import jsonify, request
from models import db, Showtime, Movie, Room, Ticket, Seat, Cinema
from sqlalchemy.orm import joinedload

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

def get_showtimes_by_movie(movie_id):
    showtimes = Showtime.query.filter_by(movie_id=movie_id).all()
    result = []

    for s in showtimes:
        result.append({
            "id": s.id,
            "movie_id": s.movie_id,
            "room": s.room.name if s.room else None,
            "start_time": s.start_time.strftime("%Y-%m-%d %H:%M") if s.start_time else None,
            "end_time": s.end_time.strftime("%Y-%m-%d %H:%M") if s.end_time else None,
        })

    return jsonify(result), 200

# -------------------------------
# Lấy thông tin rạp theo showtime_id (thông qua room)
# -------------------------------
def get_cinema_by_showtime(showtime_id):

    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    room = Room.query.get(showtime.room_id)
    if not room:
        return jsonify({"message": "Room not found"}), 404

    cinema = Cinema.query.get(room.cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    return jsonify({
        "id": cinema.id,
        "name": cinema.name,
        "address": cinema.address,
        "phone": cinema.phone
    }), 200

