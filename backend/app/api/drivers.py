"""
Driver API
"""

from typing import Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enums import DriverStatus
from app.schemas.driver import (
    DriverCreate,
    DriverResponse,
    DriverUpdate,
)
from app.schemas.services.driver_service import DriverService

router = APIRouter(
    prefix="/drivers",
    tags=["Drivers"],
)


@router.post(
    "/",
    response_model=DriverResponse,
    status_code=201,
)
def create_driver(
    payload: DriverCreate,
    db: Session = Depends(get_db),
):
    return DriverService(db).create_driver(payload)


@router.get(
    "/",
    response_model=list[DriverResponse],
)
def list_drivers(
    status: Optional[DriverStatus] = None,
    db: Session = Depends(get_db),
):
    return DriverService(db).list_drivers(status)


@router.get(
    "/{driver_id}",
    response_model=DriverResponse,
)
def get_driver(
    driver_id: int,
    db: Session = Depends(get_db),
):
    return DriverService(db).get_driver(driver_id)


@router.patch(
    "/{driver_id}",
    response_model=DriverResponse,
)
def update_driver(
    driver_id: int,
    payload: DriverUpdate,
    db: Session = Depends(get_db),
):
    return DriverService(db).update_driver(driver_id, payload)


@router.delete(
    "/{driver_id}",
    response_model=DriverResponse,
)
def suspend_driver(
    driver_id: int,
    db: Session = Depends(get_db),
):
    return DriverService(db).suspend_driver(driver_id)