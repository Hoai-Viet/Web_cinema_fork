from flask import Blueprint
from controllers.seat_controllers import (
    get_seats,
    get_seat,
    create_seat,
    update_seat,
    delete_seat
)

seat_routes = Blueprint("seat_routes", __name__)

# ---------------------------
# Routes mapping
# ---------------------------
seat_routes.route("/seats", methods=["GET"])(get_seats)
seat_routes.route("/seats/<seat_id>", methods=["GET"])(get_seat)
seat_routes.route("/seats", methods=["POST"])(create_seat)
seat_routes.route("/seats/<seat_id>", methods=["PUT"])(update_seat)
seat_routes.route("/seats/<seat_id>", methods=["DELETE"])(delete_seat)
