from datetime import datetime

from extension import db


class AbundanceCrosswalk(db.Model):
    __tablename__ = "abundance_crosswalk"

    id = db.Column(db.Integer, primary_key=True)
    original_abundance = db.Column(db.String, nullable=False)
    normalized_abundance = db.Column(db.String, nullable=True)
    expedition = db.Column(db.String, nullable=False)
    taxon_group = db.Column(db.String, nullable=True)
    notes = db.Column(db.String, nullable=True)
    definition = db.Column(db.String, nullable=True)
    type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
