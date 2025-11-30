from flask import Blueprint
from flask_jwt_extended import jwt_required
from flasgger import swag_from
from controllers.movie_controllers import (
    get_movies,
    get_movie,
    create_movie,
    update_movie,
    delete_movie
)

movie_routes = Blueprint("movie_routes", __name__)
# 7
# 🟢 Lấy danh sách tất cả phim
@movie_routes.route("/movies", methods=["GET"])
# @jwt_required()
@swag_from("../swagger/movie/get_movies.yaml", methods=["GET"])
def get_all_movies():
    return get_movies()


# 8
# 🟢 Lấy chi tiết phim theo ID
@movie_routes.route("/movies/<string:movie_id>", methods=["GET"])
# @jwt_required()
@swag_from("../swagger/movie/get_movie.yaml", methods=["GET"])
def get_movie_detail(movie_id):
    return get_movie(movie_id)
