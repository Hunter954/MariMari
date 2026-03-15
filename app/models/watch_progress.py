from datetime import datetime
from app.extensions.db import db


class WatchProgress(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False, index=True)
    episode_id = db.Column(db.Integer, db.ForeignKey('episode.id'), nullable=False, index=True)
    progress_seconds = db.Column(db.Integer, default=0)
    completed = db.Column(db.Boolean, default=False)
    last_watched_at = db.Column(db.DateTime, default=datetime.utcnow)

    __table_args__ = (db.UniqueConstraint('user_id', 'episode_id', name='uq_progress_user_episode'),)
