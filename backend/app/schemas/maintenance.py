from datetime import date as date_type

from pydantic import BaseModel

from app.models.enums import MaintenanceStatus


class MaintenanceCreate(BaseModel):
    vehicle_id: int
    service_type: str
    cost: float
    service_date: date_type


class MaintenanceResponse(BaseModel):
    id: int
    vehicle_id: int
    service_type: str
    cost: float
    service_date: date_type
    status: MaintenanceStatus

    class Config:
        from_attributes = True