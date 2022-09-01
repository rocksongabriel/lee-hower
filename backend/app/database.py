from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import get_settings

settings = get_settings()

SQLALCHEMY_DATABASE_URL = (
    f"postgresql://{settings.dev_database_username}:{settings.dev_database_password}"
    f"@{settings.dev_database_host}:{settings.dev_database_port}/"
    f"{settings.dev_database_name}"
)

engine = create_engine(SQLALCHEMY_DATABASE_URL)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
