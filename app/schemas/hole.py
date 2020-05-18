from extension import ma
from models.hole import Hole


class HoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hole
