import json
from datetime import datetime, timezone
from app import create_app
from models import (
    db, City, Cinema, Room, Movie, Seat, Showtime, SnackCombo,
    User, TicketType, generate_uuid
)

app = create_app()
app.app_context().push()


def seed_from_json():
    print("\n🔹 Starting database seeding...\n")

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # ======================================================
    # Seed Cities
    # ======================================================
    if City.query.count() == 0:
        print("🗺️  Seeding Cities...")
        cities = [City(id=generate_uuid(), name=c["name"]) for c in data["cities"]]
        db.session.bulk_save_objects(cities)
        db.session.commit()

    # ======================================================
    # Seed Cinemas
    # ======================================================
    if Cinema.query.count() == 0:
        print("🏢  Seeding Cinemas...")
        cinemas = []
        for c in data["cinemas"]:
            city = City.query.filter_by(name=c["city"]).first()
            if not city:
                print(f"⚠️  City not found for cinema: {c['name']}")
                continue
            cinemas.append(Cinema(
                id=generate_uuid(),
                name=c["name"],
                address=c["address"],
                phone=c.get("phone"),
                city_id=city.id
            ))
        db.session.bulk_save_objects(cinemas)
        db.session.commit()

    # ======================================================
    # Seed Rooms
    # ======================================================
    if Room.query.count() == 0:
        print("🎬  Seeding Rooms...")
        rooms = []
        for r in data["rooms"]:
            cinema = Cinema.query.filter_by(name=r["cinema"]).first()
            if not cinema:
                print(f"⚠️  Cinema not found for room: {r['name']}")
                continue
            rooms.append(Room(
                id=generate_uuid(),
                name=r["name"],
                cinema_id=cinema.id,
                total_seats=r["total_seats"],
                room_type=r["room_type"]
            ))
        db.session.bulk_save_objects(rooms)
        db.session.commit()

    # ======================================================
    # Seed Movies
    # ======================================================
    if Movie.query.count() == 0:
        print("🎞️  Seeding Movies...")
        movies = []
        for m in data["movies"]:
            movies.append(Movie(
                id=generate_uuid(),
                title=m["title"],
                description=m.get("description"),
                genre=m.get("genre"),
                duration_minutes=m["duration_minutes"],
                movie_content=m.get("movie_content"),
                poster_url=m.get("poster_url"),
                country=m.get("country"),
                age_rating=m.get("age_rating"),
                language=m.get("language"),
                status=m.get("status", "Coming Soon")
            ))
        db.session.bulk_save_objects(movies)
        db.session.commit()

    if Seat.query.count() == 0:
        print("💺  Auto generating Seats...")
        seats = []
        rooms = Room.query.all()

        for room in rooms:
            for i in range(1, room.total_seats + 1):
                row_index = (i - 1) // 10
                seat_number = f"{chr(65 + row_index)}{(i - 1) % 10 + 1}"

                if i <= room.total_seats * 0.2:
                    seat_type = "VIP"
                elif i > room.total_seats * 0.8:
                    seat_type = "Sweetbox"
                else:
                    seat_type = "Standard"

                seats.append(Seat(
                    id=generate_uuid(),
                    room_id=room.id,
                    seat_number=seat_number,
                    seat_type=seat_type
                ))
        db.session.bulk_save_objects(seats)
        db.session.commit()

    # ======================================================
    # Seed Showtimes
    # ======================================================
    if Showtime.query.count() == 0:
        print("⏰  Seeding Showtimes...")
        showtimes = []

        for s in data["showtimes"]:
            movie = Movie.query.filter_by(title=s["movie"]).first()
            room = Room.query.filter_by(name=s["room"]).first()

            if not movie or not room:
                print("⚠️  Missing movie/room for showtime, skipping...")
                continue

            showtimes.append(Showtime(
                id=generate_uuid(),
                movie_id=movie.id,
                room_id=room.id,
                start_time=datetime.fromisoformat(s["start_time"]),
                end_time=datetime.fromisoformat(s["end_time"])
            ))
        db.session.bulk_save_objects(showtimes)
        db.session.commit()

    # ======================================================
    # Seed Snack Combos
    # ======================================================
    if SnackCombo.query.count() == 0:
        print("🍿  Seeding Snack Combos...")
        combos = [
            SnackCombo(
                id=generate_uuid(),
                name=c["name"],
                description=c.get("description"),
                price=c["price"],
                image_url=c.get("image_url", "https://via.placeholder.com/300x200")
            )
            for c in data["snack_combos"]
        ]
        db.session.bulk_save_objects(combos)
        db.session.commit()

    # ======================================================
    # Seed Demo User
    # ======================================================
    if User.query.count() == 0:
        print("👤  Creating demo user...")
        user = User(
            id=generate_uuid(),
            username="demo_user",
            email="demo@example.com",
            password="hashed_demo_password"   # bạn tự hash lại nhé
        )
        db.session.add(user)
        db.session.commit()

    # ======================================================
    # Seed Ticket Types
    # ======================================================
    if TicketType.query.count() == 0:
        print("🎟️  Seeding Ticket Types...")
        ticket_types = [
            TicketType(
                id=generate_uuid(),
                name="Student Ticket",
                description="Standard seat in 2D room",
                base_price=90000,
                room_type="Standard"
            ),
            TicketType(
                id=generate_uuid(),
                name="Adult Ticket",
                description="Premium IMAX seat",
                base_price=150000,
                room_type="Deluxe"
            ),
            TicketType(
                id=generate_uuid(),
                name="VIP Ticket",
                description="VIP 3D seat",
                base_price=200000,
                room_type="Deluxe"
            )
        ]
        db.session.bulk_save_objects(ticket_types)
        db.session.commit()

    print("\n✅ Seeding completed successfully!\n")


if __name__ == "__main__":
    seed_from_json()
