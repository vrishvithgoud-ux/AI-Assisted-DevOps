from flask import Flask
from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker


def init_db(app: Flask) -> None:
    """Create and attach the SQLAlchemy engine and session factory."""
    engine = create_engine(app.config["DATABASE_URL"])
    from .models.service import Base

    Base.metadata.create_all(engine)
    session_factory = sessionmaker(bind=engine, expire_on_commit=False)

    app.extensions["sqlalchemy_engine"] = engine
    app.extensions["sqlalchemy_session_factory"] = session_factory
