from flask import Blueprint
from flasgger.utils import swag_from
from controllers.seat_controllers import (
    get_seats,
    get_seat,
    create_seat,
    update_seat,
    delete_seat
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
