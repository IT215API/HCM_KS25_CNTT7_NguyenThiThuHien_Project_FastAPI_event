# engine, SessionLocal. Base, get_db
from app.core.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase

DATABASE_URL = settings.DATABASE_URL

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autoflush=False,
    autocommit=False,
    bind=engine
)

def get_db():
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()

class Base(DeclarativeBase):
    pass