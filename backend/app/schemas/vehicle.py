from typing import Optional

from pydantic import BaseModel

from app.models.enums import VehicleStatus


class VehicleCreate(BaseModel):
    reg_no: str
    name: str
    type: str
    capacity_kg: float
    odometer: float = 0
    acquisition_cost: float


class VehicleUpdate(BaseModel):
    name: Optional[str] = None
    type: Optional[str] = None
    capacity_kg: Optional[float] = None
    odometer: Optional[float] = None
    acquisition_cost: Optional[float] = None
    status: Optional[VehicleStatus] = None


class VehicleResponse(BaseModel):
    id: int
    reg_no: str
    name: str
    type: str
    capacity_kg: float
    odometer: float
    acquisition_cost: float
    status: VehicleStatus

    class Config:
        from_attributes = True