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
    birthday = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    tickets = db.relationship("Ticket", backref="user", lazy=True)


class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False, unique=True)
    cinemas = db.relationship("Cinema", backref="city", lazy=True)


class Cinema(db.Model):
    __tablename__ = "cinemas"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    city_id = db.Column(db.String(36), db.ForeignKey("cities.id"), nullable=False)
    rooms = db.relationship("Room", backref="cinema", lazy=True)


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    cinema_id = db.Column(db.String(36), db.ForeignKey("cinemas.id"), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    room_type = db.Column(db.Enum("Standard", "Deluxe", name="room_types"), nullable=False)
    seats = db.relationship("Seat", backref="room", lazy=True)
    showtimes = db.relationship("Showtime", backref="room", lazy=True)

class Seat(db.Model):
    __tablename__ = "seats"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False)
    seat_number = db.Column(db.String(10), nullable=False)
    seat_type = db.Column(db.Enum("Single", "Double", name="seat_types"), nullable=False)

    tickets = db.relationship("Ticket", backref="seat", lazy=True)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer, nullable=False)
    movie_content = db.Column(db.Text)
    poster_url = db.Column(db.Text)
    country = db.Column(db.String(100))
    age_rating = db.Column(db.String(10))
    language = db.Column(db.String(50))
    status = db.Column(db.Enum("Now Showing", "Coming Soon", name="movie_statuses"), default="Coming Soon")
    showtimes = db.relationship("Showtime", backref="movie", lazy=True)



class Showtime(db.Model):
    __tablename__ = "showtimes"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    movie_id = db.Column(db.String(36), db.ForeignKey("movies.id"), nullable=False)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime)
    tickets = db.relationship("Ticket", backref="showtime", lazy=True)


class TicketType(db.Model):
    __tablename__ = "ticket_types"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    base_price = db.Column(db.Float, nullable=False)
    room_type = db.Column(db.Enum("Standard", "Deluxe", name="ticket_room_types"), nullable=False)
    tickets = db.relationship("Ticket", backref="ticket_type", lazy=True)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False)
    showtime_id = db.Column(db.String(36), db.ForeignKey("showtimes.id"), nullable=False)
    seat_id = db.Column(db.String(36), db.ForeignKey("seats.id"), nullable=False)
    ticket_type_id = db.Column(db.String(36), db.ForeignKey("ticket_types.id"), nullable=False)
    price = db.Column(db.Float, nullable=False)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow)
    snacks = db.relationship("SnackCombo", secondary="ticket_snack", backref="tickets")


class SnackCombo(db.Model):
    __tablename__ = "snack_combos"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)
Combo = SnackCombo
ticket_snack = db.Table(
    "ticket_snack",
    db.Column("ticket_id", db.String(36), db.ForeignKey("tickets.id"), primary_key=True),
    db.Column("snack_id", db.String(36), db.ForeignKey("snack_combos.id"), primary_key=True),
    db.Column("quantity", db.Integer, default=1)
)

class Payment(db.Model):
    __tablename__ = "payments"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    ticket_id = db.Column(db.String(36), db.ForeignKey("tickets.id"), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(db.Enum("Cash", name="payment_methods"), nullable=False)
    status = db.Column(db.Enum("Pending", "Completed", "Failed", name="payment_statuses"), default="Pending")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

class Promotion(db.Model):
    __tablename__ = "promotions"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.Text)

class TicketCombo(db.Model):
    __tablename__ = "ticket_combos"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    ticket_id = db.Column(db.String(36), db.ForeignKey("tickets.id"), nullable=False)
    combo_id = db.Column(db.String(36), db.ForeignKey("snack_combos.id"), nullable=False)
    quantity = db.Column(db.Integer, default=1)

    ticket = db.relationship("Ticket", backref="ticket_combos")
    combo = db.relationship("SnackCombo", backref="ticket_combos")
