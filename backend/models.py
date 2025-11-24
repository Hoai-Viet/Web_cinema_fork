from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import uuid

db = SQLAlchemy()


def generate_uuid():
    return str(uuid.uuid4())


# Association table for Ticket <-> SnackCombo (many-to-many)
ticket_snack = db.Table(
    "ticket_snack",
    db.Column("ticket_id", db.String(36), db.ForeignKey("tickets.id"), primary_key=True),
    db.Column("snack_combo_id", db.String(36), db.ForeignKey("snack_combos.id"), primary_key=True),
    db.Column("quantity", db.Integer, default=1, nullable=False)
)


class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    username = db.Column(db.String(50), unique=True, nullable=False, index=True)
    email = db.Column(db.String(255), unique=True, nullable=False, index=True)
    birthday = db.Column(db.Date, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tickets = db.relationship("Ticket", back_populates="user", lazy=True, cascade="all, delete-orphan")


class City(db.Model):
    __tablename__ = "cities"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False, unique=True)

    cinemas = db.relationship("Cinema", back_populates="city", lazy=True, cascade="all, delete-orphan")


class Cinema(db.Model):
    __tablename__ = "cinemas"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(255), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(50))
    city_id = db.Column(db.String(36), db.ForeignKey("cities.id"), nullable=False, index=True)

    city = db.relationship("City", back_populates="cinemas")
    rooms = db.relationship("Room", back_populates="cinema", lazy=True, cascade="all, delete-orphan")


class Room(db.Model):
    __tablename__ = "rooms"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    cinema_id = db.Column(db.String(36), db.ForeignKey("cinemas.id"), nullable=False, index=True)
    name = db.Column(db.String(100), nullable=False)
    total_seats = db.Column(db.Integer, nullable=False)
    room_type = db.Column(
        db.Enum('2D', '3D', 'IMAX', name='room_types'),
        nullable=False
    )

    cinema = db.relationship("Cinema", back_populates="rooms")
    seats = db.relationship("Seat", back_populates="room", lazy=True, cascade="all, delete-orphan")
    showtimes = db.relationship("Showtime", back_populates="room", lazy=True, cascade="all, delete-orphan")


class Seat(db.Model):
    __tablename__ = "seats"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False, index=True)
    seat_number = db.Column(db.String(10), nullable=False)
    seat_type = db.Column(
        db.Enum('Standard', 'VIP', 'Sweetbox', name='seat_types'),
        nullable=False
    )

    room = db.relationship("Room", back_populates="seats")
    tickets = db.relationship("Ticket", back_populates="seat", lazy=True)

    __table_args__ = (db.UniqueConstraint('room_id', 'seat_number', name='uix_room_seat'),)


class Movie(db.Model):
    __tablename__ = "movies"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False, index=True)
    description = db.Column(db.Text)
    genre = db.Column(db.String(100))
    duration_minutes = db.Column(db.Integer, nullable=False)
    movie_content = db.Column(db.Text)
    poster_url = db.Column(db.Text)
    country = db.Column(db.String(100))
    age_rating = db.Column(db.String(10))
    language = db.Column(db.String(50))
    status = db.Column(
        db.Enum("Now Showing", "Coming Soon", name="movie_statuses"),
        default="Coming Soon",
        nullable=False
    )

    showtimes = db.relationship("Showtime", back_populates="movie", lazy=True, cascade="all, delete-orphan")


class Showtime(db.Model):
    __tablename__ = "showtimes"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    movie_id = db.Column(db.String(36), db.ForeignKey("movies.id"), nullable=False, index=True)
    room_id = db.Column(db.String(36), db.ForeignKey("rooms.id"), nullable=False, index=True)
    start_time = db.Column(db.DateTime, nullable=False, index=True)
    end_time = db.Column(db.DateTime)

    movie = db.relationship("Movie", back_populates="showtimes")
    room = db.relationship("Room", back_populates="showtimes")
    tickets = db.relationship("Ticket", back_populates="showtime", lazy=True, cascade="all, delete-orphan")

    __table_args__ = (db.UniqueConstraint('room_id', 'start_time', name='uix_room_starttime'),)


class TicketType(db.Model):
    __tablename__ = "ticket_types"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255))
    base_price = db.Column(db.Float, nullable=False)
    room_type = db.Column(
        db.Enum("Standard", "Deluxe", name="ticket_room_types"),
        nullable=False
    )

    tickets = db.relationship("Ticket", back_populates="ticket_type", lazy=True)


class Ticket(db.Model):
    __tablename__ = "tickets"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)
    showtime_id = db.Column(db.String(36), db.ForeignKey("showtimes.id"), nullable=False, index=True)
    seat_id = db.Column(db.String(36), db.ForeignKey("seats.id"), nullable=False, index=True)
    ticket_type_id = db.Column(db.String(36), db.ForeignKey("ticket_types.id"), nullable=False, index=True)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False, default=1)
    booked_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # New: one snack combo per ticket
    snack_id = db.Column(db.String(36), db.ForeignKey("snack_combos.id"), nullable=True)
    snack = db.relationship("SnackCombo", back_populates="tickets")

    user = db.relationship("User", back_populates="tickets")
    showtime = db.relationship("Showtime", back_populates="tickets")
    seat = db.relationship("Seat", back_populates="tickets")
    ticket_type = db.relationship("TicketType", back_populates="tickets")

    payment_id = db.Column(db.String(36), db.ForeignKey("payments.id"), nullable=True)
    payment = db.relationship("Payment", back_populates="tickets")



class SnackCombo(db.Model):
    __tablename__ = "snack_combos"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(255))
    price = db.Column(db.Float, nullable=False)
    image_url = db.Column(db.Text)

    # updated relationship
    tickets = db.relationship("Ticket", back_populates="snack", lazy=True)



class Payment(db.Model):
    __tablename__ = "payments"

    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey("users.id"), nullable=False, index=True)

    amount = db.Column(db.Float, nullable=False)
    payment_method = db.Column(
        db.Enum("Cash", "Credit Card", "Momo", "ZaloPay", name="payment_methods"),
        nullable=False
    )
    status = db.Column(
        db.Enum("Pending", "Completed", "Failed", name="payment_statuses"),
        default="Pending",
        nullable=False
    )
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    tickets = db.relationship("Ticket", back_populates="payment", lazy=True)




class Promotion(db.Model):
    __tablename__ = "promotions"
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    discount_percent = db.Column(db.Float, nullable=False)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    image_url = db.Column(db.Text)

    __table_args__ = (
        db.CheckConstraint('discount_percent >= 0 AND discount_percent <= 100', name='check_discount_range'),
    )