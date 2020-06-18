from extension import ma
from models.sample_taxon import SampleTaxon


class SampleTaxonSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = SampleTaxon
        include_fk = True

    taxon = ma.Nested("TaxonSchema", only=("name", "link"))
    sample = ma.Nested("SampleSchema", only=("name", "link"))
