
import logging
import os
from pathlib import Path

from dotenv import load_dotenv
from flask import Flask

from app.extensions import db, login_manager, migrate
from app.config import get_config


env_path = Path(__file__).parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)


def create_app(config_name=None):

    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')

    base_dir = Path(__file__).parent.parent
    app = Flask(
        __name__,
        template_folder=str(base_dir / "web"),
        static_folder=str(base_dir / "web"),
        static_url_path="/static",
    )

    # Загрузка конфигурации: читает класс из config_by_name в app/config.py.
    # Например, если FLASK_ENV=development, будет использован DevelopmentConfig.
    config_class = get_config()
    app.config.from_object(config_class)

    # Инициализация расширений Flask.
    # Важно: мы передаём app через init_app(), а не через конструктор.
    # Это позволяет создать расширения ДО создания приложения (паттерн Factory).
    if app.config.get("SQLALCHEMY_DATABASE_URI"):
        db.init_app(app)
        migrate.init_app(app, db)
        login_manager.init_app(app)
        login_manager.login_view = "web.login_page"
        login_manager.login_message = "Пожалуйста, войдите в систему"

        # Flask-Login использует этот callback для восстановления сессии.
        # При каждом запросе Flask-Login вызывает load_user(user_id), чтобы
        # подгрузить объект пользователя из БД и сохранить в сессию.
        @login_manager.user_loader
        def load_user(user_id):
            from app.models import Users
            return db.session.get(Users, int(user_id))

        # Регистрация Blueprint — это способ разделения маршрутов по модулям.
        # Каждый Blueprint отвечает за свою область (web-страницы, API авторизации, клиенты и т.д.).
        # Url_prefix="/api/..." означает, что все маршруты этого Blueprint будут
        # начинаться с этого префикса (например, /api/clients/).
        from app.blueprints import web_bp
        from app.blueprints import auth_bp
        # OOP Views (Class-Based Views)
        from app.views.customer_view import Customer_bp
        from app.views.items_views import items_db
        from app.views.specification_view import specifications_bp
        from app.views.customer_order_view import sales_orders_bp
        from app.views.production_order_view import production_orders_bp
        from app.views.admin_view import admin_bp
        from app.views.notes_view import notes_bp

        app.register_blueprint(web_bp)
        app.register_blueprint(auth_bp, url_prefix="/api/auth")
        app.register_blueprint(Customer_bp, url_prefix="/api/clients")
        app.register_blueprint(items_db, url_prefix="/api/items")
        app.register_blueprint(specifications_bp, url_prefix="/api/specifications")
        app.register_blueprint(sales_orders_bp, url_prefix="/api/sales-orders")
        app.register_blueprint(production_orders_bp, url_prefix="/api/production-orders")
        app.register_blueprint(admin_bp, url_prefix="/api/admin")
        app.register_blueprint(notes_bp, url_prefix="/api/notes")

        # Обработчики ошибок: эти функции вызываются Flask автоматически,
        # когда возникает ошибка с указанным кодом (400, 404, 500).
        # Мы возвращаем JSON вместо HTML, чтобы API был консистентным.
        @app.errorhandler(400)
        def bad_request(e):
            return {"error": "Bad Request", "message": str(e.description)}, 400

        @app.errorhandler(404)
        def not_found(e):
            return {"error": "Not Found", "message": "Ресурс не найден"}, 404

        @app.errorhandler(500)
        def internal_error(e):
            # При ошибке откатываем транзакцию, чтобы не оставить БД в несогласованном состоянии.
            db.session.rollback()
            return {
                "error": "Internal Server Error",
                "message": "Ошибка подключения к базе данных",
            }, 500

        # Проверка подключения к базе данных при запуске.
        # Если БД недоступна — логируем ошибку, но не прерываем работу приложения.
        def check_db_connection():
            """Проверка подключения к PostgreSQL."""
            try:
                with app.app_context():
                    db.engine.connect()
                    logging.info("Успешное подключение к PostgreSQL")
                    return True
            except Exception as e:
                logging.error(f"Ошибка подключения к базе данных: {e}")
                return False

        # Создание таблиц БД (для разработки).
        # Студенты: в продакшене обычно используют миграции (Alembic/Flask-Migrate),
        # а не db.create_all(). Этот код удобен для быстрого старта, но не заменяет миграции.
        with app.app_context():
            check_db_connection()
            db.create_all()

        return app

