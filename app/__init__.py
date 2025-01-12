from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_cors import CORS
from flask import Blueprint

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app():
    app = Flask(__name__)
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
        "RENDER_DATABASE_URI")

    # Import models here for Alembic setup
    # from app.models.ExampleModel import ExampleModel

    db.init_app(app)
    migrate.init_app(app, db)

    from app.models.card import Card
    from app.models.board import Board

    # Register Blueprints here
    # from .routes import example_bp
    # app.register_blueprint(example_bp)

    

    #  add our new cards blueprint
    from .routes.card import cards_bp
    app.register_blueprint(cards_bp)

    # # add our new board blueprint
    from .routes.board import boards_bp
    app.register_blueprint(boards_bp)

    CORS(app)
    return app
