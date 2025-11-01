from flask import Blueprint
from flasgger import swag_from
from controllers.combo_controllers import (
    get_all_combos,
    get_combo_by_id,
    add_combo_to_ticket,
    get_combos_in_ticket,
    remove_combo_from_ticket
)

# Tạo Blueprint
combo_routes = Blueprint("combo_routes", __name__, url_prefix="/api")


# ==================== ROUTES ====================

@combo_routes.route("/combos", methods=["GET"])
@swag_from("../swagger/combo/get_all_combos.yaml")
def route_get_all_combos():
    """Lấy danh sách tất cả combo đồ ăn"""
    return get_all_combos()


@combo_routes.route("/combos/<combo_id>", methods=["GET"])
@swag_from("../swagger/combo/get_combo_by_id.yaml")
def route_get_combo_by_id(combo_id):
    """Lấy chi tiết 1 combo theo ID"""
    return get_combo_by_id(combo_id)


@combo_routes.route("/combos/ticket", methods=["POST"])
@swag_from("../swagger/combo/add_combo_to_ticket.yaml")
def route_add_combo_to_ticket():
    """Thêm combo vào vé (kèm số lượng)"""
    return add_combo_to_ticket()


@combo_routes.route("/combos/ticket/<ticket_id>", methods=["GET"])
@swag_from("../swagger/combo/get_combos_in_ticket.yaml")
def route_get_combos_in_ticket(ticket_id):
    """Lấy danh sách combo đã chọn trong 1 vé"""
    return get_combos_in_ticket(ticket_id)


@combo_routes.route("/combos/ticket/<ticket_id>/<combo_id>", methods=["DELETE"])
@swag_from("../swagger/combo/remove_combo_from_ticket.yaml")
def route_remove_combo_from_ticket(ticket_id, combo_id):
    """Xóa 1 combo khỏi vé"""
    return remove_combo_from_ticket(ticket_id, combo_id)