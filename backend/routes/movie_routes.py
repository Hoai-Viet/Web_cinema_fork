from flask import Blueprint
from controllers.movie_controllers import (
    get_movies,
    get_movie,
    create_movie,
    update_movie,
    delete_movie
)

movie_routes = Blueprint("movie_routes", __name__)

# Danh sách và tạo mới phim
movie_routes.route("/movies", methods=["GET"])(get_movies)
movie_routes.route("/movies", methods=["POST"])(create_movie)

# Các route chi tiết phim
movie_routes.route("/movies/<string:movie_id>", methods=["GET"])(get_movie)
movie_routes.route("/movies/<string:movie_id>", methods=["PUT"])(update_movie)
movie_routes.route("/movies/<string:movie_id>", methods=["DELETE"])(delete_movie)
