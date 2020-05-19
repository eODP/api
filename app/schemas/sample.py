from extension import ma
from models.sample import Sample


class SampleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Sample

    link = ma.Hyperlinks(ma.URLFor("sampleresource", id="<id>"))
    section = ma.Nested("SectionSchema", only=("link", "name"))
