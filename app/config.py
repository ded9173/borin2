import os
from operator import truediv
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(Path(__file__).with_name('.env'))

BASE_DIR = Path(__file__).parent.parent

def _bild_database_url():
    url = os.getenv('DATABASE_URL')
    if url:
        return url

    host = os.getenv('DATABASE_HOST', 'localhost')
    port = os.getenv('DATABASE_PORT', '5432')
    name = os.getenv('DATABASE_NAME', 'demo1')
    user = os.getenv('DATABASE_USER', 'postgres')
    password = os.getenv('DATABASE_PASSWORD', '12345')
    return f'postgres://{user}:{password}@{host}:{port}/{name}'

class Baseconfig:
    SECRET_KEY = os.getenv('SECRET_KEY', 'production-is-systrm-secret-key-change-me')
    SQLALCHEMY_MAX_OVERFLOW = int(os.getenv('SQLALCHEMY_MAX_OVERFLOW', '20'))
    SQLALCHEMY_POOL_TIMEOUT = int(os.getenv('SQLALCHEMY_POOL_TIMEOUT', '30'))
    SQLALCHEMY_POOL_RECYCLE = int(os.getenv('SQLALCHEMY_POOL_RECYCLE', '3600'))
    SQLALCHEMY_ECHO = os.getenv('SQLALCHEMY_ECHO', 'False').lower() == 'true'

class DevelopmentConfig(Baseconfig):
    DEBUG = True

class ProductionConfig(Baseconfig):
    DEBUG = False

class TestingConfig(Baseconfig):
    TESTING = True

class DevelopmentConfig(Baseconfig):
    DEBUG = True

class ProductionTestingConfig(Baseconfig):
    DEBUG = True

class TestingConfig(Baseconfig):
    Testing = True
    SQLALCHEMY_DATABASE_URI = os.getenv('TEST_DATABASE_URL', "postgres://postgres:12345@localhost/test_demo1",)

config_by_name = {
    "development": DevelopmentConfig,
    "production": ProductionConfig,
    "testing": TestingConfig,
    }

def get_config():
    env = os.getenv('ENV', 'development')
    return config_by_name.get(env, DevelopmentConfig)