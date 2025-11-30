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
# Get showtimes by movie ID
# --------------------------------------
# 9
@showtime_routes.route("/movies/<string:movie_id>/showtimes", methods=["GET"])
@swag_from("../swagger/showtime/get_showtimes_by_movie.yaml")
def route_get_showtimes_by_movie(movie_id):
    return get_showtimes_by_movie(movie_id)

# 10
# ✅ Get cinema info by showtime ID
@showtime_routes.route("/<string:showtime_id>/cinema", methods=["GET"])
def route_get_cinema_by_showtime(showtime_id):
    return get_cinema_by_showtime(showtime_id)
