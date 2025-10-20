from flask import Blueprint
from flask_jwt_extended import jwt_required
from controllers.movie_controllers import (
    get_movies,
    get_movie,
    create_movie,
    update_movie,
    delete_movie
)

movie_routes = Blueprint("movie_routes", __name__)

# 🟢 Lấy danh sách tất cả phim (chỉ user đã đăng nhập mới xem được)
@movie_routes.route("/movies", methods=["GET"])
@jwt_required()
def get_all_movies():
    return get_movies()

# 🟢 Tạo mới phim
@movie_routes.route("/movies", methods=["POST"])
@jwt_required()
def create_new_movie():
    return create_movie()

# 🟢 Lấy chi tiết phim theo ID
@movie_routes.route("/movies/<string:movie_id>", methods=["GET"])
@jwt_required()
def get_movie_detail(movie_id):
    return get_movie(movie_id)

# 🟢 Cập nhật phim
@movie_routes.route("/movies/<string:movie_id>", methods=["PUT"])
@jwt_required()
def update_movie_info(movie_id):
    return update_movie(movie_id)

# 🟢 Xóa phim
@movie_routes.route("/movies/<string:movie_id>", methods=["DELETE"])
@jwt_required()
def delete_movie_info(movie_id):
    return delete_movie(movie_id)
