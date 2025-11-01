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
@swag_from("../swagger/seat.yaml", endpoint="get_seats", methods=["GET"])
def route_get_seats():
    return get_seats()

@seat_routes.route("/seats/<seat_id>", methods=["GET"])
@swag_from("../swagger/seat.yaml", endpoint="get_seat", methods=["GET"])
def route_get_seat(seat_id):
    return get_seat(seat_id)

@seat_routes.route("/seats", methods=["POST"])
@swag_from("../swagger/seat.yaml", endpoint="create_seat", methods=["POST"])
def route_create_seat():
    return create_seat()

@seat_routes.route("/seats/<seat_id>", methods=["PUT"])
@swag_from("../swagger/seat.yaml", endpoint="update_seat", methods=["PUT"])
def route_update_seat(seat_id):
    return update_seat(seat_id)

@seat_routes.route("/seats/<seat_id>", methods=["DELETE"])
@swag_from("../swagger/seat.yaml", endpoint="delete_seat", methods=["DELETE"])
def route_delete_seat(seat_id):
    return delete_seat(seat_id)
