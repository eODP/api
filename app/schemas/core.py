from extension import ma
from models.core import CoreModel


class CoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = CoreModel
