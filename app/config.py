"""Application configuration loaded from environment variables."""
import os
from pathlib import Path
from urllib.parse import quote_plus

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def database_url():
    url = os.getenv("DATABASE_URL")
    if url:
        if url.startswith("postgres://"):
            return url.replace("postgres://", "postgresql+psycopg://", 1)
        return url
    if os.getenv("FLASK_ENV") == "production":
        raise RuntimeError("DATABASE_URL must be set in production")
    # SQLite makes local development and automated checks possible without PostgreSQL.
    return f"sqlite:///{BASE_DIR / 'borin-dev.sqlite3'}"


class BaseConfig:
    SECRET_KEY = os.getenv("SECRET_KEY")
    if not SECRET_KEY or len(SECRET_KEY) < 32:
        if os.getenv("FLASK_ENV") == "production":
            raise RuntimeError("Set a random SECRET_KEY (at least 32 characters)")
        SECRET_KEY = os.getenv("SECRET_KEY", "local-only-change-this-development-key")
    SQLALCHEMY_DATABASE_URI = database_url()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ECHO = os.getenv("SQLALCHEMY_ECHO", "false").lower() == "true"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_SECURE = os.getenv("FLASK_ENV") == "production"


class DevelopmentConfig(BaseConfig):
    DEBUG = False


class ProductionConfig(BaseConfig):
    DEBUG = False


class TestingConfig(BaseConfig):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL", "sqlite:///:memory:")


config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
}


def get_config(name=None):
    name = name or os.getenv("FLASK_ENV", "development")
    return config_by_name.get(name, DevelopmentConfig)
