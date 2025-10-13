from flask import Blueprint
from controllers.ticket_type_controllers import (
    get_all_ticket_types,
    get_ticket_type,
    create_ticket_type,
    update_ticket_type,
    delete_ticket_type
)

ticket_type_routes = Blueprint("ticket_type_routes", __name__)

# Lấy danh sách loại vé
ticket_type_routes.route("/", methods=["GET"])(get_all_ticket_types)

# Lấy chi tiết loại vé theo ID
ticket_type_routes.route("/<ticket_type_id>", methods=["GET"])(get_ticket_type)

# Thêm loại vé mới
ticket_type_routes.route("/", methods=["POST"])(create_ticket_type)

# Cập nhật loại vé
ticket_type_routes.route("/<ticket_type_id>", methods=["PUT"])(update_ticket_type)

# Xóa loại vé
ticket_type_routes.route("/<ticket_type_id>", methods=["DELETE"])(delete_ticket_type)
