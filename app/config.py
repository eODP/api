import os
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_ORM")
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")
    PER_PAGE = 20


class DevelopmentConfig(Config):
    DEBUG = True
    # SQLALCHEMY_ECHO = True


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL_TESTING")


class ProductionConfig(Config):
    DEBUG = False
