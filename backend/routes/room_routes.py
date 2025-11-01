from flask import Blueprint
from flasgger.utils import swag_from
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

# 🟢 Lấy danh sách tất cả phòng
@room_routes.route("/rooms", methods=["GET"])
@swag_from("../swagger/room.yaml")
def route_get_rooms():
    return get_rooms()

# 🟢 Lấy chi tiết 1 phòng
@room_routes.route("/rooms/<string:room_id>", methods=["GET"])
@swag_from("../swagger/room.yaml")
def route_get_room(room_id):
    return get_room(room_id)

# 🟢 Tạo phòng mới
@room_routes.route("/rooms", methods=["POST"])
@swag_from("../swagger/room.yaml")
def route_create_room():
    return create_room()

# 🟢 Cập nhật thông tin phòng
@room_routes.route("/rooms/<string:room_id>", methods=["PUT"])
@swag_from("../swagger/room.yaml")
def route_update_room(room_id):
    return update_room(room_id)

# 🟢 Xóa phòng
@room_routes.route("/rooms/<string:room_id>", methods=["DELETE"])
@swag_from("../swagger/room.yaml")
def route_delete_room(room_id):
    return delete_room(room_id)
