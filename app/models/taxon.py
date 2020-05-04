from extension import db
from models.pagination import paginate


class TaxonModel(db.Model):
    __tablename__ = "taxa"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
