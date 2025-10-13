from flask import jsonify, request
from models import db, Movie
from datetime import datetime

# 🟢 Lấy danh sách phim (có hỗ trợ lọc theo thể loại, quốc gia, trạng thái)
def get_movies():
    genre = request.args.get("genre")
    country = request.args.get("country")
    status = request.args.get("status")

    query = Movie.query
    if genre:
        query = query.filter_by(genre=genre)
    if country:
        query = query.filter_by(country=country)
    if status:
        query = query.filter_by(status=status)

    movies = query.all()
    result = []
    for movie in movies:
        result.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "duration_minutes": movie.duration_minutes,
            "genre": movie.genre,
            "release_date": movie.release_date.isoformat() if movie.release_date else None,
            "poster_url": movie.poster_url,
            "country": movie.country,
            "age_rating": movie.age_rating,
            "language": movie.language,
            "status": movie.status
        })
    return jsonify(result), 200


# 🟢 Lấy chi tiết phim theo ID
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
        "poster_url": movie.poster_url,
        "country": movie.country,
        "age_rating": movie.age_rating,
        "language": movie.language,
        "status": movie.status
    }
    return jsonify(result), 200


# 🟢 Tạo phim mới
def create_movie():
    data = request.get_json()
    if not data or "title" not in data or "duration_minutes" not in data:
        return jsonify({"message": "Missing required fields"}), 400

    # Kiểm tra trùng tên
    if Movie.query.filter_by(title=data["title"]).first():
        return jsonify({"message": "Movie with this title already exists"}), 400

    # Parse ngày phát hành
    release_date = None
    if data.get("release_date"):
        try:
            release_date = datetime.strptime(data["release_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date format (YYYY-MM-DD required)"}), 400

    new_movie = Movie(
        title=data["title"],
        description=data.get("description"),
        duration_minutes=data["duration_minutes"],
        genre=data.get("genre"),
        release_date=release_date,
        poster_url=data.get("poster_url"),
        country=data.get("country"),
        age_rating=data.get("age_rating"),
        language=data.get("language"),
        status=data.get("status", "Coming Soon")
    )

    db.session.add(new_movie)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500

    return jsonify({"message": "Movie created successfully", "id": new_movie.id}), 201


# 🟢 Cập nhật phim
def update_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    # Cập nhật từng trường
    movie.title = data.get("title", movie.title)
    movie.description = data.get("description", movie.description)
    movie.duration_minutes = data.get("duration_minutes", movie.duration_minutes)
    movie.genre = data.get("genre", movie.genre)
    movie.poster_url = data.get("poster_url", movie.poster_url)
    movie.country = data.get("country", movie.country)
    movie.age_rating = data.get("age_rating", movie.age_rating)
    movie.language = data.get("language", movie.language)
    movie.status = data.get("status", movie.status)

    # Parse lại release_date nếu có
    if "release_date" in data:
        try:
            movie.release_date = datetime.strptime(data["release_date"], "%Y-%m-%d").date()
        except ValueError:
            return jsonify({"message": "Invalid date format (YYYY-MM-DD required)"}), 400

    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500

    return jsonify({"message": "Movie updated successfully", "id": movie.id}), 200


# 🟢 Xóa phim
def delete_movie(movie_id):
    movie = Movie.query.get(movie_id)
    if not movie:
        return jsonify({"message": "Movie not found"}), 404

    db.session.delete(movie)
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "Database error", "error": str(e)}), 500

    return jsonify({"message": "Movie deleted successfully", "id": movie_id}), 200
