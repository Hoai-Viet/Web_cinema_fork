from flask import Blueprint
from flasgger.utils import swag_from
from controllers.payments_controllers import (
    create_payment,
    get_payment_by_ticket,
    update_payment_status,
    preview_payment,
    get_payments_by_user,
    get_payment_detail
)

payment_routes = Blueprint("payment_routes", __name__)

# 🟢 Tạo thanh toán mới
@payment_routes.route("/api/payments", methods=["POST"])
@swag_from("../swagger/payment/create_payment.yaml")
def route_create_payment():
    return create_payment()

# 🟢 Xem thanh toán theo ticket_id
@payment_routes.route("/api/payments/ticket/<string:ticket_id>", methods=["GET"])
@swag_from("../swagger/payment/get_payment_by_ticket.yaml")
def route_get_payment_by_ticket(ticket_id):
    return get_payment_by_ticket(ticket_id)

# 🟢 Cập nhật trạng thái thanh toán
@payment_routes.route("/api/payments/<string:payment_id>", methods=["PUT"])
@swag_from("../swagger/payment/update_payment_status.yaml")
def route_update_payment_status(payment_id):
    return update_payment_status(payment_id)

@payment_routes.route("/api/payments/preview", methods=["POST"])    
# @swag_from("../swagger/payment/preview_payment.yaml")
def route_preview_payment():
    return preview_payment()

@payment_routes.route("/api/payments/user/<string:user_id>", methods=["GET"])
# @swag_from("../swagger/payment/get_payments_by_user.yaml")
def route_get_payments_by_user(user_id):
    return get_payments_by_user(user_id)

@payment_routes.route("/api/payments/detail/<string:payment_id>", methods=["GET"])
# @swag_from("../swagger/payment/get_payment_detail.yaml")
def route_get_payment_detail(payment_id):
    return get_payment_detail(payment_id)