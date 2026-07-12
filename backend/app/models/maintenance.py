"""
Maintenance Model

Represents a service/repair record for a vehicle.

Responsibilities:
✓ Store maintenance service details
✓ Track maintenance status (Active/Closed)

Relationships:
Maintenance -> Vehicle
"""

from datetime import date as date_type

from sqlalchemy import String, Float, Date, ForeignKey
from sqlalchemy import Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base, BaseModel
from app.models.enums import MaintenanceStatus


class Maintenance(Base, BaseModel):
    __tablename__ = "maintenance"

    vehicle_id: Mapped[int] = mapped_column(
        ForeignKey("vehicles.id"),
        nullable=False,
    )
    service_type: Mapped[str] = mapped_column(
        String(100),
        nullable=False,
    )
    cost: Mapped[float] = mapped_column(
        Float,
        nullable=False,
    )
    service_date: Mapped[date_type] = mapped_column(
        Date,
        nullable=False,
    )
    status: Mapped[MaintenanceStatus] = mapped_column(
        SQLEnum(MaintenanceStatus),
        default=MaintenanceStatus.ACTIVE,
    )

    vehicle: Mapped["Vehicle"] = relationship(
        back_populates="maintenance_logs",
    )

    def __repr__(self) -> str:
        return f"<Maintenance {self.service_type} for vehicle {self.vehicle_id}>"