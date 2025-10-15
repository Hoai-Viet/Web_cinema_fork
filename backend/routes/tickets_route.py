from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from controllers.tickets_controllers import (
    get_all_tickets,
    get_ticket_by_id,
    get_tickets_by_user,
    create_ticket,
    update_ticket,
    delete_ticket,
    get_available_seats,
    get_ticket_details
)

ticket_routes = Blueprint("ticket_routes", __name__)

# ✅ Chỉ admin hoặc nhân viên mới nên xem tất cả vé
@ticket_routes.route("/tickets", methods=["GET"])
@jwt_required()
def get_tickets():
    return get_all_tickets()

# ✅ Xem chi tiết 1 vé
@ticket_routes.route("/tickets/<ticket_id>", methods=["GET"])
@jwt_required()
def get_ticket(ticket_id):
    return get_ticket_by_id(ticket_id)

# ✅ Xem vé của 1 user (chỉ user đó hoặc admin mới nên xem)
@ticket_routes.route("/tickets/user/<user_id>", methods=["GET"])
@jwt_required()
def get_user_tickets(user_id):
    return get_tickets_by_user(user_id)

# ✅ Tạo vé (chỉ user đã đăng nhập)
@ticket_routes.route("/tickets", methods=["POST"])
@jwt_required()
def add_ticket():
    data = request.get_json()
    return create_ticket(data)

# ✅ Cập nhật vé (chỉ user hoặc admin)
@ticket_routes.route("/tickets/<ticket_id>", methods=["PUT"])
@jwt_required()
def modify_ticket(ticket_id):
    data = request.get_json()
    return update_ticket(ticket_id, data)

# ✅ Hủy vé (chỉ user)
@ticket_routes.route("/tickets/<ticket_id>", methods=["DELETE"])
@jwt_required()
def cancel_ticket(ticket_id):
    return delete_ticket(ticket_id)

# ✅ Lấy ghế trống của suất chiếu (ai đăng nhập mới được xem)
@ticket_routes.route("/tickets/available-seats/<showtime_id>", methods=["GET"])
@jwt_required()
def available_seats(showtime_id):
    return get_available_seats(showtime_id)

# ✅ Xem chi tiết vé (user cần đăng nhập)
@ticket_routes.route("/tickets/details/<ticket_id>", methods=["GET"])
@jwt_required()
def ticket_details(ticket_id):
    return get_ticket_details(ticket_id)
