from flask import Blueprint
from flasgger import swag_from
from controllers.ticket_type_controllers import (
    get_all_ticket_types,
    get_ticket_type,
    create_ticket_type,
    update_ticket_type,
    delete_ticket_type
)

ticket_type_routes = Blueprint("ticket_type_routes", __name__)

