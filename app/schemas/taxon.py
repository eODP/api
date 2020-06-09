from extension import ma
from models.taxon import Taxon


class TaxonSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = Taxon

    link = ma.Hyperlinks(ma.URLFor("taxonresource", id="<id>"))
    samples = ma.List(ma.Nested("SampleSchema", only=("name", "link")))
