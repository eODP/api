from extension import db
from models.pagination import paginate
from models.core import Core


class Hole(db.Model):
    __tablename__ = "holes"

    id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey("sites.id"))
    name = db.Column(db.String, nullable=False, index=True)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    water_depth = db.Column(db.Float)
    penetration_dsf = db.Column(db.Float)
    cored_interval = db.Column(db.Float)
    recovered_length = db.Column(db.Float)
    recovery_percent = db.Column(db.Float)
    drilled_interval = db.Column(db.Float)
    drilled_intervals = db.Column(db.Integer)
    total_cores = db.Column(db.Integer)
    apc_cores = db.Column(db.Integer)
    hlapc_cores = db.Column(db.Integer)
    xcb_cores = db.Column(db.Integer)
    rcb_cores = db.Column(db.Integer)
    other_cores = db.Column(db.Integer)
    date_started = db.Column(db.DateTime)
    date_finished = db.Column(db.DateTime)
    time_on_hole = db.Column(db.Float)
    comments = db.Column(db.Text)
    seafloor_depth_drf = db.Column(db.Float)
    seafloor_depth_estimation_method = db.Column(db.String)
    rig_floor_to_sea_level = db.Column(db.Float)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    site = db.relationship("Site")
    cores = db.relationship("Core", lazy="dynamic")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
