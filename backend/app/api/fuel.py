"""
api/fuel_logs.py
"""

from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from repositories.fuel_log_repository import FuelLogRepository
from schemas.fuel_log import FuelLogCreate, FuelLogResponse
from services.fuel_log_service import FuelLogService

router = APIRouter(prefix="/fuel-logs", tags=["Fuel Logs"])


def get_fuel_log_service(db: Session = Depends(get_db)) -> FuelLogService:
    return FuelLogService(FuelLogRepository(db))


@router.post("/", response_model=FuelLogResponse, status_code=201)
def create_fuel_log(payload: FuelLogCreate, service: FuelLogService = Depends(get_fuel_log_service)):
    return service.create_fuel_log(payload)


@router.get("/{fuel_log_id}", response_model=FuelLogResponse)
def get_fuel_log(fuel_log_id: int, service: FuelLogService = Depends(get_fuel_log_service)):
    return service.get_fuel_log(fuel_log_id)


@router.get("/trip/{trip_id}", response_model=List[FuelLogResponse])
def list_fuel_logs_for_trip(trip_id: int, service: FuelLogService = Depends(get_fuel_log_service)):
    return service.list_for_trip(trip_id)


@router.get("/trip/{trip_id}/efficiency")
def get_trip_efficiency(trip_id: int, service: FuelLogService = Depends(get_fuel_log_service)):
    return {"trip_id": trip_id, "km_per_liter": service.average_efficiency_km_per_liter(trip_id)}