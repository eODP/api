from extension import ma
from models.expedition import ExpeditionModel


class ExpeditionSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = ExpeditionModel
