from models import db, Cinema, Room

def get_all_cinemas():
    cinemas = Cinema.query.all()
    return [{"id": c.id, "name": c.name, "address": c.address, "phone": c.phone} for c in cinemas]

def create_new_cinema(data):
    new_cinema = Cinema(name=data["name"], address=data["address"], phone=data.get("phone"))
    db.session.add(new_cinema)
    db.session.commit()
    return new_cinema.id