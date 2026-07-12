"""
Trip Schemas
============

Pydantic schemas used for request validation
and API responses.

Author:
-------
Khubi
"""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import TripStatus


class TripBase(BaseModel):
    """
    Common trip fields shared by multiple schemas.
    """

    source: str = Field(..., max_length=100)
    destination: str = Field(..., max_length=100)
    cargo_weight: float = Field(..., gt=0)
    distance: float = Field(..., gt=0)


class TripCreate(TripBase):
    """
    Request body for creating a trip.
    """

    vehicle_id: int
    driver_id: int


class TripUpdate(TripBase):
    """
    Request body for updating trip details.
    """

    pass


class TripDispatch(BaseModel):
    """
    Request body for dispatching a trip.

    Currently empty but kept for future extensibility.
    """

    pass


class TripComplete(BaseModel):
    """
    Request body for completing a trip.
    """

    fuel_used: float = Field(..., gt=0)
    final_odometer: float = Field(..., gt=0)


class TripResponse(TripBase):
    """
    Response returned to the client.
    """

    id: int

    vehicle_id: int
    driver_id: int

    status: TripStatus

    dispatch_time: datetime | None
    completion_time: datetime | None

    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)