from extension import ma
from models.taxon import TaxonModel


class TaxonSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = TaxonModel
