from flask import jsonify, request
from models import db, Seat, Ticket, Cinema, Room

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

def get_seats_by_room(room_id):
    seats = Seat.query.filter_by(room_id=room_id).all()
    result = [{
        "id": s.id,
        "seat_number": s.seat_number,
        "seat_type": s.seat_type
    } for s in seats]

    return jsonify(result)

def get_seats_status(showtime_id):
    booked_seats = db.session.query(Seat.id).join(Ticket).filter(
        Ticket.showtime_id == showtime_id
    ).all()
    booked_ids = [s.id for s in booked_seats]

    seats = Seat.query.all()
    result = [{
        "id": s.id,
        "seat_number": s.seat_number,
        "seat_type": s.seat_type,
        "is_booked": s.id in booked_ids
    } for s in seats]

    return jsonify(result)


def book_multiple_seats():
    data = request.get_json()

    seat_ids = data.get("seat_ids")
    showtime_id = data.get("showtime_id")
    user_id = data.get("user_id")  # nếu có thông tin user

    if not seat_ids or not showtime_id:
        return jsonify({"message": "Missing seat_ids or showtime_id"}), 400

    # Kiểm tra xem có ghế nào đã bị đặt chưa
    existing_tickets = Ticket.query.filter(
        Ticket.showtime_id == showtime_id,
        Ticket.seat_id.in_(seat_ids)
    ).all()

    if existing_tickets:
        booked_list = [t.seat_id for t in existing_tickets]
        return jsonify({
            "message": "Some seats are already booked",
            "booked_seats": booked_list
        }), 409

    # Tạo vé mới cho từng ghế
    for sid in seat_ids:
        ticket = Ticket(
            seat_id=sid,
            showtime_id=showtime_id,
            user_id=user_id,  # nếu bạn có cột user_id
            booking_time=db.func.now()
        )
        db.session.add(ticket)

    db.session.commit()
    return jsonify({
        "message": "Seats booked successfully",
        "booked_seat_ids": seat_ids
    }), 201
    
def get_seats_by_cinema(cinema_id):
    """
    Lấy danh sách tất cả ghế thuộc về 1 rạp chiếu cụ thể (Cinema)
    """
    # Kiểm tra xem rạp có tồn tại không
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return jsonify({"message": "Cinema not found"}), 404

    # Lấy tất cả các phòng của rạp
    rooms = Room.query.filter_by(cinema_id=cinema.id).all()
    if not rooms:
        return jsonify({"message": "No rooms found for this cinema"}), 404

    # Lấy toàn bộ ghế trong các phòng đó
    room_ids = [r.id for r in rooms]
    seats = Seat.query.filter(Seat.room_id.in_(room_ids)).all()

    # Gộp kết quả thành danh sách có cấu trúc rõ ràng
    result = []
    for seat in seats:
        result.append({
            "id": seat.id,
            "seat_number": seat.seat_number,
            "seat_type": seat.seat_type,
            "room_id": seat.room_id
        })

    return jsonify({
        "cinema_id": cinema.id,
        "cinema_name": cinema.name,
        "total_rooms": len(rooms),
        "total_seats": len(result),
        "seats": result
    }), 200