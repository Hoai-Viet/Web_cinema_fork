from flask import Flask
from models import db
from config import Config
from routes.auth_routes import auth_routes # chú ý: import blueprint
from routes.movie_routes import movie_routes

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)

    # đăng ký blueprint
    app.register_blueprint(auth_routes, url_prefix="/auth")
    app.register_blueprint(movie_routes, url_prefix="/movie")

    @app.route("/")
    def home():
        return "Flask backend with SQLAlchemy is ready!"

    return app

if __name__ == "__main__":
    app = create_app()
    with app.app_context():
        db.create_all()   # tạo table nếu chưa có
    app.run(debug=True)
