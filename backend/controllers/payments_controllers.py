from flask import jsonify, request
from models import db, Payment, Ticket,ticket_snack, SnackCombo
from datetime import datetime


#  User tạo payment (thanh toán vé)
def create_payment():
    data = request.get_json()
    ticket_id = data.get("ticket_id")
    snacks = data.get("snacks", [])   # list combo + quantity
    payment_method = data.get("payment_method", "Cash")

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    total_amount = ticket.price  # start with ticket price

    # Xử lý combo
    for item in snacks:
        combo_id = item["combo_id"]
        qty = item.get("quantity", 1)

        combo = SnackCombo.query.get(combo_id)
        if not combo:
            return jsonify({"error": f"Snack combo {combo_id} not found"}), 404

        # Gắn combo vào ticket
        stmt = ticket_snack.insert().values(
            ticket_id=ticket_id,
            snack_combo_id=combo_id,
            quantity=qty
        )
        db.session.execute(stmt)

        total_amount += combo.price * qty

    # Tạo payment
    payment = Payment(
        ticket_id=ticket_id,
        amount=total_amount,
        payment_method=payment_method,
        status="Pending",
        created_at=datetime.utcnow()
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "message": "Payment created successfully",
        "payment_id": payment.id,
        "amount": total_amount,
        "status": payment.status
    }), 201


#  Xem thông tin thanh toán của user (theo ticket_id)
def get_payment_by_ticket(ticket_id):
    payment = Payment.query.filter_by(ticket_id=ticket_id).first()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify({
        "payment_id": payment.id,
        "ticket_id": payment.ticket_id,
        "amount": payment.amount,
        "payment_method": payment.payment_method,
        "status": payment.status,
        "created_at": payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
    }), 200


#  Cập nhật trạng thái thanh toán (ví dụ: sau khi user trả tiền xong)
def update_payment_status(payment_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["Pending", "Completed", "Failed"]:
        return jsonify({"error": "Invalid status"}), 400

    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    payment.status = new_status
    db.session.commit()

    return jsonify({"message": f"Payment updated to {new_status}"}), 200


# ------------------------------------------------------
# Preview Payment
# ------------------------------------------------------
def preview_payment():
    data = request.get_json()
    ticket_id = data.get("ticket_id")
    snacks = data.get("snacks", [])

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    total_ticket_price = ticket.price
    total_snack_price = 0
    snack_details = []

    for item in snacks:
        combo_id = item["combo_id"]
        qty = item.get("quantity", 1)

        combo = SnackCombo.query.get(combo_id)
        if not combo:
            return jsonify({"error": f"Snack combo {combo_id} not found"}), 404

        total_snack_price += combo.price * qty

        snack_details.append({
            "combo_id": combo.id,
            "name": combo.name,
            "quantity": qty,
            "unit_price": combo.price,
            "total_price": combo.price * qty
        })

    final_amount = total_ticket_price + total_snack_price

    return jsonify({
        "ticket_price": total_ticket_price,
        "snacks": snack_details,
        "snack_total": total_snack_price,
        "final_amount": final_amount
    }), 200


# ------------------------------------------------------
# Get all payments of a user
# ------------------------------------------------------
def get_payments_by_user(user_id):
    payments = (
        db.session.query(Payment)
        .join(Ticket)
        .filter(Ticket.user_id == user_id)
        .all()
    )

    if not payments:
        return jsonify({"message": "No payments found"}), 200

    result = []
    for p in payments:
        result.append({
            "payment_id": p.id,
            "ticket_id": p.ticket_id,
            "amount": p.amount,
            "payment_method": p.payment_method,
            "status": p.status,
            "created_at": p.created_at.strftime("%Y-%m-%d %H:%M:%S")
        })

    return jsonify(result), 200


# ------------------------------------------------------
# Get payment detail
# ------------------------------------------------------
def get_payment_detail(ticket_id):
    payment = Payment.query.filter_by(ticket_id=ticket_id).first()
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    ticket = Ticket.query.get(ticket_id)

    combo_rows = db.session.execute(
        ticket_snack.select().where(ticket_snack.c.ticket_id == ticket_id)
    )

    snacks = []
    for row in combo_rows:
        combo = SnackCombo.query.get(row.snack_combo_id)
        snacks.append({
            "combo_id": combo.id,
            "name": combo.name,
            "quantity": row.quantity,
            "unit_price": combo.price,
            "total_price": combo.price * row.quantity
        })

    showtime = ticket.showtime
    movie = showtime.movie

    return jsonify({
        "payment": {
            "payment_id": payment.id,
            "amount": payment.amount,
            "payment_method": payment.payment_method,
            "status": payment.status,
            "created_at": payment.created_at.strftime("%Y-%m-%d %H:%M:%S")
        },
        "ticket": {
            "seat": ticket.seat.seat_number,
            "room": showtime.room.name,
            "showtime": showtime.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            "movie": movie.title
        },
        "snacks": snacks
    }), 200


# ------------------------------------------------------
# Cancel payment
# ------------------------------------------------------
def cancel_payment(payment_id):
    payment = Payment.query.get(payment_id)
    if not payment:
        return jsonify({"error": "Payment not found"}), 404

    if payment.status == "Completed":
        return jsonify({"error": "Cannot cancel a completed payment"}), 400

    payment.status = "Failed"

    db.session.execute(
        ticket_snack.delete().where(ticket_snack.c.ticket_id == payment.ticket_id)
    )

    db.session.commit()

    return jsonify({"message": "Payment cancelled successfully"}), 200