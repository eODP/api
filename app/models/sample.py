from datetime import datetime

from sqlalchemy.dialects.postgresql.json import JSONB

from extension import db
from models.pagination import paginate
from models.taxon import Taxon  # noqa F401
from models.sample_taxon import SampleTaxon  # noqa F401


class Sample(db.Model):
    __tablename__ = "samples"

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    name = db.Column(db.String, index=True)
    original_sample_id = db.Column(db.Integer)
    top = db.Column(db.Float, index=True)
    bottom = db.Column(db.Float, index=True)
    top_depth = db.Column(db.Float, index=True)
    bottom_depth = db.Column(db.Float, index=True)
    principal_lithology_prefix = db.Column(db.String, index=True)
    principal_lithology_name = db.Column(db.String, index=True)
    principal_lithology_suffix = db.Column(db.String, index=True)
    minor_lithology_prefix = db.Column(db.String, index=True)
    minor_lithology_name = db.Column(db.String, index=True)
    minor_lithology_suffix = db.Column(db.String, index=True)
    sampled_date = db.Column(db.DateTime)
    raw_data = db.Column(JSONB)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text, index=True)
    data_source_type = db.Column(db.String)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    section = db.relationship("Section")
    taxa = db.relationship("SampleTaxon", back_populates="sample")

    @classmethod
    def find_all(cls, page, data_source_type):
        query = cls.query.order_by("name")
        if data_source_type == "lithology":
            query = query.filter_by(data_source_type="lithology csv")
        elif data_source_type == "micropal":
            query = query.filter_by(data_source_type="micropal csv")

        return paginate(query, page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
