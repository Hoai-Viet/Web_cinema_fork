from flask import jsonify, request
from models import db, SnackCombo, Ticket, ticket_snack
from sqlalchemy.exc import SQLAlchemyError


# [GET] Lấy tất cả combo
def get_all_combos():
    try:
        combos = SnackCombo.query.all()
        result = [
            {
                "id": c.id,
                "name": c.name,
                "description": c.description,
                "price": c.price,
                "image_url": c.image_url
            }
            for c in combos
        ]
        return jsonify(result), 200
    except Exception as e:
        return jsonify({"message": "Error fetching combos", "error": str(e)}), 500


# [GET] Lấy chi tiết 1 combo theo ID
def get_combo_by_id(combo_id):
    combo = SnackCombo.query.get(combo_id)
    if not combo:
        return jsonify({"message": "Combo not found"}), 404

    return jsonify({
        "id": combo.id,
        "name": combo.name,
        "description": combo.description,
        "price": combo.price,
        "image_url": combo.image_url
    }), 200


# [POST] Thêm combo vào vé (user mua combo khi đặt vé)
def add_combo_to_ticket():
    data = request.get_json()
    ticket_id = data.get("ticket_id")
    combo_id = data.get("combo_id")
    quantity = data.get("quantity", 1)

    if not ticket_id or not combo_id:
        return jsonify({"message": "Missing ticket_id or combo_id"}), 400

    if quantity < 1:
        return jsonify({"message": "Quantity must be at least 1"}), 400

    try:
        # Kiểm tra vé tồn tại
        ticket = Ticket.query.get(ticket_id)
        if not ticket:
            return jsonify({"message": "Ticket not found"}), 404

        # Kiểm tra combo tồn tại
        combo = SnackCombo.query.get(combo_id)
        if not combo:
            return jsonify({"message": "Combo not found"}), 404

        # Kiểm tra xem đã thêm combo này vào vé chưa
        existing = db.session.query(ticket_snack).filter_by(
            ticket_id=ticket_id,
            snack_combo_id=combo_id
        ).first()

        if existing:
            # Nếu đã có → cập nhật số lượng
            stmt = (
                ticket_snack.update()
                .where(
                    ticket_snack.c.ticket_id == ticket_id,
                    ticket_snack.c.snack_combo_id == combo_id
                )
                .values(quantity=existing.quantity + quantity)
            )
            db.session.execute(stmt)
            message = "Combo quantity updated successfully"
        else:
            # Nếu chưa có → thêm mới
            stmt = ticket_snack.insert().values(
                ticket_id=ticket_id,
                snack_combo_id=combo_id,
                quantity=quantity
            )
            db.session.execute(stmt)
            message = "Combo added to ticket successfully"

        db.session.commit()
        return jsonify({"message": message}), 201

    except SQLAlchemyError as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Server error", "error": str(e)}), 500


# [GET] Lấy danh sách combo đã chọn trong 1 vé
def get_combos_in_ticket(ticket_id):
    ticket = Ticket.query.get(ticket_id)
    if not ticket:
        return jsonify({"message": "Ticket not found"}), 404

    combos = db.session.query(
        SnackCombo, ticket_snack.c.quantity
    ).join(
        ticket_snack, SnackCombo.id == ticket_snack.c.snack_combo_id
    ).filter(
        ticket_snack.c.ticket_id == ticket_id
    ).all()

    result = [
        {
            "id": combo.id,
            "name": combo.name,
            "description": combo.description,
            "price": combo.price,
            "image_url": combo.image_url,
            "quantity": quantity
        }
        for combo, quantity in combos
    ]

    return jsonify(result), 200


# [DELETE] Xóa 1 combo khỏi vé
def remove_combo_from_ticket(ticket_id, combo_id):
    try:
        deleted = db.session.execute(
            ticket_snack.delete().where(
                ticket_snack.c.ticket_id == ticket_id,
                ticket_snack.c.snack_combo_id == combo_id
            )
        )
        db.session.commit()

        if deleted.rowcount == 0:
            return jsonify({"message": "Combo not found in this ticket"}), 404

        return jsonify({"message": "Combo removed from ticket"}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Error removing combo", "error": str(e)}), 500