from extension import ma

from models.site import Site


class SiteSchema(ma.SQLAlchemyAutoSchema):
    expedition = ma.Nested("ExpeditionSchema", only=("name",))

    class Meta:
        model = Site
