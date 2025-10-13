from flask import Blueprint, request
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

@ticket_routes.route("/tickets", methods=["GET"])
def get_tickets():
    return get_all_tickets()

@ticket_routes.route("/tickets/<ticket_id>", methods=["GET"])
def get_ticket(ticket_id):
    return get_ticket_by_id(ticket_id)

@ticket_routes.route("/tickets/user/<user_id>", methods=["GET"])
def get_user_tickets(user_id):
    return get_tickets_by_user(user_id)

@ticket_routes.route("/tickets", methods=["POST"])
def add_ticket():
    data = request.get_json()
    return create_ticket(data)

@ticket_routes.route("/tickets/<ticket_id>", methods=["PUT"])
def modify_ticket(ticket_id):
    data = request.get_json()
    return update_ticket(ticket_id, data)

@ticket_routes.route("/tickets/<ticket_id>", methods=["DELETE"])
def cancel_ticket(ticket_id):
    return delete_ticket(ticket_id)

@ticket_routes.route("/tickets/available-seats/<showtime_id>", methods=["GET"])
def available_seats(showtime_id):
    return get_available_seats(showtime_id)

@ticket_routes.route("/tickets/details/<ticket_id>", methods=["GET"])
def ticket_details(ticket_id):
    return get_ticket_details(ticket_id)
