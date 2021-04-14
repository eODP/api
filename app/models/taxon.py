from datetime import datetime

from sqlalchemy.dialects.postgresql.json import JSONB

from extension import db
from models.pagination import paginate


class Taxon(db.Model):
    __tablename__ = "taxa"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    taxon_group = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    taxon_name_above_genus = db.Column(db.String, nullable=True)
    genus_modifier = db.Column(db.String, nullable=True)
    genus_name = db.Column(db.String, nullable=True)
    subgenera_modifier = db.Column(db.String, nullable=True)
    subgenera_name = db.Column(db.String, nullable=True)
    species_modifier = db.Column(db.String, nullable=True)
    species_name = db.Column(db.String, nullable=True)
    subspecies_modifier = db.Column(db.String, nullable=True)
    subspecies_name = db.Column(db.String, nullable=True)
    non_taxa_descriptor = db.Column(db.String, nullable=True)
    pbdb_taxon_id = db.Column(db.Integer)
    pbdb_taxon_name = db.Column(db.String)
    pbdb_taxon_rank = db.Column(db.String)
    pbdb_data = db.Column(JSONB)
    pbdb_notes = db.Column(db.String)

    samples = db.relationship("SampleTaxon", back_populates="taxon")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_by_name(cls, name, taxon_group):
        return cls.query.filter_by(name=name, taxon_group=taxon_group).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
