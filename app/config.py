import os


class Config:
    """Default settings for local development."""

    DEBUG = True
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///app.db")
