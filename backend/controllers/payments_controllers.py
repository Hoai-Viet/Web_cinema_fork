from flask import jsonify, request
from models import db, Payment, Ticket
from datetime import datetime


#  User tạo payment (thanh toán vé)
def create_payment():
    data = request.get_json()
    ticket_id = data.get("ticket_id")
    amount = data.get("amount")
    payment_method = data.get("payment_method", "Cash")

    if not ticket_id or not amount:
        return jsonify({"error": "Missing ticket_id or amount"}), 400

    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"error": "Ticket not found"}), 404

    payment = Payment(
        ticket_id=ticket_id,
        amount=amount,
        payment_method=payment_method,
        status="Pending",
        created_at=datetime.utcnow()
    )
    db.session.add(payment)
    db.session.commit()

    return jsonify({
        "message": "Payment created successfully",
        "payment_id": payment.id,
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
