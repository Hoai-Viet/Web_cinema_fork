from flask import jsonify, request
from models import db, TicketType, Showtime
import uuid
from sqlalchemy.orm import joinedload

#   Lấy tất cả loại vé
def get_all_ticket_types():
    ticket_types = TicketType.query.all()
    result = [
        {
            "id": t.id,
            "name": t.name,
            "description": t.description,
            "base_price": t.base_price,
            "room_type": t.room_type
        }
        for t in ticket_types
    ]
    return jsonify(result), 200


#   Lấy loại vé theo ID
def get_ticket_type(ticket_type_id):
    ticket_type = TicketType.query.get(ticket_type_id)
    if not ticket_type:
        return jsonify({"message": "Ticket type not found"}), 404

    return jsonify({
        "id": ticket_type.id,
        "name": ticket_type.name,
        "description": ticket_type.description,
        "base_price": ticket_type.base_price,
        "room_type": ticket_type.room_type
    }), 200


#    Tạo loại vé mới
def create_ticket_type():
    data = request.get_json()
    new_ticket_type = TicketType(
        id=str(uuid.uuid4()),
        name=data.get("name"),
        description=data.get("description"),
        base_price=data.get("base_price"),
        room_type=data.get("room_type")
    )
    db.session.add(new_ticket_type)
    db.session.commit()
    return jsonify({"message": "Ticket type created successfully"}), 201


#    Cập nhật loại vé
def update_ticket_type(ticket_type_id):
    data = request.get_json()
    ticket_type = TicketType.query.get(ticket_type_id)
    if not ticket_type:
        return jsonify({"message": "Ticket type not found"}), 404

    ticket_type.name = data.get("name", ticket_type.name)
    ticket_type.description = data.get("description", ticket_type.description)
    ticket_type.base_price = data.get("base_price", ticket_type.base_price)
    ticket_type.room_type = data.get("room_type", ticket_type.room_type)

    db.session.commit()
    return jsonify({"message": "Ticket type updated successfully"}), 200


#    Xóa loại vé
def delete_ticket_type(ticket_type_id):
    ticket_type = TicketType.query.get(ticket_type_id)
    if not ticket_type:
        return jsonify({"message": "Ticket type not found"}), 404

    db.session.delete(ticket_type)
    db.session.commit()
    return jsonify({"message": "Ticket type deleted successfully"}), 200
