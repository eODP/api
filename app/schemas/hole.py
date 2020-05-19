from extension import ma
from models.hole import Hole


class HoleSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Hole

    link = ma.Hyperlinks(ma.URLFor("holeresource", id="<id>"))
    site = ma.Nested("SiteSchema", only=("name", "link"))
    cores = ma.List(ma.Nested("CoreSchema", only=("link", "name")))
