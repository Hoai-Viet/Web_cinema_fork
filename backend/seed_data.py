from app import db, create_app
from models import User, Movie, Cinema, Room, Seat, Showtime, Ticket, generate_uuid
import json
from datetime import datetime

# ✅ Khởi tạo Flask app trước khi mở context
app = create_app()

# Đọc dữ liệu và seed
with app.app_context():  
    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    print("🚀 Bắt đầu seed dữ liệu...")

    # ======== 1️⃣ Thêm Cinema ========
    print("🏢 Thêm rạp chiếu phim...")
    cinemas = []
    for c in data["cinemas"]:
        cinema = Cinema(
            id=generate_uuid(),
            name=c["name"],
            address=c["address"],
            phone=c["phone"]
        )
        cinemas.append(cinema)
    db.session.add_all(cinemas)
    db.session.commit()

    # ======== 2️⃣ Thêm Movie ========
    print("🎬 Thêm phim...")
    movies = []
    for m in data["movies"]:
        movie = Movie(
            id=generate_uuid(),
            title=m["title"],
            genre=m["genre"],
            duration_minutes=m["duration_minutes"],
            country=m.get("country"),
            age_rating=m.get("age_rating")
        )
        movies.append(movie)
    db.session.add_all(movies)
    db.session.commit()

    # ======== 3️⃣ Thêm Room ========
    print("🏠 Thêm phòng...")
    rooms = []
    for r in data["rooms"]:
        cinema_index = r["cinema_id"] - 1
        if 0 <= cinema_index < len(cinemas):
            room = Room(
                id=generate_uuid(),
                cinema_id=cinemas[cinema_index].id,
                name=r["name"],
                total_seats=r["total_seats"]
            )
            rooms.append(room)
    db.session.add_all(rooms)
    db.session.commit()

    # ======== 4️⃣ Thêm Seat ========
    print("💺 Thêm ghế...")
    seats = []
    for s in data["seats"]:
        room_index = s["room_id"] - 1
        if 0 <= room_index < len(rooms):
            seat = Seat(
                id=generate_uuid(),
                room_id=rooms[room_index].id,
                seat_number=s["seat_number"],
                seat_type=s["seat_type"]
            )
            seats.append(seat)
    db.session.add_all(seats)
    db.session.commit()

    # ======== 5️⃣ Thêm User ========
    print("👤 Thêm người dùng...")
    users = []
    for u in data["users"]:
        user = User(
            id=generate_uuid(),
            username=u["username"],
            email=u["email"],
            password=u["password"]
        )
        users.append(user)
    db.session.add_all(users)
    db.session.commit()

    # ======== 6️⃣ Thêm Showtime ========
    print("🕒 Thêm suất chiếu...")
    showtimes = []
    for s in data["showtimes"]:
        movie_index = s["movie_id"] - 1
        room_index = s["room_id"] - 1
        if 0 <= movie_index < len(movies) and 0 <= room_index < len(rooms):
            showtime = Showtime(
                id=generate_uuid(),
                movie_id=movies[movie_index].id,
                room_id=rooms[room_index].id,
                start_time=datetime.fromisoformat(s["start_time"])
            )
            showtimes.append(showtime)
    db.session.add_all(showtimes)
    db.session.commit()

    # ======== 7️⃣ Thêm Ticket ========
    print("🎟️ Thêm vé...")
    tickets = []
    for t in data["tickets"]:
        user_index = t["user_id"] - 1
        showtime_index = t["showtime_id"] - 1
        seat_index = t["seat_id"] - 1
        if (
            0 <= user_index < len(users)
            and 0 <= showtime_index < len(showtimes)
            and 0 <= seat_index < len(seats)
        ):
            ticket = Ticket(
                id=generate_uuid(),
                user_id=users[user_index].id,
                showtime_id=showtimes[showtime_index].id,
                seat_id=seats[seat_index].id,
                price=t["price"]
            )
            tickets.append(ticket)
    db.session.add_all(tickets)
    db.session.commit()

    print("✅ Seed dữ liệu hoàn tất!")
