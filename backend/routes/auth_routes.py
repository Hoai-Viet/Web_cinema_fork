from flask import Blueprint, request
from controllers.auth_controllers import (
    signup_user,
    login_user,
    logout_user,
    forgot_password,
    refresh_token
)
from flask_jwt_extended import jwt_required
from flasgger import swag_from
import os

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/signup", methods=["POST"])
@swag_from("../swagger/auth_sign_up.yaml")
def signup():
    data = request.get_json()
    return signup_user(data)

@auth_routes.route("/login", methods=["POST"])
# @swag_from("../swagger/auth_login.yaml")
def login():
    data = request.get_json()
    return login_user(data)

@auth_routes.route("/forgot-password", methods=["POST"])
# @swag_from("../swagger/auth_forgot_password.yaml")
def forgot():
    data = request.get_json()
    return forgot_password(data)

@auth_routes.route("/logout", methods=["POST"])
@jwt_required()
# @swag_from("../swagger/auth_logout.yaml")
def logout():
    return logout_user()

@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)
# @swag_from("../swagger/auth_refresh.yaml")
def refresh():
    return refresh_token()

