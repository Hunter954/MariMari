from datetime import datetime
from app.extensions.db import db


class LeadInterest(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    bonus_item_id = db.Column(db.Integer, db.ForeignKey('bonus_item.id'), nullable=False)
    message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
