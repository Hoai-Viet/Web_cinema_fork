from flask import Blueprint, request
from flasgger.utils import swag_from

from controllers.showtime_controllers import (
    get_showtimes,
    get_showtime,
    create_showtime,
    update_showtime,
    delete_showtime,
    get_available_seats,
    get_showtimes_by_movie,
    get_cinema_by_showtime
)

showtime_routes = Blueprint("showtime_routes", __name__)

# --------------------------------------
# Get all showtimes
# --------------------------------------
@showtime_routes.route("/showtimes", methods=["GET"])
# @swag_from("../swagger/showtime/get_showtimes.yaml")
def route_get_showtimes():
    return get_showtimes()


# --------------------------------------
# Get showtime by ID
# --------------------------------------
@showtime_routes.route("/showtimes/<string:showtime_id>", methods=["GET"])
# @swag_from("../swagger/showtime/get_showtime.yaml")
def route_get_showtime(showtime_id):
    return get_showtime(showtime_id)


# --------------------------------------
# Create showtime
# --------------------------------------
@showtime_routes.route("/showtimes", methods=["POST"])
# @swag_from("../swagger/showtime/create_showtime.yaml")
def route_create_showtime():
    data = request.get_json()
    return create_showtime(data)


# --------------------------------------
# Update showtime
# --------------------------------------
@showtime_routes.route("/showtimes/<string:showtime_id>", methods=["PUT"])
# @swag_from("../swagger/showtime/update_showtime.yaml")
def route_update_showtime(showtime_id):
    data = request.get_json()
    return update_showtime(showtime_id, data)


# --------------------------------------
# Delete showtime
# --------------------------------------
@showtime_routes.route("/showtimes/<string:showtime_id>", methods=["DELETE"])
# @swag_from("../swagger/showtime/delete_showtime.yaml")
def route_delete_showtime(showtime_id):
    return delete_showtime(showtime_id)


# --------------------------------------
# Get available seats for a showtime
# --------------------------------------
@showtime_routes.route("/showtimes/<string:showtime_id>/available-seats", methods=["GET"])
# @swag_from("../swagger/showtime/get_available_seats.yaml")
def route_get_available_seats(showtime_id):
    return get_available_seats(showtime_id)


# --------------------------------------
# ✅ Get showtimes by movie ID
# --------------------------------------
@showtime_routes.route("/movies/<string:movie_id>/showtimes", methods=["GET"])
# @swag_from("../swagger/showtime/get_showtimes_by_movie.yaml")
def route_get_showtimes_by_movie(movie_id):
    return get_showtimes_by_movie(movie_id)
     
@showtime_routes.route("/showtime/<int:showtime_id>/cinema", methods=["GET"])
def route_get_cinema_by_showtime(showtime_id):
    return get_cinema_by_showtime(showtime_id)