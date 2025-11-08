import json
from datetime import datetime, timedelta
from app import create_app
from models import (
    db, City, Cinema, Room, Movie, Seat, Showtime, SnackCombo,
    User, TicketType, Ticket, Payment, generate_uuid
)

app = create_app()
app.app_context().push()

def seed_from_json():
    print("🔹 Bắt đầu seed dữ liệu từ data.json...")

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Seed Cities ---
    if City.query.count() == 0:
        print("🗺️  Thêm thành phố...")
        cities = [City(id=generate_uuid(), name=c["name"]) for c in data["cities"]]
        db.session.bulk_save_objects(cities)
        db.session.commit()

    # --- Seed Cinemas ---
    if Cinema.query.count() == 0:
        print("🏢  Thêm rạp chiếu...")
        cinemas = []
        for c in data["cinemas"]:
            city = City.query.filter_by(name=c["city"]).first()
            if not city:
                print(f"⚠️ Không tìm thấy thành phố: {c['city']}")
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

    # --- Seed Rooms ---
    if Room.query.count() == 0:
        print("🎬  Thêm phòng chiếu...")
        rooms = []
        for r in data["rooms"]:
            cinema = Cinema.query.filter_by(name=r["cinema"]).first()
            if not cinema:
                print(f"⚠️ Không tìm thấy rạp: {r['cinema']}")
                continue
            rooms.append(Room(
                id=generate_uuid(),
                cinema_id=cinema.id,
                name=r["name"],
                total_seats=r["total_seats"],
                room_type=r["room_type"]
            ))
        db.session.bulk_save_objects(rooms)
        db.session.commit()

    # --- Seed Movies ---
    if Movie.query.count() == 0:
        print("🎞️  Thêm phim...")
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

    # --- Seed Seats ---
    if Seat.query.count() == 0:
        print("💺  Tạo ghế tự động cho từng phòng...")
        seats = []
        rooms = Room.query.all()
        for room in rooms:
            for i in range(1, room.total_seats + 1):
                row_index = (i - 1) // 10
                seat_number = f"{chr(65 + row_index % 26)}{(i - 1) % 10 + 1}"
                seat_type = (
                    "VIP" if i <= room.total_seats // 4
                    else "Sweetbox" if i > room.total_seats * 3 // 4
                    else "Standard"
                )
                seats.append(Seat(
                    id=generate_uuid(),
                    room_id=room.id,
                    seat_number=seat_number,
                    seat_type=seat_type
                ))
        db.session.bulk_save_objects(seats)
        db.session.commit()

    # --- Seed Showtimes ---
    if Showtime.query.count() == 0:
        print("⏰  Thêm suất chiếu mẫu...")
        movies = Movie.query.filter_by(status="Now Showing").all()
        rooms = Room.query.all()
        if not movies or not rooms:
            print("⚠️ Không có phim hoặc phòng để tạo suất chiếu")
        else:
            showtimes = []
            base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            for movie in movies:
                for room in rooms:
                    start_time = base_time + timedelta(hours=14)
                    end_time = start_time + timedelta(minutes=movie.duration_minutes)
                    showtimes.append(Showtime(
                        id=generate_uuid(),
                        movie_id=movie.id,
                        room_id=room.id,
                        start_time=start_time,
                        end_time=end_time
                    ))
            db.session.bulk_save_objects(showtimes)
            db.session.commit()

    # --- Seed Snack Combos ---
    if SnackCombo.query.count() == 0:
        print("🍿  Thêm combo đồ ăn...")
        combos = [
            SnackCombo(
                id=generate_uuid(),
                name=c["name"],
                description=c.get("description"),
                price=c["price"],
                image_url=c.get("image_url", "https://via.placeholder.com/300x200?text=Combo")
            )
            for c in data["snack_combos"]
        ]
        db.session.bulk_save_objects(combos)
        db.session.commit()

    # --- Seed User Demo ---
    if User.query.count() == 0:
        print("👤  Thêm người dùng demo...")
        demo_user = User(
            id=generate_uuid(),
            username="demo_user",
            email="demo@example.com",
            password="hashed_demo_password"  # nhớ thay bằng hash thật
        )
        db.session.add(demo_user)
        db.session.commit()

    # --- Seed Ticket Types ---
    if TicketType.query.count() == 0:
        print("🎟️  Thêm loại vé...")
        ticket_types = [
            TicketType(
                id=generate_uuid(),
                name="Vé Standard 2D",
                description="Vé thường cho phòng 2D",
                base_price=90000,
                room_type="Standard"
            ),
            TicketType(
                id=generate_uuid(),
                name="Vé Deluxe IMAX",
                description="Vé IMAX cao cấp",
                base_price=150000,
                room_type="Deluxe"
            ),
            TicketType(
                id=generate_uuid(),
                name="Vé VIP 3D",
                description="Ghế VIP phòng 3D",
                base_price=200000,
                room_type="Deluxe"
            )
        ]
        db.session.bulk_save_objects(ticket_types)
        db.session.commit()

    # --- Seed Tickets + Payments ---
    if Ticket.query.count() == 0:
        print("🧾  Thêm vé mẫu và thanh toán...")
        user = User.query.filter_by(username="demo_user").first()
        showtime = Showtime.query.first()
        seats = Seat.query.limit(2).all()
        ticket_type = TicketType.query.first()
        combo = SnackCombo.query.first()

        if not (user and showtime and ticket_type):
            print("⚠️ Thiếu dữ liệu để tạo vé.")
        else:
            tickets = []
            payments = []
            for seat in seats:
                ticket_id = generate_uuid()
                tickets.append(Ticket(
                    id=ticket_id,
                    user_id=user.id,
                    showtime_id=showtime.id,
                    seat_id=seat.id,
                    ticket_type_id=ticket_type.id,
                    price=ticket_type.base_price,
                    snack_combos=[combo]
                ))
                payments.append(Payment(
                    id=generate_uuid(),
                    ticket_id=ticket_id,
                    amount=ticket_type.base_price + combo.price,
                    payment_method="Momo",
                    status="Completed"
                ))
            db.session.bulk_save_objects(tickets)
            db.session.bulk_save_objects(payments)
            db.session.commit()

    print("✅ Seed dữ liệu hoàn tất!")


if __name__ == "__main__":
    seed_from_json()