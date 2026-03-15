from app.extensions.db import db
from app.models.lead_interest import LeadInterest


def register_interest(user_id: int, bonus_item_id: int, message: str):
    lead = LeadInterest(user_id=user_id, bonus_item_id=bonus_item_id, message=message.strip())
    db.session.add(lead)
    db.session.commit()
    return lead
