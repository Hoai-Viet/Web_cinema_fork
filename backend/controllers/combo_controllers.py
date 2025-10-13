from flask import jsonify, request
from models import db, Combo, TicketCombo
from datetime import datetime
import uuid

# Lấy toàn bộ combo
def get_all_combos():
    combos = Combo.query.all()
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


# Lấy chi tiết 1 combo
def get_combo_by_id(combo_id):
    combo = Combo.query.get(combo_id)
    if not combo:
        return jsonify({"message": "Combo not found"}), 404

    return jsonify({
        "id": combo.id,
        "name": combo.name,
        "description": combo.description,
        "price": combo.price,
        "image_url": combo.image_url
    }), 200


# User mua combo (gắn combo với vé)
def add_combo_to_ticket():
    data = request.get_json()
    ticket_id = data.get("ticket_id")
    combo_id = data.get("combo_id")
    quantity = data.get("quantity", 1)

    if not all([ticket_id, combo_id]):
        return jsonify({"message": "Missing ticket_id or combo_id"}), 400

    ticket_combo = TicketCombo(
        ticket_id=ticket_id,
        combo_id=combo_id,
        quantity=quantity
    )
    db.session.add(ticket_combo)
    db.session.commit()

    return jsonify({"message": "Combo added to ticket successfully"}), 201
