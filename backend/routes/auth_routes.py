from flask import Blueprint, request
from controllers.auth_controllers import (
    signup_user,
    login_user,
    logout_user,
    forgot_password
)

auth_routes = Blueprint("auth_routes", __name__)

@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    return signup_user(data)

@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)

@auth_routes.route("/logout", methods=["POST"])
def logout():
    return logout_user()

@auth_routes.route("/forgot-password", methods=["POST"])
def forgot():
    data = request.get_json()
    return forgot_password(data)
