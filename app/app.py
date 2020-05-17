import os

from flask import Flask
from flask_restful import Api
from dotenv import load_dotenv

from extension import db, migrate, ma
from resources.expedition import ExpeditionListResource
from resources.home import HomeResource
from resources.site import SiteListResource

# NOTE: temporarily import models in app.py so migrations will work
from models.core import Core
from models.expedition import Expedition
from models.hole import Hole
from models.sample_taxon import SampleTaxon
from models.sample import Sample
from models.section import Section
from models.site import Site
from models.taxon import Taxon

load_dotenv(".env", verbose=True)


def create_app():
    if os.environ.get("ENV") == "Production":
        config_str = "config.ProductionConfig"
    elif os.environ.get("ENV") == "Testing":
        config_str = "config.TestingConfig"
    else:
        config_str = "config.DevelopmentConfig"

    app = Flask(__name__)
    app.config.from_object(config_str)

    register_extensions(app)
    register_resources(app)

    return app


def register_extensions(app):
    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)


def register_resources(app):
    api = Api(app)

    api.add_resource(SiteListResource, "/sites")
    api.add_resource(ExpeditionListResource, "/expeditions")
    api.add_resource(HomeResource, "/")


if __name__ == "__main__":
    app = create_app()
    app.run(port=os.environ.get("PORT"))
