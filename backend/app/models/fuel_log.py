"""
FuelLog Model

Represents a single refueling entry linked to a trip.

Responsibilities

✓ Store fuel purchase details

✓ Support fuel efficiency calculations

Relationships

FuelLog -> Trip
"""

from typing import TYPE_CHECKING

from sqlalchemy import Date, ForeignKey, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

# from app.models.base_model import BaseModel
from app.db.base import Base, BaseModel

if TYPE_CHECKING:
    from app.models.trip import Trip  


class FuelLog(Base,BaseModel):

    __tablename__ = "fuel_logs"

    # Per guide Section 10 (Duplicate Data): store trip_id only.
    # vehicle_id is NOT stored here - it can be obtained via trip.vehicle_id.
    trip_id: Mapped[int] = mapped_column(
        ForeignKey("trips.id", ondelete="CASCADE"),
        nullable=False,
    )

    liters: Mapped[float] = mapped_column(
        Numeric(8, 2),
        nullable=False,
    )

    cost: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    odometer_reading: Mapped[int] = mapped_column(
        nullable=False,
    )

    fuel_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    trip: Mapped["Trip"] = relationship(
        back_populates="fuel_logs",
    )

    def __repr__(self) -> str:
        return f"<FuelLog id={self.id} trip_id={self.trip_id} liters={self.liters}>"