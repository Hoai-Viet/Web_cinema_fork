from flask import Blueprint
from flasgger.utils import swag_from
from controllers.showtime_controllers import (
    get_showtimes,
    get_showtime,
    create_showtime,
    update_showtime,
    delete_showtime,
    get_available_seats
)

showtime_routes = Blueprint("showtime_routes", __name__)

# -------------------------------
# Routes mapping (Swagger)
# -------------------------------

@showtime_routes.route("/showtimes", methods=["GET"])
@swag_from("../swagger/showtime.yaml")
def route_get_showtimes():
    return get_showtimes()


@showtime_routes.route("/showtimes/<showtime_id>", methods=["GET"])
@swag_from("../swagger/showtime.yaml")
def route_get_showtime(showtime_id):
    return get_showtime(showtime_id)


@showtime_routes.route("/showtimes", methods=["POST"])
@swag_from("../swagger/showtime.yaml")
def route_create_showtime():
    return create_showtime()


@showtime_routes.route("/showtimes/<showtime_id>", methods=["PUT"])
@swag_from("../swagger/showtime.yaml")
def route_update_showtime(showtime_id):
    return update_showtime(showtime_id)


@showtime_routes.route("/showtimes/<showtime_id>", methods=["DELETE"])
# @swag_from("docs/showtime/delete_showtime.yaml")
def route_delete_showtime(showtime_id):
    return delete_showtime(showtime_id)


@showtime_routes.route("/showtimes/<showtime_id>/available-seats", methods=["GET"])
# @swag_from("docs/showtime/get_available_seats.yaml")
def route_get_available_seats(showtime_id):
    return get_available_seats(showtime_id)
