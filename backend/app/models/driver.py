"""
Driver Model

Represents every registered driver in the fleet.

Responsibilities

✓ Store driver personal and license details

✓ Maintain driver status

Relationships

Driver -> Trips
"""

from typing import TYPE_CHECKING, List

from sqlalchemy import Date, Enum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from models.base import Base, BaseModel
from models.enums import DriverStatus

if TYPE_CHECKING:
    from models.trip import Trip  # owned by Member 1 - not created yet


class Driver(Base, BaseModel):

    __tablename__ = "drivers"

    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )

    license_number: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        unique=True,
        index=True,
    )

    license_expiry: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    phone: Mapped[str] = mapped_column(
        String(20),
        nullable=False,
    )

    email: Mapped[str] = mapped_column(
        String(120),
        nullable=True,
        unique=True,
        index=True,
    )

    status: Mapped[DriverStatus] = mapped_column(
        Enum(DriverStatus),
        nullable=False,
        default=DriverStatus.AVAILABLE,
    )

    trips: Mapped[List["Trip"]] = relationship(
        back_populates="driver",
    )

    def __repr__(self) -> str:
        return f"<Driver id={self.id} name={self.name} status={self.status}>"