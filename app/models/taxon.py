from extension import db
from models.pagination import paginate


class Taxon(db.Model):
    __tablename__ = "taxa"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
