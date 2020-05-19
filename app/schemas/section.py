from extension import ma
from models.section import Section


class SectionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Section

    link = ma.Hyperlinks(ma.URLFor("sectionresource", id="<id>"))
    core = ma.Nested("CoreSchema", only=("name", "link"))
    samples = ma.List(ma.Nested("SampleSchema", only=("name", "link")))
