from pathlib import Path
import os
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app import create_app
from app.extensions.db import db
from app.models.user import User
from app.services.auth_service import hash_password

app = create_app()

with app.app_context():
    db.create_all()
    email = os.getenv('ADMIN_EMAIL', 'admin@mariolivier.com')
    password = os.getenv('ADMIN_PASSWORD', '12345678')
    user = User.query.filter_by(email=email).first()
    if user:
        user.role = 'admin'
        user.password_hash = hash_password(password)
    else:
        user = User(name='Admin', email=email, password_hash=hash_password(password), role='admin', username='admin')
        db.session.add(user)
    db.session.commit()
    print(f'Admin pronto: {email}')
