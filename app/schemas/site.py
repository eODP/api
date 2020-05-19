from extension import ma

from models.site import Site


class SiteSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = Site

    link = ma.Hyperlinks(ma.URLFor("siteresource", id="<id>"))
    expedition = ma.Nested("ExpeditionSchema", only=("name", "link"))
    holes = ma.List(ma.Nested("HoleSchema", only=("link", "name")))
