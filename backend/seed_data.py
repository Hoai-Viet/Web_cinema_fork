# seed_data.py
import json
from datetime import datetime, timedelta
from app import create_app
from models import db, City, Cinema, Room, Movie, Seat, Showtime, SnackCombo
from models import generate_uuid

app = create_app()
app.app_context().push()

def seed_from_json():
    print("Bắt đầu seed dữ liệu từ data.json...")

    with open("data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # --- Seed Cities ---
    if City.query.count() == 0:
        print("Thêm thành phố...")
        cities = [City(id=generate_uuid(), name=c["name"]) for c in data["cities"]]
        db.session.bulk_save_objects(cities)
        db.session.commit()

    # --- Seed Cinemas ---
    if Cinema.query.count() == 0:
        print("Thêm rạp chiếu...")
        cinemas = []
        for c in data["cinemas"]:
            city = City.query.filter_by(name=c["city"]).first()
            if not city:
                print(f"Không tìm thấy thành phố: {c['city']}")
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
        print("Thêm phòng chiếu...")
        rooms = []
        for r in data["rooms"]:
            cinema = Cinema.query.filter_by(name=r["cinema"]).first()
            if not cinema:
                print(f"Không tìm thấy rạp: {r['cinema']}")
                continue
            if r["room_type"] not in ['2D', '3D', 'IMAX']:
                print(f"Loại phòng không hợp lệ: {r['room_type']}")
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
        print("Thêm phim...")
        movies = []
        for m in data["movies"]:
            status = m.get("status", "Coming Soon")
            if status not in ["Now Showing", "Coming Soon"]:
                status = "Coming Soon"
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
                status=status
            ))
        db.session.bulk_save_objects(movies)
        db.session.commit()

    # --- Seed Seats (tự động theo total_seats) ---
    if Seat.query.count() == 0:
        print("Tạo ghế tự động cho từng phòng...")
        seats = []
        rooms = Room.query.all()
        for room in rooms:
            total = room.total_seats
            for i in range(1, total + 1):
                seat_number = f"{chr(64 + (i-1) // 10 + 1)}{(i-1) % 10 + 1}"  # A1, A2, ..., B1
                seat_type = "VIP" if i <= total // 4 else "Sweetbox" if i > total * 3 // 4 else "Standard"
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
        print("Thêm suất chiếu mẫu...")
        movie = Movie.query.first()
        room = Room.query.first()
        if not movie or not room:
            print("Không có phim hoặc phòng để tạo suất chiếu")
        else:
            base_time = datetime.utcnow().replace(minute=0, second=0, microsecond=0)
            showtimes = [
                Showtime(
                    id=generate_uuid(),
                    movie_id=movie.id,
                    room_id=room.id,
                    start_time=base_time + timedelta(hours=14),
                    end_time=base_time + timedelta(hours=16, minutes=movie.duration_minutes)
                ),
                Showtime(
                    id=generate_uuid(),
                    movie_id=movie.id,
                    room_id=room.id,
                    start_time=base_time + timedelta(hours=18),
                    end_time=base_time + timedelta(hours=20, minutes=movie.duration_minutes)
                ),
                Showtime(
                    id=generate_uuid(),
                    movie_id=movie.id,
                    room_id=room.id,
                    start_time=base_time + timedelta(days=1, hours=15),
                    end_time=base_time + timedelta(days=1, hours=17, minutes=movie.duration_minutes)
                )
            ]
            db.session.bulk_save_objects(showtimes)
            db.session.commit()

    # --- Seed Snack Combos ---
    if SnackCombo.query.count() == 0:
        print("Thêm combo đồ ăn...")
        combos = []
        for c in data["snack_combos"]:
            combos.append(SnackCombo(
                id=generate_uuid(),
                name=c["name"],
                description=c.get("description"),
                price=c["price"],
                image_url=c.get("image_url", "https://via.placeholder.com/300x200?text=Combo")
            ))
        db.session.bulk_save_objects(combos)
        db.session.commit()

    print("Seed dữ liệu hoàn tất!")


if __name__ == "__main__":
    seed_from_json()