
"""
Database Configuration

Responsibilities
----------------
- Create SQLAlchemy Engine
- Create Database Session
- Dependency for FastAPI

Author: Team TransitOps
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db():
    """
    FastAPI Dependency.
    Returns a database session.
    """

    db = SessionLocal()

    try:
        yield db


    finally:
        db.close()