from extension import db


class ExpeditionModel(db.Model):
    __tablename__ = "expeditions"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, index=True)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text)
    workbook_tab_name = db.Column(db.String)

    @classmethod
    def find_all(cls):
        return cls.query.all()
