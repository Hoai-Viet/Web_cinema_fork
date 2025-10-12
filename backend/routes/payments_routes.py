from flask import Blueprint
from controllers.payments_controllers import (
    create_payment,
    get_payment_by_ticket,
    update_payment_status
)

payment_routes = Blueprint("payment_routes", __name__)

# POST /api/payments → user tạo thanh toán mới
payment_routes.route("/api/payments", methods=["POST"])(create_payment)

# GET /api/payments/ticket/<ticket_id> → xem thanh toán theo vé
payment_routes.route("/api/payments/ticket/<string:ticket_id>", methods=["GET"])(get_payment_by_ticket)

# PUT /api/payments/<payment_id> → cập nhật trạng thái
payment_routes.route("/api/payments/<string:payment_id>", methods=["PUT"])(update_payment_status)
