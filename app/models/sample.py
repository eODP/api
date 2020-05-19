from extension import db
from models.pagination import paginate
from sqlalchemy.dialects.postgresql.json import JSONB


class Sample(db.Model):
    __tablename__ = "samples"

    id = db.Column(db.Integer, primary_key=True)
    section_id = db.Column(db.Integer, db.ForeignKey("sections.id"))
    name = db.Column(db.String, nullable=False, index=True)
    aw = db.Column(db.String)
    original_sample_id = db.Column(db.Integer)
    top = db.Column(db.Float)
    bottom = db.Column(db.Float)
    top_depth = db.Column(db.Float)
    bottom_depth = db.Column(db.Float)
    principal_lithology_prefix = db.Column(db.String)
    principal_lithology_name = db.Column(db.String)
    principal_lithology_suffix = db.Column(db.String)
    minor_lithology_prefix = db.Column(db.String)
    minor_lithology_name = db.Column(db.String)
    minor_lithology_suffix = db.Column(db.String)
    sampled_date = db.Column(db.DateTime)
    raw_data = db.Column(JSONB)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    section = db.relationship("Section")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
