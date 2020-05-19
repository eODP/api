from extension import ma
from models.expedition import Expedition


class ExpeditionSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Expedition

    link = ma.Hyperlinks(ma.URLFor("expeditionresource", id="<id>"))
    sites = ma.List(ma.Nested("SiteSchema", only=("link", "name")))
