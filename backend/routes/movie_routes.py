from flask import Blueprint, jsonify
from models import db, Movie

movie_routes = Blueprint("movie_routes", __name__)

# Lấy danh sách phim
@movie_routes.route("/movies", methods=["GET"])
def get_movies():
    movies = Movie.query.all()
    result = []
    for movie in movies:
        result.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "duration_minutes": movie.duration_minutes,
            "genre": movie.genre,
            "release_date": movie.release_date.isoformat() if movie.release_date else None,
            "poster_url": movie.poster_url
        })
    return jsonify(result)

# Lấy chi tiết phim theo id
@movie_routes.route("/movies/<movie_id>", methods=["GET"])
def get_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    result = {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "duration_minutes": movie.duration_minutes,
        "genre": movie.genre,
        "release_date": movie.release_date.isoformat() if movie.release_date else None,
        "poster_url": movie.poster_url
    }
    return jsonify(result)
