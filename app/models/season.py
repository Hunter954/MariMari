from datetime import datetime
from app.extensions.db import db


class Season(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120), nullable=False)
    slug = db.Column(db.String(140), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    cover_image = db.Column(db.String(255))
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='draft')
    is_current = db.Column(db.Boolean, default=False)
    release_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    episodes = db.relationship('Episode', back_populates='season', cascade='all, delete-orphan', order_by='Episode.sort_order')
