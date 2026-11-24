"""Flask application factory."""
import logging
from pathlib import Path
from flask import Flask, jsonify
from sqlalchemy import text
from app.config import get_config
from app.extensions import db, login_manager, migrate


def create_app(config_name=None, config_overrides=None):
    base_dir = Path(__file__).resolve().parent.parent
    app = Flask(__name__, template_folder=str(base_dir / "web"), static_folder=str(base_dir / "web"), static_url_path="/static")
    app.config.from_object(get_config(config_name))
    if config_overrides:
        app.config.update(config_overrides)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = "web.login_page"
    login_manager.login_message = "Пожалуйста, войдите в систему"

    @login_manager.user_loader
    def load_user(user_id):
        from app.models import Users
        try:
            return db.session.get(Users, int(user_id))
        except (TypeError, ValueError):
            return None

    from app.blueprints.auth import auth_bp
    from app.blueprints.web import web_bp
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(web_bp)

    @app.get("/health")
    def health():
        try:
            db.session.execute(text("SELECT 1"))
            return jsonify(status="ok", database="ok")
        except Exception:
            logging.exception("Database health check failed")
            return jsonify(status="error", database="unavailable"), 503

    @app.errorhandler(404)
    def not_found(_error):
        return jsonify(error="Not Found", message="Ресурс не найден"), 404

    @app.errorhandler(500)
    def internal_error(_error):
        db.session.rollback()
        logging.exception("Unhandled application error")
        return jsonify(error="Internal Server Error"), 500

    with app.app_context():
        # Create tables only for local SQLite development; production schema is managed by migrations.
        if app.config.get("SQLALCHEMY_DATABASE_URI", "").startswith("sqlite:"):
            db.create_all()

    return app
