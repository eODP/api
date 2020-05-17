import random

import factory

from extension import db
from models.expedition import Expedition


class ExpeditionFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Expedition
        sqlalchemy_session = db.session

    name = random.randint(1, 500)
