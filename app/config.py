import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
INSTANCE_DIR = BASE_DIR / 'instance'
INSTANCE_DIR.mkdir(exist_ok=True)


class Config:
    APP_NAME = os.getenv('APP_NAME', 'Mari Olivier')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', f"sqlite:///{INSTANCE_DIR / 'app.db'}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SESSION_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_HTTPONLY = True
    UPLOAD_ROOT = os.getenv('UPLOAD_ROOT', str(BASE_DIR / 'storage'))
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024 * 1024
    MAIL_FROM = os.getenv('MAIL_FROM', 'no-reply@example.com')
