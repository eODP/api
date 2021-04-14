import random

import factory

from extension import db
from models.core import Core
from models.expedition import Expedition
from models.hole import Hole
from models.sample import Sample
from models.section import Section
from models.site import Site
from models.taxon import Taxon


class ExpeditionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Expedition
        sqlalchemy_session = db.session

    name = f"exp {random.randint(1, 1000)}"


class SiteFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Site
        sqlalchemy_session = db.session

    name = f"site {random.randint(1, 1000)}"


class HoleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Hole
        sqlalchemy_session = db.session

    name = f"hole {random.randint(1, 10)}"


class CoreFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Core
        sqlalchemy_session = db.session

    name = f"core {random.randint(1, 100)}"


class SectionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Section
        sqlalchemy_session = db.session

    name = f"section {random.randint(1, 10)}"


class SampleFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Sample
        sqlalchemy_session = db.session

    name = f"sample {random.randint(1, 10000)}"


class TaxonFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Taxon
        sqlalchemy_session = db.session

    name = f"taxon {random.randint(1, 10000)}"
