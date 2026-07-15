"""
Fuel Log API

Handles all Fuel Log related endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.fuel_log import FuelLogCreate, FuelLogResponse
from app.schemas.services.fuel_log_service import FuelLogService

router = APIRouter(
    prefix="/fuel-logs",
    tags=["Fuel Logs"],
)


@router.post(
    "/",
    response_model=FuelLogResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_fuel_log(
    payload: FuelLogCreate,
    db: Session = Depends(get_db),
):
    return FuelLogService(db).create_fuel_log(payload)


@router.get(
    "/{fuel_log_id}",
    response_model=FuelLogResponse,
)
def get_fuel_log(
    fuel_log_id: int,
    db: Session = Depends(get_db),
):
    return FuelLogService(db).get_fuel_log(fuel_log_id)


@router.get(
    "/trip/{trip_id}",
    response_model=list[FuelLogResponse],
)
def list_fuel_logs_for_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return FuelLogService(db).list_for_trip(trip_id)


@router.get(
    "/trip/{trip_id}/efficiency",
)
def get_trip_efficiency(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return {
        "trip_id": trip_id,
        "km_per_liter": FuelLogService(db).average_efficiency_km_per_liter(
            trip_id,
        ),
    }