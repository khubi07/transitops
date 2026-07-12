"""
Trip Model
==========

Represents a transportation trip in the system.

Responsibilities
----------------
✓ Assign a Vehicle
✓ Assign a Driver
✓ Track Cargo
✓ Track Route
✓ Track Trip Status

Relationships
-------------
Trip -> Vehicle (Many-to-One)
Trip -> Driver (Many-to-One)
Trip -> FuelLog (One-to-Many)
Trip -> Expense (One-to-Many)

Author:
-------
Khubi
"""

from datetime import datetime

from sqlalchemy import (
    DateTime,
    Enum,
    Float,
    ForeignKey,
    String,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.models.base_model import BaseModel
from app.models.enums import TripStatus


class Trip(Base, BaseModel):
    """
    SQLAlchemy model representing a Trip.
    """

    __tablename__ = "trips"

    # ------------------------
    # Foreign Keys
    # ------------------------

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id", ondelete="RESTRICT"),
        nullable=False,
    )

    driver_id: Mapped[int] = mapped_column(
        ForeignKey("drivers.id", ondelete="RESTRICT"),
        nullable=False,
    )

    # ------------------------
    # Trip Details
    # ------------------------

    source: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    destination: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    cargo_weight: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    distance: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )

    status: Mapped[TripStatus] = mapped_column(
        Enum(TripStatus),
        default=TripStatus.DRAFT,
        nullable=False,
    )

    dispatch_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    completion_time: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
    )

    # ------------------------
    # Relationships
    # ------------------------

    vehicle = relationship(
        "Vehicle",
        back_populates="trips",
    )

    driver = relationship(
        "Driver",
        back_populates="trips",
    )

    fuel_logs = relationship(
        "FuelLog",
        back_populates="trip",
        cascade="all, delete-orphan",
    )

    expenses = relationship(
        "Expense",
        back_populates="trip",
    )

    # ------------------------
    # Debug Representation
    # ------------------------

    def __repr__(self) -> str:
        return (
            f"<Trip(id={self.id}, "
            f"vehicle={self.vehicle_id}, "
            f"driver={self.driver_id}, "
            f"status='{self.status.value}')>"
        )