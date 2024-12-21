from . import db
from datetime import datetime


class Issue(db.Model):
    __tablename__ = "issues"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # Location details
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    address = db.Column(db.Text, nullable=False)

    # Issue details
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(
        db.String(50), nullable=False
    )  # pothole, streetlight, garbage, etc.
    severity = db.Column(db.String(20), default="medium")  # low, medium, high

    # Media
    photo_url = db.Column(db.String(500))

    # Status tracking
    status = db.Column(
        db.String(20), default="pending"
    )  # pending, in_progress, resolved, closed
    assigned_to = db.Column(
        db.Integer, db.ForeignKey("users.id")
    )  # contractor assigned

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(
        db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    resolved_at = db.Column(db.DateTime)

    # Additional fields for tracking
    votes = db.Column(db.Integer, default=0)
    is_duplicate = db.Column(db.Boolean, default=False)
    duplicate_of = db.Column(db.Integer, db.ForeignKey("issues.id"))

    def __repr__(self):
        return f"<Issue {self.id}: {self.title}>"
