from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from controllers.user_controllers import get_user_profile, update_user_profile, delete_user_account

user_routes = Blueprint("user_routes", __name__)

@user_routes.route("/me", methods=["GET"])
@jwt_required()
def get_profile():
    user_id = get_jwt_identity()
    return get_user_profile(user_id)

@user_routes.route("/me", methods=["PUT"])
@jwt_required()
def update_profile():
    user_id = get_jwt_identity()
    data = request.get_json()
    return update_user_profile(user_id, data)

@user_routes.route("/me", methods=["DELETE"])
@jwt_required()
def delete_account():
    user_id = get_jwt_identity()
    return delete_user_account(user_id)
