from flask import jsonify, request
from models import db, Movie

# Lấy danh sách phim
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


# Tạo phim mới
def create_movie():
    data = request.get_json()
    if not data or "title" not in data or "duration_minutes" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    new_movie = Movie(
        title=data["title"],
        description=data.get("description"),
        duration_minutes=data["duration_minutes"],
        genre=data.get("genre"),
        release_date=data.get("release_date"),
        poster_url=data.get("poster_url")
    )
    db.session.add(new_movie)
    db.session.commit()
    return jsonify({"message": "Movie created", "id": new_movie.id}), 201


# Cập nhật phim
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    data = request.get_json()
    movie.title = data.get("title", movie.title)
    movie.description = data.get("description", movie.description)
    movie.duration_minutes = data.get("duration_minutes", movie.duration_minutes)
    movie.genre = data.get("genre", movie.genre)
    movie.release_date = data.get("release_date", movie.release_date)
    movie.poster_url = data.get("poster_url", movie.poster_url)

    db.session.commit()
    return jsonify({"message": "Movie updated", "id": movie.id})


# Xóa phim
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    db.session.delete(movie)
    db.session.commit()
    return jsonify({"message": "Movie deleted", "id": movie_id})
