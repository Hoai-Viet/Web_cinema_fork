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


# 13
@seat_routes.route("/<showtime_id>/seats", methods=["GET"])
# @swag_from("../swagger/seat/get_seats_for_showtime.yaml")
def route_get_seats_for_showtime(showtime_id):
    return get_seats_for_showtime(showtime_id)