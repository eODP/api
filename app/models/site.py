from extension import db
from models.pagination import paginate
from models.hole import Hole


class Site(db.Model):
    __tablename__ = "sites"

    id = db.Column(db.Integer, primary_key=True)
    expedition_id = db.Column(db.Integer, db.ForeignKey("expeditions.id"))
    name = db.Column(db.String, nullable=False, index=True)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)

    expedition = db.relationship("Expedition")
    holes = db.relationship("Hole", lazy="dynamic")

    @classmethod
    def find_all(cls, page):
        return paginate(cls.query.order_by("name"), page)

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
