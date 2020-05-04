from extension import ma
from models.section import SectionModel


class SectionSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = SectionModel
