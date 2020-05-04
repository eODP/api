from extension import ma
from models.hole import HoleModel


class HoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = HoleModel
