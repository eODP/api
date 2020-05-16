from extension import db
from models.pagination import paginate


class SampleTaxon(db.Model):
    __tablename__ = "samples_taxa"

    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey("samples.id"))
    taxon_id = db.Column(db.Integer, db.ForeignKey("taxa.id"))
    code = db.Column(db.String)

    sample = db.relationship("Sample")
    taxon = db.relationship("Taxon")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
