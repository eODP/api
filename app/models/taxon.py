from datetime import datetime

from extension import db
from models.pagination import paginate


class Taxon(db.Model):
    __tablename__ = "taxa"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    verbatim_name = db.Column(db.String)
    taxon_group = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    def save(self):
        db.session.add(self)
        db.session.commit()
