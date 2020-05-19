from extension import ma
from models.core import Core


class CoreSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Core

    link = ma.Hyperlinks(ma.URLFor("coreresource", id="<id>"))
    hole = ma.Nested("HoleSchema", only=("name", "link"))
    sections = ma.List(ma.Nested("SectionSchema", only=("link", "name")))
