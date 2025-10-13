from flask import Blueprint, request
from controllers.auth_controllers import (
    signup_user,
    login_user,
    logout_user,
    forgot_password,
    refresh_token
)
from flask_jwt_extended import jwt_required

auth_routes = Blueprint("auth_routes", __name__)

# -----------------------------
# Đăng ký tài khoản
# -----------------------------
@auth_routes.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    return signup_user(data)


# -----------------------------
# Đăng nhập
# -----------------------------
@auth_routes.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    return login_user(data)


# -----------------------------
# Đăng xuất
# -----------------------------
@auth_routes.route("/logout", methods=["POST"])
@jwt_required()  # 🔐 chỉ user đã login (có token) mới được logout
def logout():
    return logout_user()


# -----------------------------
# Quên mật khẩu
# -----------------------------
@auth_routes.route("/forgot-password", methods=["POST"])
def forgot():
    data = request.get_json()
    return forgot_password(data)


# -----------------------------
# Làm mới token (refresh)
# -----------------------------
@auth_routes.route("/refresh", methods=["POST"])
@jwt_required(refresh=True)  # 🔐 chỉ được gọi bằng refresh token
def refresh():
    return refresh_token()
