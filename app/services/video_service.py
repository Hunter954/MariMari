from datetime import datetime
from app.extensions.db import db
from app.models.watch_progress import WatchProgress
from app.models.video_like import VideoLike


def save_progress(user_id: int, episode_id: int, progress_seconds: int, duration_seconds: int):
    record = WatchProgress.query.filter_by(user_id=user_id, episode_id=episode_id).first()
    if not record:
        record = WatchProgress(user_id=user_id, episode_id=episode_id)
        db.session.add(record)
    record.progress_seconds = max(progress_seconds, 0)
    record.completed = duration_seconds > 0 and progress_seconds >= int(duration_seconds * 0.95)
    record.last_watched_at = datetime.utcnow()
    db.session.commit()
    return record


def toggle_video_like(user_id: int, episode_id: int):
    like = VideoLike.query.filter_by(user_id=user_id, episode_id=episode_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return False
    like = VideoLike(user_id=user_id, episode_id=episode_id)
    db.session.add(like)
    db.session.commit()
    return True
