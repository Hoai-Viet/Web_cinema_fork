from flask import jsonify, request
from models import db, Payment, Ticket, SnackCombo, ticket_snack, User, Showtime,TicketType
from datetime import datetime
from sqlalchemy.orm import joinedload
from models import User


def preview_payment():
    data = request.get_json()

    user_id = data.get("user_id")
    amount = data.get("amount")
    payment_method = data.get("payment_method", "Cash")

    # ==============================
    # VALIDATION
    # ==============================
    if not user_id:
        return jsonify({"error": "Missing user_id"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # ==============================
    # RESPONSE (KHÔNG LƯU DB)
    # ==============================
    return jsonify({
        "message": "Payment preview generated successfully",
        "user_id": user.id,
        "username": user.username,
        "payment_method": payment_method,
        "estimated_amount": amount or 0,
        "status": "Preview",
        "created_at": datetime.utcnow().isoformat()
    }), 200




# ====================================================================
# CREATE PAYMENT
# ====================================================================


from flask import request, jsonify
from datetime import datetime
from models import db, Payment, User


def create_payment():
    data = request.get_json()
    user_id = data.get("user_id")
    amount = data.get("amount") 
    payment_method = data.get("payment_method", "Cash")

    if not user_id or amount is None:
        return jsonify({"error": "Missing required fields"}), 400

    user = User.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    payment = Payment(
        user_id=user.id,
        amount=amount,
        payment_method=payment_method,
        status="Pending",
        created_at=datetime.utcnow()
    )

    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "message": "Payment created successfully",
        "payment": {
            "id": payment.id,
            "user_id": payment.user_id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "created_at": payment.created_at.isoformat()
        }
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
