from flask import Blueprint
from controllers.room_controllers import (
    get_rooms,
    get_room,
    create_room,
    update_room,
    delete_room
)

room_routes = Blueprint("room_routes", __name__)

# ---------------------------
# Routes
# ---------------------------
room_routes.route("/rooms", methods=["GET"])(get_rooms)
room_routes.route("/rooms/<room_id>", methods=["GET"])(get_room)
room_routes.route("/rooms", methods=["POST"])(create_room)
room_routes.route("/rooms/<room_id>", methods=["PUT"])(update_room)
room_routes.route("/rooms/<room_id>", methods=["DELETE"])(delete_room)
