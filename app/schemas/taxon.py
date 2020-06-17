from extension import ma
from models.taxon import Taxon
from schemas.sample_taxon import SampleTaxonSchema  # noqa F401


class TaxonSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = Taxon

    link = ma.Hyperlinks(ma.URLFor("taxonresource", id="<id>"))
    samples = ma.List(ma.Nested("SampleTaxonSchema", only=("code", "sample")))
