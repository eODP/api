from extension import ma
from models.expedition import ExpeditionModel


class ExpeditionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ExpeditionModel
