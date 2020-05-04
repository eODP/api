from extension import ma

from models.site import SiteModel


class SiteSchema(ma.SQLAlchemyAutoSchema):
    expedition = ma.Nested("ExpeditionSchema", only=("name",))

    class Meta:
        model = SiteModel
