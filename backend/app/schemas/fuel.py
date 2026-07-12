from datetime import date, datetime

from pydantic import BaseModel, ConfigDict, Field


class FuelLogCreate(BaseModel):
    trip_id: int
    liters: float = Field(gt=0)
    cost: float = Field(gt=0)
    odometer_reading: int = Field(gt=0)
    fuel_date: date


class FuelLogResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: int
    liters: float
    cost: float
    odometer_reading: int
    fuel_date: date
    created_at: datetime
    updated_at: datetime