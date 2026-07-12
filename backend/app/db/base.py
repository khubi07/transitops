"""
SQLAlchemy Base

Every model inherits from this Base.
"""

from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    pass