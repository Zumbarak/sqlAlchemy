from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from app.config import Config

db = SQLAlchemy()
migrate = Migrate()
app = Flask(__name__)

def create_app():
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from app import models, views
    return app
