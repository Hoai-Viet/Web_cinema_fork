from flask import Flask
from models import db
from config import Config
from routes.auth_routes import auth_routes
from routes.movie_routes import movie_routes
from routes.room_routes import room_routes
from routes.seat_routes import seat_routes
from routes.tickets_route import ticket_routes  
from routes.showtime_routes import showtime_routes
from routes.cinema_routes import cinema_routes
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # đăng ký blueprint
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(movie_routes, url_prefix="/movie")
    app.register_blueprint(room_routes, url_prefix="/room") 
    app.register_blueprint(seat_routes, url_prefix="/seat") 
    app.register_blueprint(ticket_routes, url_prefix="/ticket")
    app.register_blueprint(showtime_routes, url_prefix="/showtime") 
    app.register_blueprint(cinema_routes, url_prefix="/cinema") 
    
    @app.route("/")
    def home():
        return "Flask backend with SQLAlchemy is ready!"

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()   # tạo table nếu chưa có
    app.run(debug=True)
