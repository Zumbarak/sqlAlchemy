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
    from app.routes.book import bp as book_bp
    from app.routes.library import bp as library_bp
    from app.routes.user import bp as user_bp

    app.register_blueprint(book_bp)
    app.register_blueprint(library_bp)
    app.register_blueprint(user_bp)

    return app
