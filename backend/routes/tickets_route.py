from flask import Blueprint, request
from controllers.tickets_controllers import (
    get_all_tickets,
    get_ticket_by_id,
    create_ticket,
    update_ticket,
    delete_ticket
)

ticket_routes = Blueprint("ticket_routes", __name__)

# GET all tickets
@ticket_routes.route("/tickets", methods=["GET"])
def get_tickets_route():
    return get_all_tickets()

# GET ticket by id
@ticket_routes.route("/tickets/<ticket_id>", methods=["GET"])
def get_ticket_route(ticket_id):
    return get_ticket_by_id(ticket_id)

# POST create new ticket
@ticket_routes.route("/tickets", methods=["POST"])
def create_ticket_route():
    data = request.get_json()
    return create_ticket(data)

# PUT update ticket
@ticket_routes.route("/tickets/<ticket_id>", methods=["PUT"])
def update_ticket_route(ticket_id):
    data = request.get_json()
    return update_ticket(ticket_id, data)

# DELETE cancel ticket
@ticket_routes.route("/tickets/<ticket_id>", methods=["DELETE"])
def delete_ticket_route(ticket_id):
    return delete_ticket(ticket_id)
