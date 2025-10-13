from flask import jsonify
from models import db, Ticket, User, Seat, Showtime, Payment

# ✅ Lấy tất cả vé
def get_all_tickets():
    tickets = Ticket.query.all()
    result = []
    for t in tickets:
        result.append({
            "id": t.id,
            "user_id": t.user_id,
            "showtime_id": t.showtime_id,
            "seat_id": t.seat_id,
            "price": t.price,
            "booked_at": t.booked_at.isoformat() if t.booked_at else None
        })
    return jsonify(result)


# ✅ Lấy vé theo ID
def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    return jsonify({
        "id": ticket.id,
        "user_id": ticket.user_id,
        "showtime_id": ticket.showtime_id,
        "seat_id": ticket.seat_id,
        "price": ticket.price,
        "booked_at": ticket.booked_at.isoformat() if ticket.booked_at else None
    })


# ✅ Lấy danh sách vé của 1 user
def get_tickets_by_user(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).all()
    if not tickets:
        return jsonify({"message": "No tickets found for this user"}), 404

    result = []
    for t in tickets:
        movie = t.showtime.movie if t.showtime else None
        seat = t.seat
        result.append({
            "id": t.id,
            "movie": movie.title if movie else None,
            "seat_number": seat.seat_number if seat else None,
            "room": seat.room.name if seat and seat.room else None,
            "start_time": t.showtime.start_time.isoformat() if t.showtime else None,
            "price": t.price,
            "booked_at": t.booked_at.isoformat() if t.booked_at else None
        })
    return jsonify(result)


# ✅ Đặt vé mới
def create_ticket(data):
    required_fields = ("user_id", "showtime_id", "seat_id", "price")
    if not data or not all(k in data for k in required_fields):
        return jsonify({"message": "Missing required fields"}), 400

    if not User.query.get(data["user_id"]):
        return jsonify({"message": "User not found"}), 404
    if not Showtime.query.get(data["showtime_id"]):
        return jsonify({"message": "Showtime not found"}), 404
    if not Seat.query.get(data["seat_id"]):
        return jsonify({"message": "Seat not found"}), 404

    existing_ticket = Ticket.query.filter_by(
        showtime_id=data["showtime_id"], seat_id=data["seat_id"]
    ).first()
    if existing_ticket:
        return jsonify({"message": "Seat already booked for this showtime"}), 400

    new_ticket = Ticket(
        user_id=data["user_id"],
        showtime_id=data["showtime_id"],
        seat_id=data["seat_id"],
        price=data["price"]
    )
    db.session.add(new_ticket)
    db.session.commit()

    return jsonify({"message": "Ticket booked successfully", "ticket_id": new_ticket.id}), 201


# ✅ Cập nhật vé (chỉ khi chưa thanh toán)
def update_ticket(ticket_id, data):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    if "seat_id" in data:
        existing_ticket = Ticket.query.filter_by(
            showtime_id=ticket.showtime_id, seat_id=data["seat_id"]
        ).first()
        if existing_ticket and existing_ticket.id != ticket.id:
            return jsonify({"message": "Seat already booked"}), 400
        ticket.seat_id = data["seat_id"]

    if "showtime_id" in data:
        if not Showtime.query.get(data["showtime_id"]):
            return jsonify({"message": "Showtime not found"}), 404
        ticket.showtime_id = data["showtime_id"]

    if "price" in data:
        ticket.price = data["price"]

    db.session.commit()
    return jsonify({"message": "Ticket updated successfully"})


# ✅ Huỷ vé
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket cancelled successfully"})


# ✅ Lấy ghế trống của suất chiếu
def get_available_seats(showtime_id):
    booked_seats = db.session.query(Ticket.seat_id).filter_by(showtime_id=showtime_id)
    available_seats = Seat.query.filter(~Seat.id.in_(booked_seats)).all()

    result = [
        {
            "id": s.id,
            "seat_number": s.seat_number,
            "seat_type": s.seat_type,
            "room_type": s.room.room_type if s.room else None
        }
        for s in available_seats
    ]
    return jsonify(result)


# ✅ Lấy chi tiết vé
def get_ticket_details(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    showtime = ticket.showtime
    movie = showtime.movie if showtime else None
    seat = ticket.seat

    combos = [
        {
            "id": c.id,
            "name": c.name,
            "price": c.price
        } for c in ticket.snacks
    ]

    payments = Payment.query.filter_by(ticket_id=ticket.id).all()
    payment_info = [
        {
            "amount": p.amount,
            "method": p.payment_method,
            "status": p.status,
            "created_at": p.created_at.isoformat()
        }
        for p in payments
    ]

    return jsonify({
        "ticket_id": ticket.id,
        "movie": movie.title if movie else None,
        "room": seat.room.name if seat and seat.room else None,
        "seat_number": seat.seat_number if seat else None,
        "showtime": showtime.start_time.isoformat() if showtime else None,
        "price": ticket.price,
        "booked_at": ticket.booked_at.isoformat() if ticket.booked_at else None,
        "combos": combos,
        "payment_info": payment_info
    })
