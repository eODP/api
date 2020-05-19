from extension import db
from models.pagination import paginate
from models.section import Section


class Core(db.Model):
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
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    hole = db.relationship("Hole")
    sections = db.relationship(Section, lazy="dynamic")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
