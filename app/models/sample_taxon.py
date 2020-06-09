from datetime import datetime

from extension import db
from models.pagination import paginate


class SampleTaxon(db.Model):
    __tablename__ = "samples_taxa"

    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey("samples.id"))
    taxon_id = db.Column(db.Integer, db.ForeignKey("taxa.id"))
    code = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    sample = db.relationship("Sample")
    taxon = db.relationship("Taxon")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    def save(self):
        db.session.add(self)
        db.session.commit()
