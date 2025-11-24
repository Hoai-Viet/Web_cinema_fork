from flask import jsonify, request
from models import db, Payment, Ticket, SnackCombo, ticket_snack, User, Showtime,TicketType
from datetime import datetime
from sqlalchemy.orm import joinedload


# ============================================================================ 
# PREVIEW PAYMENT (before checkout) - mỗi ticket chỉ 1 combo
# ============================================================================
from flask import jsonify, request
from models import db, Payment, Ticket, SnackCombo, ticket_snack
from datetime import datetime

# ====================================================================
# PREVIEW PAYMENT
# ====================================================================
def preview_payment():
    data = request.get_json()
    user_id = data.get("user_id")
    showtime_id = data.get("showtime_id")
    seat_ids = data.get("seat_ids", [])
    ticket_type_id = data.get("ticket_type_id")
    snack = data.get("snack_combo")  # chỉ 1 combo

    if not user_id or not showtime_id or not seat_ids or not ticket_type_id:
        return jsonify({"error": "Missing required fields"}), 400

    showtime = Showtime.query.get(showtime_id)
    ticket_type = TicketType.query.get(ticket_type_id)

    if not showtime or not ticket_type:
        return jsonify({"error": "Invalid showtime or ticket type"}), 404

    total_ticket_price = ticket_type.base_price * len(seat_ids)
    total_snack_price = 0
    snack_detail = []

    if snack:
        combo = SnackCombo.query.get(snack.get("combo_id"))
        qty = snack.get("quantity", 1)

        if not combo:
            return jsonify({"error": "Snack combo not found"}), 404

        total_snack_price = combo.price * qty
        snack_detail.append({
            "combo_id": combo.id,
            "name": combo.name,
            "unit_price": combo.price,
            "quantity": qty,
            "total_price": total_snack_price
        })

    return jsonify({
        "user_id": user_id,
        "showtime_id": showtime.id,
        "seats": seat_ids,
        "ticket_type": {"id": ticket_type.id, "name": ticket_type.name, "price": ticket_type.base_price},
        "tickets_total": total_ticket_price,
        "snack": snack_detail,
        "snack_total": total_snack_price,
        "final_amount": total_ticket_price + total_snack_price
    }), 200



# ====================================================================
# CREATE PAYMENT
# ====================================================================
from flask import jsonify, request
from datetime import datetime
from models import db, Ticket, User, Showtime, TicketType, SnackCombo, Payment, ticket_snack

def create_payment():
    data = request.get_json()

    user_id = data.get("user_id")
    showtime_id = data.get("showtime_id")
    seat_ids = data.get("seat_ids", [])
    ticket_type_id = data.get("ticket_type_id")
    snack = data.get("snack_combo")  # chỉ 1 combo
    payment_method = data.get("payment_method", "Cash")

    if not user_id or not showtime_id or not seat_ids or not ticket_type_id:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.get(user_id)
    showtime = Showtime.query.get(showtime_id)
    ticket_type = TicketType.query.get(ticket_type_id)

    if not user or not showtime or not ticket_type:
        return jsonify({"error": "Invalid user, showtime or ticket type"}), 404

    # Kiểm tra ghế đã đặt chưa
    existing_seats = db.session.query(Ticket.seat_id).filter(
        Ticket.showtime_id == showtime_id,
        Ticket.seat_id.in_(seat_ids)
    ).all()
    if existing_seats:
        existing_seat_list = [s[0] for s in existing_seats]
        return jsonify({"error": f"Seats already booked: {existing_seat_list}"}), 409

    total_ticket_price = ticket_type.base_price * len(seat_ids)
    total_snack_price = 0

    # Tạo payment trước để gắn ticket
    payment = Payment(
        amount=0,
        payment_method=payment_method,
        status="Pending",
        user_id=user.id,
        created_at=datetime.utcnow()
    )
    db.session.add(payment)
    db.session.flush()  # flush để lấy payment.id

    # Tạo ticket cho từng ghế
    tickets = []
    for seat_id in seat_ids:
        ticket = Ticket(
            user_id=user.id,
            showtime_id=showtime.id,
            seat_id=seat_id,
            ticket_type_id=ticket_type.id,
            price=ticket_type.base_price,
            payment_id=payment.id,
            quantity=1
        )
        db.session.add(ticket)
        tickets.append(ticket)
    db.session.flush()  # flush để có ticket.id

    # Gắn snack combo (tối đa 1) vào ticket đầu tiên
    if snack:
        combo = SnackCombo.query.get(snack.get("combo_id"))
        qty = snack.get("quantity", 1)
        if not combo:
            return jsonify({"error": "Snack combo not found"}), 404

        db.session.execute(
            ticket_snack.insert().values(
                ticket_id=tickets[0].id,
                snack_combo_id=combo.id,
                quantity=qty
            )
        )
        total_snack_price = combo.price * qty

    # Tính tổng tiền
    payment.amount = total_ticket_price + total_snack_price
    db.session.commit()

    return jsonify({
        "message": "Payment and tickets created successfully",
        "payment_id": payment.id,
        "user_id": payment.user_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "status": payment.status,
        "ticket_ids": [t.id for t in tickets]
    }), 201


# ============================================================================ 
# GET PAYMENT DETAIL
# ============================================================================
def get_payment_detail(payment_id):
    # Load payment kèm tickets, showtime, movie, seat và snack combos
    payment = Payment.query.options(
        joinedload(Payment.tickets)
        .joinedload(Ticket.showtime)
        .joinedload(Showtime.movie),
        joinedload(Payment.tickets)
        .joinedload(Ticket.seat),
        joinedload(Payment.tickets)
        .joinedload(Ticket.snacks).joinedload(ticket_snack.c.snack_combo)
    ).get(payment_id)

    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    user = User.query.get(payment.user_id)

    tickets_list = []
    for t in payment.tickets:
        # Lấy combo cho từng ticket
        snacks_list = []
        for ts in t.snacks:
            combo = SnackCombo.query.get(ts.snack_combo_id)
            snacks_list.append({
                "combo_id": combo.id,
                "name": combo.name,
                "price": combo.price,
                "quantity": ts.quantity
            })

        tickets_list.append({
            "ticket_id": t.id,
            "seat": t.seat.seat_number,
            "room": t.showtime.room.name,
            "movie": t.showtime.movie.title,
            "showtime": t.showtime.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "price": t.price,
            "snacks": snacks_list
        })

    return jsonify({
        "payment": {
            "payment_id": payment.id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "created_at": payment.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            "user": {
                "user_id": user.id,
                "username": user.username,
                "email": user.email
            }
        },
        "tickets": tickets_list
    }), 200
