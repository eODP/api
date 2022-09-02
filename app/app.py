import os

from flask import Flask, render_template
from flask_restful import Api

from extension import db, migrate, ma
from resources.api_home import ApiHomeResource
from resources.expedition import ExpeditionListResource, ExpeditionResource
from resources.site import SiteListResource, SiteResource
from resources.hole import HoleListResource, HoleResource
from resources.core import CoreListResource, CoreResource
from resources.section import SectionListResource, SectionResource
from resources.sample import SampleListResource, SampleResource
from resources.taxon import TaxonListResource, TaxonResource

# NOTE: import models in app.py so migrations will work
from models.taxon_crosswalk import TaxonCrosswalk  # noqa: F401
from models.field import Field  # noqa: F401
from models.sample_field import SampleField  # noqa: F401


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
    api = Api(app, prefix="/api")

    api.add_resource(ApiHomeResource, "/")
    api.add_resource(ExpeditionListResource, "/expeditions")
    api.add_resource(ExpeditionResource, "/expeditions/<int:id>")
    api.add_resource(SiteListResource, "/sites")
    api.add_resource(SiteResource, "/sites/<int:id>")
    api.add_resource(HoleListResource, "/holes")
    api.add_resource(HoleResource, "/holes/<int:id>")
    api.add_resource(CoreListResource, "/cores")
    api.add_resource(CoreResource, "/cores/<int:id>")
    api.add_resource(SectionListResource, "/sections")
    api.add_resource(SectionResource, "/sections/<int:id>")
    api.add_resource(SampleListResource, "/samples")
    api.add_resource(SampleResource, "/samples/<int:id>")
    api.add_resource(TaxonListResource, "/taxa")
    api.add_resource(TaxonResource, "/taxa/<int:id>")

    @app.route("/")
    def home():
        return render_template("home.html")


if __name__ == "__main__":
    app = create_app()
    app.run(port=os.environ.get("PORT"))
