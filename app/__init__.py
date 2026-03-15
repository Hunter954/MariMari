from flask import Flask
from app.config import Config
from app.extensions.db import db
from app.extensions.migrate import migrate
from app.extensions.login_manager import login_manager
from app.extensions.bcrypt import bcrypt


def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    from app.routes.auth.routes import auth_bp
    from app.routes.platform.routes import platform_bp
    from app.routes.admin.routes import admin_bp
    from app.routes.api.routes import api_bp
    from app.utils.storage import ensure_storage_dirs

    app.register_blueprint(auth_bp)
    app.register_blueprint(platform_bp)
    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(api_bp, url_prefix='/api')

    ensure_storage_dirs(app.config['UPLOAD_ROOT'])

    @app.context_processor
    def inject_globals():
        return {
            'app_name': app.config['APP_NAME'],
        }

    return app
