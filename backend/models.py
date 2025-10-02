from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)   # <- plain text
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    tickets = db.relationship("Ticket", backref="user", lazy=True)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    duration_minutes = db.Column(db.Integer, nullable=False)
    genre = db.Column(db.String(100))
    release_date = db.Column(db.Date)
    poster_url = db.Column(db.Text)

    showtimes = db.relationship("Showtime", backref="movie", lazy=True)

class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)

    seats = db.relationship("Seat", backref="room", lazy=True)
    showtimes = db.relationship("Showtime", backref="room", lazy=True)

class Seat(db.Model):
    __tablename__ = "seats"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False)

    seat_number = db.Column(db.String(10), nullable=False)  # VD: A1, A2, B5
    seat_type = db.Column(db.Enum("Single", "Double", name="seat_types"), nullable=False)  
    tickets = db.relationship("Ticket", backref="seat", lazy=True)


class Showtime(db.Model):
    __tablename__ = "showtimes"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    movie_id = db.Column(db.String(36), db.ForeignKey("movies.id"), nullable=False)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)

    tickets = db.relationship("Ticket", backref="showtime", lazy=True)

class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    showtime_id = db.Column(db.String(36), db.ForeignKey("showtimes.id"), nullable=False)
    seat_id = db.Column(db.String(36), db.ForeignKey("seats.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
