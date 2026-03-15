from app.extensions.db import db
from app.models.notification import Notification


def create_notification(user_id: int, title: str, body: str, link: str | None = None, type_: str = 'general'):
    item = Notification(user_id=user_id, title=title, body=body, link=link, type=type_)
    db.session.add(item)
    db.session.commit()
    return item


def mark_notification_read(notification_id: int, user_id: int):
    item = Notification.query.filter_by(id=notification_id, user_id=user_id).first_or_404()
    item.is_read = True
    db.session.commit()
    return item
