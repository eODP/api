from extension import db
from models.pagination import paginate


class SiteModel(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True)
    expedition_id = db.Column(db.Integer, db.ForeignKey("expeditions.id"))
    name = db.Column(db.String, nullable=False, index=True)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    expedition = db.relationship("ExpeditionModel")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
