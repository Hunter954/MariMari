from datetime import datetime
from app.extensions.db import db


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    season_id = db.Column(db.Integer, db.ForeignKey('season.id'), nullable=False)
    title = db.Column(db.String(140), nullable=False)
    slug = db.Column(db.String(160), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    video_url = db.Column(db.String(255))
    thumb_url = db.Column(db.String(255))
    duration_seconds = db.Column(db.Integer, default=0)
    sort_order = db.Column(db.Integer, default=0)
    status = db.Column(db.String(20), default='draft')
    release_date = db.Column(db.DateTime)
    is_featured = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    season = db.relationship('Season', back_populates='episodes')
    comments = db.relationship('Comment', back_populates='episode', cascade='all, delete-orphan')
