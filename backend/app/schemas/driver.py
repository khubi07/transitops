from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, EmailStr

from models.enums import DriverStatus


class DriverCreate(BaseModel):
    name: str
    license_number: str
    license_expiry: date
    phone: str
    email: Optional[EmailStr] = None


class DriverUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[EmailStr] = None
    status: Optional[DriverStatus] = None


class DriverResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    license_number: str
    license_expiry: date
    phone: str
    email: Optional[EmailStr] = None
    status: DriverStatus
    created_at: datetime
    updated_at: datetime