from blueprintapp.app import db
from datetime import datetime, timezone


class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String, nullable=False)
    threshold = db.Column(db.Float, nullable=False)
    # active False indicates alert has already been triggered
    active = db.Column(db.Boolean, default=True)
    # triggered_at is timestamp when alert was triggered
    triggered_at = db.Column(db.DateTime, nullable=True)
    # Use UTC timestamp on creation
    created_at = db.Column(
        db.DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    def __repr__(self):
        return f"{self.id}, {self.email}, {self.threshold}, {self.active}, {self.triggered_at}, {self.created_at}"
