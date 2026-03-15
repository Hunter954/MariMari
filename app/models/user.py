from datetime import datetime
from flask_login import UserMixin
from app.extensions.db import db
from app.extensions.login_manager import login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.String(255))
    phone = db.Column(db.String(30))
    birth_date = db.Column(db.Date)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    username = db.Column(db.String(80), unique=True)
    role = db.Column(db.String(20), default='viewer', nullable=False)
    subscription_status = db.Column(db.String(20), default='trial', nullable=False)
    is_active_user = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    comments = db.relationship('Comment', back_populates='user', lazy=True)
    notifications = db.relationship('Notification', back_populates='user', lazy=True)

    def get_id(self):
        return str(self.id)

    @property
    def is_active(self):
        return self.is_active_user


@login_manager.user_loader

def load_user(user_id):
    return User.query.get(int(user_id))
