from datetime import datetime

from extension import db
from models.pagination import paginate


class SampleTaxon(db.Model):
    __tablename__ = "samples_taxa"

    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey("samples.id"))
    taxon_id = db.Column(db.Integer, db.ForeignKey("taxa.id"))
    original_taxon_id = db.Column(db.Integer, db.ForeignKey("taxa_crosswalk.id"))
    code = db.Column(db.String)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    dataset = db.Column(db.String, index=True)
    comments = db.Column(db.String, nullable=True)

    sample = db.relationship("Sample", back_populates="taxa")
    taxon = db.relationship("Taxon", back_populates="samples")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_ids(cls, sample_id, taxon_id, original_taxon_id):
        return cls.query.filter_by(
            sample_id=sample_id, taxon_id=taxon_id, original_taxon_id=original_taxon_id
        ).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
