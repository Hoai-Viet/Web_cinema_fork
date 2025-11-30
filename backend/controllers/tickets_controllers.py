from flask import jsonify
from models import db, Ticket, User, Seat, Showtime, Payment, TicketType, SnackCombo
from sqlalchemy.orm import joinedload


# ============================================================================
# GET ALL TICKETS
# ============================================================================
def get_all_tickets():
    tickets = Ticket.query.options(
        joinedload(Ticket.showtime),
        joinedload(Ticket.seat),
        joinedload(Ticket.ticket_type)
    ).all()

    return jsonify([{
        "id": t.id,
        "user_id": t.user_id,
        "showtime_id": t.showtime_id,
        "seat_id": t.seat_id,
        "ticket_type_id": t.ticket_type_id,
        "price": t.price,
        "booked_at": t.booked_at.isoformat()
    } for t in tickets]), 200


# ============================================================================
# GET TICKET BY ID
# ============================================================================
def get_ticket_by_id(ticket_id):
    ticket = Ticket.query.options(
        joinedload(Ticket.showtime),
        joinedload(Ticket.seat),
        joinedload(Ticket.ticket_type)
    ).get(ticket_id)

    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    return jsonify({
        "id": ticket.id,
        "user_id": ticket.user_id,
        "showtime_id": ticket.showtime_id,
        "seat_id": ticket.seat_id,
        "ticket_type_id": ticket.ticket_type_id,
        "price": ticket.price,
        "booked_at": ticket.booked_at.isoformat()
    }), 200


# ============================================================================
# GET TICKETS BY USER
# ============================================================================
def get_tickets_by_user(user_id):
    tickets = Ticket.query.filter_by(user_id=user_id).options(
        joinedload(Ticket.showtime).joinedload(Showtime.movie),
        joinedload(Ticket.seat).joinedload(Seat.room)
    ).all()

    if not tickets:
        return jsonify({"message": "No tickets found"}), 404

    result = []
    for t in tickets:
        result.append({
            "ticket_id": t.id,
            "movie": t.showtime.movie.title,
            "room": t.seat.room.name,
            "seat_number": t.seat.seat_number,
            "start_time": t.showtime.start_time.isoformat(),
            "price": t.price,
            "booked_at": t.booked_at.isoformat()
        })

    return jsonify(result), 200


# ============================================================================
# CREATE TICKET — ĐẶT VÉ MỚI
# ============================================================================
def create_ticket(data):
    payment_id = data.get("payment_id")
    user_id = data.get("user_id")
    showtime_id = data.get("showtime_id")
    tickets = data.get("tickets", [])  # list các ticket: seat_id, ticket_type_id, snack_id

    required_fields = ["payment_id", "user_id", "showtime_id"]

    missing = [f for f in required_fields if f not in data or data[f] is None]
    if missing:
        return jsonify({
            "message": "Missing required fields",
            "missing_fields": missing
        }), 400

    created_ids = []

    try:
        for t in tickets:
            required = ("seat_id", "ticket_type_id")
            if not all(k in t for k in required):
                return jsonify({"message": "Invalid ticket structure"}), 400

            seat = Seat.query.get(t["seat_id"])
            if not seat:
                return jsonify({"message": f"Seat {t['seat_id']} not found"}), 404

            exists = Ticket.query.filter_by(showtime_id=showtime_id, seat_id=t["seat_id"]).first()
            if exists:
                return jsonify({"message": f"Seat {seat.seat_number} already booked"}), 409

            ticket_type = TicketType.query.get(t["ticket_type_id"])

            snack = None
            if t.get("snack_id"):
                snack = SnackCombo.query.get(t["snack_id"])
                if not snack:
                    return jsonify({"message": "Snack combo not found"}), 404

            new_ticket = Ticket(
                user_id=user_id,
                showtime_id=showtime_id,
                seat_id=t["seat_id"],
                ticket_type_id=t["ticket_type_id"],
                payment_id=payment_id,
                snack_id=snack.id if snack else None
            )

            db.session.add(new_ticket)
            db.session.flush()

            created_ids.append(new_ticket.id)

        db.session.commit()

        return jsonify({
            "message": "Tickets created successfully",
            "ticket_ids": created_ids
        }), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

# ============================================================================
# UPDATE TICKET — chỉ khi chưa thanh toán
# ============================================================================
def update_ticket(ticket_id, data):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    # Không sửa vé đã thanh toán
    if ticket.payment and ticket.payment.status == "Completed":
        return jsonify({"message": "Cannot update a paid ticket"}), 400

    if "seat_id" in data:
        seat = Seat.query.get(data["seat_id"])
        if not seat:
            return jsonify({"message": "Seat not found"}), 404

        exists = Ticket.query.filter_by(showtime_id=ticket.showtime_id, seat_id=seat.id).first()
        if exists and exists.id != ticket.id:
            return jsonify({"message": "Seat already booked"}), 409

        ticket.seat_id = seat.id

    if "ticket_type_id" in data:
        tt = TicketType.query.get(data["ticket_type_id"])
        if not tt:
            return jsonify({"message": "Ticket type not found"}), 404
        ticket.ticket_type_id = tt.id
        ticket.price = tt.base_price  # cập nhật giá

    db.session.commit()
    return jsonify({"message": "Ticket updated successfully"}), 200


# ============================================================================
# DELETE TICKET — chỉ khi chưa thanh toán
# ============================================================================
def delete_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    if ticket.payment and ticket.payment.status == "Completed":
        return jsonify({"message": "Cannot cancel a paid ticket"}), 400

    db.session.delete(ticket)
    db.session.commit()
    return jsonify({"message": "Ticket cancelled"}), 200


# ============================================================================
# GET AVAILABLE SEATS (BY SHOWTIME)
# ============================================================================
def get_available_seats(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    booked = db.session.query(Ticket.seat_id).filter_by(showtime_id=showtime_id)

    seats = Seat.query.filter(
        Seat.room_id == showtime.room_id,
        ~Seat.id.in_(booked)
    ).all()

    return jsonify([{
        "id": s.id,
        "seat_number": s.seat_number,
        "seat_type": s.seat_type
    } for s in seats]), 200


# ============================================================================
# GET TICKET DETAILS
# ============================================================================
def get_ticket_details(ticket_id):
    ticket = Ticket.query.options(
        joinedload(Ticket.showtime).joinedload(Showtime.movie),
        joinedload(Ticket.seat).joinedload(Seat.room)
    ).get(ticket_id)

    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    payment = ticket.payment

    return jsonify({
        "ticket_id": ticket.id,
        "movie": ticket.showtime.movie.title,
        "room": ticket.seat.room.name,
        "seat_number": ticket.seat.seat_number,
        "showtime": ticket.showtime.start_time.isoformat(),
        "price": ticket.price,
        "booked_at": ticket.booked_at.isoformat(),
        "payment": {
            "amount": payment.amount,
            "method": payment.payment_method,
            "status": payment.status,
            "created_at": payment.created_at.isoformat()
        } if payment else None
    }), 200


# ============================================================================
# GET TICKET TYPES FOR SHOWTIME
# ============================================================================
def get_ticket_types_by_showtime(showtime_id):
    showtime = Showtime.query.get(showtime_id)
    if not showtime:
        return jsonify({"message": "Showtime not found"}), 404

    ticket_types = TicketType.query.all()

    return jsonify([{
        "id": t.id,
        "name": t.name,
        "description": t.description,
        "base_price": t.base_price
    } for t in ticket_types]), 200
