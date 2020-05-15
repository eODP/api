from extension import db
from models.pagination import paginate


class SectionModel(db.Model):
    __tablename__ = "sections"

    id = db.Column(db.Integer, primary_key=True)
    core_id = db.Column(db.Integer, db.ForeignKey("cores.id"))
    name = db.Column(db.String, nullable=False, index=True)
    recovered_length = db.Column(db.Float)
    curated_length = db.Column(db.Float)
    top_depth_csf_a = db.Column(db.Float)
    bottom_depth_csf_a = db.Column(db.Float)
    top_depth_csf_b = db.Column(db.Float)
    bottom_depth_csf_b = db.Column(db.Float)
    top_depth_ccsf = db.Column(db.Float)
    bottom_depth_ccsf = db.Column(db.Float)
    text_id_section = db.Column(db.String)
    text_id_archive_half = db.Column(db.String)
    text_id_working_half = db.Column(db.String)
    catwalk_samples = db.Column(db.Integer)
    section_half_samples = db.Column(db.Integer)
    comments = db.Column(db.Text)

    core = db.relationship("CoreModel")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
