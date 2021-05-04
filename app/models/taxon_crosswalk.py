from datetime import datetime

from extension import db


class TaxonCrosswalk(db.Model):
    __tablename__ = "taxa_crosswalk"

    id = db.Column(db.Integer, primary_key=True)
    taxon_id = db.Column(db.Integer, db.ForeignKey("taxa.id"))
    original_name = db.Column(db.String, nullable=False)
    taxon_group = db.Column(db.String, nullable=False)
    comments = db.Column(db.String, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    initial_comments = db.Column(db.String, nullable=True)
    processing_notes = db.Column(db.String, nullable=True)

    @classmethod
    def find_by_name(cls, name, taxon_group):
        return cls.query.filter_by(original_name=name, taxon_group=taxon_group).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
