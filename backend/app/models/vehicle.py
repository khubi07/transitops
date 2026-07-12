"""
Vehicle Model

Represents every fleet vehicle.

Responsibilities:
✓ Store vehicle details
✓ Maintain vehicle status

Relationships:
Vehicle -> Maintenance
"""

from sqlalchemy import String, Float
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel
from app.models.enums import VehicleStatus


class Vehicle(Base, BaseModel):
    __tablename__ = "vehicles"

    reg_no: Mapped[str] = mapped_column(
        String(20),
        unique=True,
        nullable=False,
        index=True,
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
        default=VehicleStatus.AVAILABLE,
    )

    maintenance_logs: Mapped[list["Maintenance"]] = relationship(
        back_populates="vehicle",
    )

    def __repr__(self) -> str:
        return f"<Vehicle {self.reg_no} ({self.status})>"