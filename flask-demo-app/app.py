from flask import Flask
from flask_smorest import Api
from flask_jwt_extended import JWTManager
import os
import secrets
from db import db
import models

from resources.item import blp as ItemBlueprint
from resources.store import blp as StoreBlueprint
from resources.tags import blp as TagsBlueprint


def create_app(db_url=None):

    app = Flask(__name__)

    app.config["PROPAGATE_EXCEPTION"] = True
    app.config["API_TITLE"] = "Stores REST API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = db_url or os.getenv("DATABASE_URL", "sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    api = Api(app)

    # app.config["JWT_SECRET_KEY"] = secrets.SystemRandom().getrandbits(128)
    app.config["JWT_SECRET_KEY"] = "199147354889184238543979285757619692115"
    jwt = JWTManager(app)

    # @app.before_first_request
    # def create_tables():
    #     db.create_all()

    with app.app_context():
        db.create_all()

    api.register_blueprint(StoreBlueprint)
    api.register_blueprint(ItemBlueprint)
    api.register_blueprint(TagsBlueprint)

    return app


# http://127.0.0.1:5000/store - to be accessed this way
