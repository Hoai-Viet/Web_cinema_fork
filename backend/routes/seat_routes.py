from flask import Blueprint
from flasgger.utils import swag_from
from controllers.seat_controllers import (
    get_seats,
    get_seat,
    create_seat,
    update_seat,
    delete_seat,
    get_seats_by_room,
    get_seats_status,
    book_multiple_seats,
    get_seats_by_cinema,
    get_seats_for_showtime,
    get_seats_status_by_showtime
    
)


seat_routes = Blueprint("seat_routes", __name__)

# ---------------------------
# Routes mapping + Swagger docs
# ---------------------------

@seat_routes.route("/seats", methods=["GET"])
@swag_from("../swagger/seat/get_seats.yaml")
def route_get_seats():
    """Get all seats"""
    return get_seats()


@seat_routes.route("/seats/<int:seat_id>", methods=["GET"])
@swag_from("../swagger/seat/get_seat.yaml")
def route_get_seat(seat_id):
    """Get seat by ID"""
    return get_seat(seat_id)


@seat_routes.route("/seats", methods=["POST"])
@swag_from("../swagger/seat/create_seat.yaml")
def route_create_seat():
    """Create a new seat"""
    return create_seat()


@seat_routes.route("/seats/<int:seat_id>", methods=["PUT"])
@swag_from("../swagger/seat/update_seat.yaml")
def route_update_seat(seat_id):
    """Update an existing seat"""
    return update_seat(seat_id)


@seat_routes.route("/seats/<int:seat_id>", methods=["DELETE"])
@swag_from("../swagger/seat/delete_seat.yaml")
def route_delete_seat(seat_id):
    """Delete a seat"""
    return delete_seat(seat_id)

@seat_routes.route("/room/<room_id>", methods=["GET"])
@swag_from("../swagger/seat/get_seats_by_room.yaml")
def handle_get_seats_by_room(room_id):
    return get_seats_by_room(room_id)

@seat_routes.route("/status/<showtime_id>", methods=["GET"])
@swag_from("../swagger/seat/get_seats_by_status.yaml")
def handle_get_seats_status(showtime_id):
    return get_seats_status(showtime_id)


@seat_routes.route("/book", methods=["POST"])
@swag_from("../swagger/seat/book_multiple_seats.yaml")
def handle_book_multiple_seats():
    return book_multiple_seats()


@seat_routes.route("/cinema/<cinema_id>", methods=["GET"])
@swag_from("../swagger/seat/get_seats_by_cinema.yaml")
def handle_get_seats_by_cinema(cinema_id):
    return get_seats_by_cinema(cinema_id)

@seat_routes.route("/<showtime_id>/status", methods=["GET"])
# @swag_from("../swagger/seat/get_seats_status_by_showtime.yaml")
def route_get_seat_status_by_showtime(showtime_id):
    return get_seats_status_by_showtime(showtime_id)

@seat_routes.route("/<showtime_id>/seats", methods=["GET"])
# @swag_from("../swagger/seat/get_seats_for_showtime.yaml")
def route_get_seats_for_showtime(showtime_id):
    return get_seats_for_showtime(showtime_id)