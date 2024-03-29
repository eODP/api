from datetime import datetime

from extension import db
from models.taxon import Taxon


class TaxonCrosswalk(db.Model):
    __tablename__ = "taxa_crosswalk"

    id = db.Column(db.Integer, primary_key=True)
    taxon_id = db.Column(db.Integer, db.ForeignKey("taxa.id"))
    verbatim_name = db.Column(db.String, nullable=False)
    taxon_group = db.Column(db.String, nullable=True)
    comments = db.Column(db.String, nullable=True)
    comment = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    internal_notes = db.Column(db.String, nullable=True)
    name_comment = db.Column(db.String, nullable=True)
    eodp_id = db.Column(db.String, index=True)

    @classmethod
    def find_by_name(cls, name):
        return cls.query.filter_by(verbatim_name=name).first()

    @classmethod
    def find_by_name_and_group(cls, name, taxon_group):
        return cls.query.filter_by(verbatim_name=name, taxon_group=taxon_group).first()

    @classmethod
    def find_by_name_and_taxon(cls, crosswalk_name, taxon_name, taxon_group):
        return (
            cls.query.join(Taxon)
            .filter(Taxon.name == taxon_name)
            .filter(cls.verbatim_name == crosswalk_name)
            .filter(cls.taxon_group == taxon_group)
            .first()
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
