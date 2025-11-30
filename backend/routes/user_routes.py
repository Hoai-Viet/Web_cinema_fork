from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from flasgger import swag_from
from controllers.user_controllers import (
    get_user_profile,
    update_user_profile,
    delete_user_account,
    change_password,
    get_user_tickets,
)

user_routes = Blueprint("user_routes", __name__)

# # ---------------------------
# # Lấy thông tin người dùng hiện tại
# # ---------------------------
# @user_routes.route("/me", methods=["GET"])
# @jwt_required()
# @swag_from("../swagger/user/get_user_profile.yaml", methods=["get"])
# def get_profile():
#     user_id = get_jwt_identity()
#     return get_user_profile(user_id)

# # ---------------------------
# # Cập nhật thông tin người dùng hiện tại
# # ---------------------------
# @user_routes.route("/me", methods=["PUT"])
# @jwt_required()
# @swag_from("../swagger/user/update_user_profile.yaml", methods=["put"])
# def update_profile():
#     user_id = get_jwt_identity()
#     data = request.get_json()
#     return update_user_profile(user_id, data)

# # ---------------------------
# # Xóa tài khoản người dùng hiện tại
# # ---------------------------
# @user_routes.route("/me/delete", methods=["DELETE"])
# @jwt_required()
# @swag_from("../swagger/user/delete_user_account.yaml", methods=["delete"])
# def delete_account():
#     user_id = get_jwt_identity()
#     return delete_user_account(user_id)


# @user_routes.route("/me/change-password", methods=["PUT"])
# @jwt_required()
# # @swag_from("../swagger/user/change_password.yaml", methods=["post"])
# def change_user_password():
#     user_id = get_jwt_identity()
#     return change_password(user_id)

# @user_routes.route("/me/tickets", methods=["GET"])
# @jwt_required()
# # @swag_from("../swagger/user/get_user_tickets.yaml", methods=["get"])
# def get_user_tickets_route():
#     user_id = get_jwt_identity()
#     return get_user_tickets(user_id)