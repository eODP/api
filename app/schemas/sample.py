from extension import ma
from models.sample import SampleModel


class SampleSchema(ma.SQLAlchemyAutoSchema):
    sites = ma.List(ma.Nested("SiteSchema", only=("name",)))

    class Meta:
        model = SampleModel
