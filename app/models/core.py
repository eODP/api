from extension import db
from models.pagination import paginate


class CoreModel(db.Model):
    __tablename__ = "cores"

    id = db.Column(db.Integer, primary_key=True)
    hole_id = db.Column(db.Integer, db.ForeignKey("holes.id"))
    name = db.Column(db.String, nullable=False, index=True)
    type = db.Column(db.String)
    top_depth_drilled_dsf = db.Column(db.Float)
    bottom_depth_drilled_dsf = db.Column(db.Float)
    advanced = db.Column(db.Float)
    recovered_length = db.Column(db.Float)
    curated_length = db.Column(db.Float)
    top_depth_cored_csf = db.Column(db.Float)
    bottom_depth_recovered = db.Column(db.Float)
    recovery = db.Column(db.Float)
    time_on_deck = db.Column(db.DateTime)
    sections = db.Column(db.Integer)
    label_id = db.Column(db.String)

    hole = db.relationship("HoleModel")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)
