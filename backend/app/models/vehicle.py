"""
Vehicle Model

Represents every fleet vehicle.

Responsibilities:
✓ Store vehicle details
✓ Maintain vehicle status

Relationships:
Vehicle -> Maintenance
"""

from typing import TYPE_CHECKING

from sqlalchemy import String, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel
from app.models.enums import VehicleStatus

if TYPE_CHECKING:
    from app.models.maintenance import Maintenance
    from app.models.trip import Trip


class Vehicle(Base, BaseModel):
    __tablename__ = "vehicles"

    reg_no: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
    )
    trips: Mapped[list["Trip"]] = relationship(
    back_populates="vehicle"
)
    name: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
    )
    capacity_kg: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    odometer: Mapped[float] = mapped_column(
        Float,
        default=0,
    )
    acquisition_cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    status: Mapped[VehicleStatus] = mapped_column(
        SQLEnum(VehicleStatus),
        # use getattr to avoid static analysis issues accessing enum attribute
        default=getattr(VehicleStatus, "AVAILABLE"),
    )

    maintenance_logs: Mapped[list["Maintenance"]] = relationship(
        back_populates="vehicle",
    )

    def __repr__(self) -> str:
        return f"<Vehicle {self.reg_no} ({self.status})>"