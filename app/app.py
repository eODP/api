import os

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from resources.expedition import ExpeditionListResource
from resources.home import HomeResource

load_dotenv(".env", verbose=True)


def create_app():
    if os.environ.get("ENV") == "Production":
        config_str = "api.app.config.ProductionConfig"
    else:
        config_str = "config.DevelopmentConfig"

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_resources(app)

    return app


def register_resources(app):
    api = Api(app)

    api.add_resource(ExpeditionListResource, "/expeditions")
    api.add_resource(HomeResource, "/")


if __name__ == "__main__":
    app = create_app()
    app.run(port=os.environ.get("PORT"))
