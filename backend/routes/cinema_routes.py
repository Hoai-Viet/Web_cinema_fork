from flask import Blueprint, request, jsonify
from controllers.cinema_controllers import (
    get_all_cinemas,
    get_cinema_by_id,
    create_new_cinema,
    update_cinema,
    delete_cinema,
    get_rooms_by_cinema
)

cinema_routes = Blueprint("cinema_routes", __name__)

# Lấy danh sách rạp chiếu phim
@cinema_routes.route("/cinemas", methods=["GET"])
def route_get_all_cinemas():
    result = get_all_cinemas()
    return jsonify(result), 200


# Lấy chi tiết 1 rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["GET"])
def route_get_cinema(cinema_id):
    result = get_cinema_by_id(cinema_id)
    if not result:
        return jsonify({"message": "Cinema not found"}), 404
    return jsonify(result), 200


# Thêm rạp chiếu mới
@cinema_routes.route("/cinemas", methods=["POST"])
def route_create_cinema():
    data = request.get_json()
    result, status = create_new_cinema(data)
    return jsonify(result), status


# Cập nhật rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["PUT"])
def route_update_cinema(cinema_id):
    data = request.get_json()
    result, status = update_cinema(cinema_id, data)
    return jsonify(result), status


# Xóa rạp chiếu
@cinema_routes.route("/cinemas/<cinema_id>", methods=["DELETE"])
def route_delete_cinema(cinema_id):
    result, status = delete_cinema(cinema_id)
    return jsonify(result), status


# Lấy danh sách phòng theo rạp
@cinema_routes.route("/cinemas/<cinema_id>/rooms", methods=["GET"])
def route_get_rooms_by_cinema(cinema_id):
    result = get_rooms_by_cinema(cinema_id)
    if not result:
        return jsonify({"message": "Cinema not found"}), 404
    return jsonify(result), 200
