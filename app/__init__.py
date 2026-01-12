from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models
    from app.routes.book import register_book_routes
    from app.routes.library import register_library_routes
    from app.routes.user import register_user_routes

    register_book_routes(app)
    register_library_routes(app)
    register_user_routes(app)

    return app
