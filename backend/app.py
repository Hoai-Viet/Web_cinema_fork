from flask import Flask
from flask_cors import CORS  
from flask_jwt_extended import JWTManager
from models import db
from config import Config

# Import routes
from routes.auth_routes import auth_routes
from routes.movie_routes import movie_routes
from routes.room_routes import room_routes
from routes.seat_routes import seat_routes
from routes.tickets_route import ticket_routes  
from routes.showtime_routes import showtime_routes
from routes.cinema_routes import cinema_routes
from routes.payments_routes import payment_routes
from routes.combo_routes import combo_routes    
from routes.ticket_type_routes import ticket_type_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # ---------------------------
    # 🔐 JWT CONFIG
    # ---------------------------
    app.config["JWT_SECRET_KEY"] = "super-secret-key" 
    app.config["JWT_ACCESS_TOKEN_EXPIRES"] = 3600      
    app.config["JWT_REFRESH_TOKEN_EXPIRES"] = 86400

    # Initialize extensions
    db.init_app(app)
    jwt = JWTManager(app)
    CORS(app, origins=["http://localhost:5703"])  

    # ---------------------------
    # 🔗 Register blueprints
    # ---------------------------
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(movie_routes, url_prefix="/movie")
    app.register_blueprint(room_routes, url_prefix="/room") 
    app.register_blueprint(seat_routes, url_prefix="/seat") 
    app.register_blueprint(ticket_routes, url_prefix="/ticket")
    app.register_blueprint(ticket_type_routes, url_prefix="/ticket-type")
    app.register_blueprint(showtime_routes, url_prefix="/showtime") 
    app.register_blueprint(cinema_routes, url_prefix="/cinema") 
    app.register_blueprint(payment_routes, url_prefix="/payment")
    app.register_blueprint(combo_routes, url_prefix="/combo")
    
    @app.route("/")
    def home():
        return "🎬 Flask backend with SQLAlchemy + JWT is ready!"

    return app


if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()  
    app.run(debug=True)
