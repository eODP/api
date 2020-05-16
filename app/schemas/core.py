from extension import ma
from models.core import Core


class CoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Core
