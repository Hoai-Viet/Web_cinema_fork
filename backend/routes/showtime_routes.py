from flask import Blueprint
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
# Routes mapping
# -------------------------------
showtime_routes.route("/showtimes", methods=["GET"])(get_showtimes)
showtime_routes.route("/showtimes/<showtime_id>", methods=["GET"])(get_showtime)
showtime_routes.route("/showtimes", methods=["POST"])(create_showtime)
showtime_routes.route("/showtimes/<showtime_id>", methods=["PUT"])(update_showtime)
showtime_routes.route("/showtimes/<showtime_id>", methods=["DELETE"])(delete_showtime)
showtime_routes.route("/showtimes/<showtime_id>/available-seats", methods=["GET"])(get_available_seats)
