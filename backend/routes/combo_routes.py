from flask import Blueprint
from controllers.combo_controllers import (
    get_all_combos,
    get_combo_by_id,
    add_combo_to_ticket
)

combo_routes = Blueprint("combo_routes", __name__)

combo_routes.route("/combos", methods=["GET"])(get_all_combos)
combo_routes.route("/combos/<combo_id>", methods=["GET"])(get_combo_by_id)
combo_routes.route("/combos/add_to_ticket", methods=["POST"])(add_combo_to_ticket)
