from flask import Blueprint, request
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from controllers.tickets_controllers import (
    get_all_tickets,
    get_ticket_by_id,
    get_tickets_by_user,
    create_ticket,
    update_ticket,
    delete_ticket,
    get_available_seats,
    get_ticket_details,
    get_ticket_types_by_showtime
)

ticket_routes = Blueprint("ticket_routes", __name__)

# ✅ Lấy tất cả vé
@ticket_routes.route("/tickets", methods=["GET"])
@jwt_required()
@swag_from("../swagger/ticket/get_all_tickets.yaml")
def get_tickets():
    """Get all tickets"""
    return get_all_tickets()


# ✅ Xem chi tiết 1 vé
@ticket_routes.route("/tickets/<int:ticket_id>", methods=["GET"])
@jwt_required()
@swag_from("../swagger/ticket/get_ticket_by_id.yaml")
def get_ticket(ticket_id):
    """Get a ticket by ID"""
    return get_ticket_by_id(ticket_id)


# ✅ Xem vé của 1 user
@ticket_routes.route("/tickets/user/<int:user_id>", methods=["GET"])
@jwt_required()
@swag_from("../swagger/ticket/get_tickets_by_user.yaml")
def get_user_tickets(user_id):
    """Get tickets of a specific user"""
    return get_tickets_by_user(user_id)


# ✅ Đặt vé mới
@ticket_routes.route("/tickets", methods=["POST"])
@jwt_required()
@swag_from("../swagger/ticket/create_ticket.yaml")
def add_ticket():
    """Create a new ticket"""
    data = request.get_json()
    return create_ticket(data)


# ✅ Cập nhật vé
@ticket_routes.route("/tickets/<int:ticket_id>", methods=["PUT"])
@jwt_required()
@swag_from("../swagger/ticket/update_ticket.yaml")
def modify_ticket(ticket_id):
    """Update a ticket"""
    data = request.get_json()
    return update_ticket(ticket_id, data)


# ✅ Hủy vé
@ticket_routes.route("/tickets/<int:ticket_id>", methods=["DELETE"])
@jwt_required()
@swag_from("../swagger/ticket/delete_ticket.yaml")
def cancel_ticket(ticket_id):
    """Delete (cancel) a ticket"""
    return delete_ticket(ticket_id)


# ✅ Lấy ghế trống của suất chiếu
@ticket_routes.route("/tickets/available-seats/<int:showtime_id>", methods=["GET"])
@jwt_required()
@swag_from("../swagger/ticket/get_available_seats.yaml")
def available_seats(showtime_id):
    """Get available seats for a showtime"""
    return get_available_seats(showtime_id)


# ✅ Xem chi tiết vé
@ticket_routes.route("/tickets/details/<int:ticket_id>", methods=["GET"])
@jwt_required()
@swag_from("../swagger/ticket/get_ticket_details.yaml")
def ticket_details(ticket_id):
    """Get detailed information of a ticket"""
    return get_ticket_details(ticket_id)

# ✅ Get ticket types by showtime ID
@ticket_routes.route("/showtime/<string:showtime_id>/ticket-types", methods=["GET"])
@jwt_required()
def route_get_ticket_types_by_showtime(showtime_id):
    return get_ticket_types_by_showtime(showtime_id)