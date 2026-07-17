from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, EmailStr

from app.models.enums import DriverStatus


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
    id: int
    name: str
    license_number: str
    license_expiry: date
    phone: str
    email: Optional[EmailStr] = None
    status: DriverStatus
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True