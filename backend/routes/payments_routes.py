from flask import Blueprint
from flasgger.utils import swag_from
from controllers.payments_controllers import (
    create_payment,
    # update_payment_status,
    preview_payment,
    # get_payments_by_user,
    get_payment_detail
)

payment_routes = Blueprint("payment_routes", __name__)
# 15
# 🟢 Tạo thanh toán mới
@payment_routes.route("", methods=["POST"])
@swag_from("../swagger/payment/create_payment.yaml")
def route_create_payment():
    return create_payment()
