from datetime import datetime

from extension import db
from models.taxon import Taxon


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

    # db.session.query(Taxon, cls).filter(Taxon.name == 'Neogloboquadrina acostaensis (dextral)').filter(cls.original_name==name).filter(cls.taxon_group==taxon_group)

    # cls.query(Taxon).filter_by(Taxon.name == 'Neogloboquadrina acostaensis (dextral)')

    # .filter(cls.original_name==name).filter(cls.taxon_group==taxon_group)

    #     # taxa = db.relationship(Taxon, lazy="dynamic")
    #  cls.query.join(Taxon).filter(Taxon.name == 'Neogloboquadrina acostaensis (dextral)').filter(cls.original_name==name).filter(cls.taxon_group==taxon_group)

    #  filter_by(original_name=name, taxon_group=taxon_group).join(Taxon).filter_by(Taxon.taxon_group='planktic_forams').first()

    # cls.query(Taxon)
    # Session.query(
    #          Taxon, Document, DocumentPermissions,
    #     ).filter(
    #          User.email == Document.author,
    #     ).filter(
    #          Document.name == DocumentPermissions.document,
    #     ).filter(
    #         User.email == 'someemail',
    #     ).all()

    # cls.query.join(Taxon).filter_by(cls.original_name=name, cls.taxon_group=taxon_group).first()
    @classmethod
    def find_by_name(cls, name, taxon_group):
        return cls.query.filter_by(original_name=name, taxon_group=taxon_group).first()

    @classmethod
    def find_by_name_and_taxon(cls, crosswalk_name, taxon_name, taxon_group):
        return (
            cls.query.join(Taxon)
            .filter(Taxon.name == taxon_name)
            .filter(cls.original_name == crosswalk_name)
            .filter(cls.taxon_group == taxon_group)
            .first()
        )

    def save(self):
        db.session.add(self)
        db.session.commit()
