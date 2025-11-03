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

# ---------------------------
# Lấy danh sách loại vé
# ---------------------------
@ticket_type_routes.route("/ticket-types", methods=["GET"])
@swag_from("../swagger/ticket_type/get_all_ticket_types.yaml", methods=["get"])
def route_get_all_ticket_types():
    return get_all_ticket_types()


# ---------------------------
# Lấy chi tiết loại vé theo ID
# ---------------------------
@ticket_type_routes.route("/ticket-types/<ticket_type_id>", methods=["GET"])
@swag_from("../swagger/ticket_type/get_ticket_type.yaml", methods=["get"])
def route_get_ticket_type(ticket_type_id):
    return get_ticket_type(ticket_type_id)


# ---------------------------
# Thêm loại vé mới
# ---------------------------
@ticket_type_routes.route("/ticket-types", methods=["POST"])
@swag_from("../swagger/ticket_type/create_ticket_type.yaml", methods=["post"])
def route_create_ticket_type():
    return create_ticket_type()


# ---------------------------
# Cập nhật loại vé
# ---------------------------
@ticket_type_routes.route("/ticket-types/<ticket_type_id>", methods=["PUT"])
@swag_from("../swagger/ticket_type/update_ticket_type.yaml", methods=["put"])
def route_update_ticket_type(ticket_type_id):
    return update_ticket_type(ticket_type_id)


# ---------------------------
# Xóa loại vé
# ---------------------------
@ticket_type_routes.route("/ticket-types/<ticket_type_id>", methods=["DELETE"])
@swag_from("../swagger/ticket_type/delete_ticket_type.yaml", methods=["delete"])
def route_delete_ticket_type(ticket_type_id):
    return delete_ticket_type(ticket_type_id)
