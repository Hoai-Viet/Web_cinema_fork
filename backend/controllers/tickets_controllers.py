from flask import jsonify
from models import db, Ticket, User, Seat, Showtime


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


def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket cancelled successfully"})
