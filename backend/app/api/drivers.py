"""
api/drivers.py

Per folder rules: api/ ONLY receives HTTP requests and delegates to
services/. No business logic and no DB queries here.
"""

from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

# NOTE: replace with your actual DB session dependency once
# Member 1's database setup (engine/session factory) is merged in.
from database import get_db

from models.enums import DriverStatus
from repositories.driver_repository import DriverRepository
from schemas.driver import DriverCreate, DriverResponse, DriverUpdate
from backend.app.schemas.services.driver_service import DriverService

router = APIRouter(prefix="/drivers", tags=["Drivers"])


def get_driver_service(db: Session = Depends(get_db)) -> DriverService:
    return DriverService(DriverRepository(db))


@router.post("/", response_model=DriverResponse, status_code=201)
def create_driver(payload: DriverCreate, service: DriverService = Depends(get_driver_service)):
    return service.create_driver(payload)


@router.get("/", response_model=List[DriverResponse])
def list_drivers(
    status: Optional[DriverStatus] = None,
    service: DriverService = Depends(get_driver_service),
):
    return service.list_drivers(status=status)


@router.get("/{driver_id}", response_model=DriverResponse)
def get_driver(driver_id: int, service: DriverService = Depends(get_driver_service)):
    return service.get_driver(driver_id)


@router.patch("/{driver_id}", response_model=DriverResponse)
def update_driver(
    driver_id: int,
    payload: DriverUpdate,
    service: DriverService = Depends(get_driver_service),
):
    return service.update_driver(driver_id, payload)


@router.delete("/{driver_id}", response_model=DriverResponse)
def suspend_driver(driver_id: int, service: DriverService = Depends(get_driver_service)):
    # Soft delete per guide Section 13 - sets status to SUSPENDED.
    return service.suspend_driver(driver_id)