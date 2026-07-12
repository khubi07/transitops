"""
Database Configuration

Responsibilities
----------------
- Create SQLAlchemy Engine
- Create Database Session
- Dependency for FastAPI

Author: Team TransitOps
"""

from sqlalchemy import create_engine  # type: ignore[import]
from sqlalchemy.orm import sessionmaker  # type: ignore[import]

DATABASE_URL = "sqlite:///./transitops.db"
# Later you can change to PostgreSQL:
# postgresql://username:password@localhost/transitops

engine = create_engine(
    DATABASE_URL,
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