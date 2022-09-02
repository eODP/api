from datetime import datetime

from extension import db


class SampleField(db.Model):
    __tablename__ = "samples_fields"

    id = db.Column(db.Integer, primary_key=True)
    sample_id = db.Column(db.Integer, db.ForeignKey("samples.id"))
    field_id = db.Column(db.Integer, db.ForeignKey("fields.id"))

    original_name = db.Column(db.String)
    value = db.Column(db.String)
    data_source_url = db.Column(db.String)
    data_source_notes = db.Column(db.Text, index=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @classmethod
    def find_by_ids(cls, sample_id, field_id, value, original_name):
        return cls.query.filter_by(
            sample_id=sample_id,
            field_id=field_id,
            value=value,
            original_name=original_name,
        ).first()

    def save(self):
        db.session.add(self)
        db.session.commit()
