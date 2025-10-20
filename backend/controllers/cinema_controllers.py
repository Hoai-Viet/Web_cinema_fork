from models import db, Cinema, Room

def get_all_cinemas():
    cinemas = Cinema.query.all()
    return [{"id": c.id, "name": c.name, "address": c.address, "phone": c.phone} for c in cinemas]


def get_cinema_by_id(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return None
    return {"id": cinema.id, "name": cinema.name, "address": cinema.address, "phone": cinema.phone}


def create_new_cinema(data):
    if not data.get("name") or not data.get("address"):
        return {"error": "Missing required fields"}, 400

    new_cinema = Cinema(
        name=data["name"],
        address=data["address"],
        phone=data.get("phone")
    )
    db.session.add(new_cinema)
    db.session.commit()
    return {"id": new_cinema.id, "message": "Cinema created successfully"}, 201


def update_cinema(cinema_id, data):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return {"error": "Cinema not found"}, 404

    if "name" in data:
        cinema.name = data["name"]
    if "address" in data:
        cinema.address = data["address"]
    if "phone" in data:
        cinema.phone = data["phone"]

    db.session.commit()
    return {"message": "Cinema updated successfully"}, 200


def delete_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return {"error": "Cinema not found"}, 404

    db.session.delete(cinema)
    db.session.commit()
    return {"message": "Cinema deleted successfully"}, 200


def get_rooms_by_cinema(cinema_id):
    cinema = Cinema.query.get(cinema_id)
    if not cinema:
        return None

    rooms = Room.query.filter_by(cinema_id=cinema_id).all()
    room_list = [{"id": r.id, "name": r.name, "total_seats": r.total_seats} for r in rooms]

    return {
        "cinema_id": cinema.id,
        "cinema_name": cinema.name,
        "rooms": room_list
    }
