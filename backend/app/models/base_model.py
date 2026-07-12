"""
Common Base Model

Inherited by every table.

Provides:
----------
- id
- created_at
- updated_at
"""

from datetime import datetime

from sqlalchemy import DateTime
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.sql import func


class BaseModel:
    """
    Common columns for all database tables.
    """

    id: Mapped[int] = mapped_column(
        primary_key=True,
        index=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now()
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now()
    )