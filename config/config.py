import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "VerySecretKey")
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class DevelopmentConfig(Config):
    DEBUG = True
    # Use SQLite by default, allow override via env
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///alerts_dev.db")


class ProductionConfig(Config):
    DEBUG = False
    # Use SQLite by default, allow override via env (e.g. Postgres on server)
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL", "sqlite:///alerts_prod.db")


class TestingConfig(Config):
    TESTING = True
    # Prefer TEST_DATABASE_URL (CI), otherwise in-memory SQLite
    SQLALCHEMY_DATABASE_URI = os.getenv("TEST_DATABASE_URL") or "sqlite:///:memory:"
    WTF_CSRF_ENABLED = False
    SERVER_NAME = "127.0.0.1:5000"


# class TestingConfig(Config):
#     SQLALCHEMY_DATABASE_URI = "sqlite:///./test.db"
#     WTF_CSRF_ENABLED = False
#     SQLALCHEMY_TRACK_MODIFICATIONS = False
#     SERVER_NAME = "127.0.0.1:5000"
