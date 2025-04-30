from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+asyncpg://user:password@db:5432/fastapi_app")

# Create engine
engine = create_engine(DATABASE_URL, echo=True)

# Create sessionmaker factory
SessionLocal = sessionmaker(bind=engine)

# Base class for models
class Base(DeclarativeBase):
    pass

# Dependency to get DB session
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()
