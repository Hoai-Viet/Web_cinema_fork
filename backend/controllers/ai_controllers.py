from flask import jsonify, request
from openai import OpenAI
import numpy as np
from models import Movie  # Assuming you already have this model

client = OpenAI(api_key="YOUR_API_KEY")

# Create embedding function
def get_embedding(text: str):
    """Generate embedding vector from text using OpenAI API"""
    res = client.embeddings.create(model="text-embedding-3-small", input=text)
    return np.array(res.data[0].embedding)

# AI search endpoint logic
def ai_search_movies():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "Missing query parameter ?q=..."}), 400

    # 1. Create embedding for the user query
    query_vec = get_embedding(query)

    # 2. Get all movies from DB
    movies = Movie.query.all()
    if not movies:
        return jsonify([])

    # 3. Compute similarity with each movie description
    results = []
    for movie in movies:
        movie_vec = get_embedding(movie.description or movie.title)
        similarity = np.dot(query_vec, movie_vec) / (
            np.linalg.norm(query_vec) * np.linalg.norm(movie_vec)
        )
        results.append({
            "id": movie.id,
            "title": movie.title,
            "description": movie.description,
            "similarity": float(similarity),
        })

    # 4. Sort by similarity descending
    results.sort(key=lambda x: x["similarity"], reverse=True)
    return jsonify(results[:10])  # top 10
