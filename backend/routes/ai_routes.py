from flask import Blueprint
from flasgger.utils import swag_from
from controllers.ai_controllers import ai_search_movies

ai_routes = Blueprint("ai_routes", __name__)

@ai_routes.route("/ai/search", methods=["GET"])
@swag_from("../swagger/ai/ai_search.yaml")
def route_ai_search_movies():
    return ai_search_movies()
