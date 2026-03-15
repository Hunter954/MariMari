from app.extensions.db import db
from app.models.comment import Comment
from app.models.comment_like import CommentLike


def create_comment(user_id: int, episode_id: int, content: str):
    comment = Comment(user_id=user_id, episode_id=episode_id, content=content.strip())
    db.session.add(comment)
    db.session.commit()
    return comment


def toggle_comment_like(user_id: int, comment_id: int):
    like = CommentLike.query.filter_by(user_id=user_id, comment_id=comment_id).first()
    if like:
        db.session.delete(like)
        db.session.commit()
        return False
    like = CommentLike(user_id=user_id, comment_id=comment_id)
    db.session.add(like)
    db.session.commit()
    return True
