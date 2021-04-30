from datetime import datetime

from extension import db
from models.pagination import paginate
from models.site import Site


class Expedition(db.Model):
    __tablename__ = "expeditions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, index=True)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)
    workbook_tab_name = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dataset = db.Column(db.String, index=True)

    sites = db.relationship(Site, lazy="dynamic")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(name=name).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
