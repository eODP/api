import os
from dotenv import load_dotenv

load_dotenv(".env", verbose=True)


class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL")
    SECRET_KEY = os.environ.get("APP_SECRET_KEY")


class DevelopmentConfig(Config):
    DEBUG = True
    PORT = os.environ.get("PORT")


class ProductionConfig(Config):
    DEBUG = False
