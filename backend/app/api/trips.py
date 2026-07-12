"""
Trip API

Handles all Trip-related endpoints.
"""

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.trip import (
    TripComplete,
    TripCreate,
    TripResponse,
)
from app.schemas.services.trip_service import TripService

router = APIRouter(
    prefix="/trips",
    tags=["Trips"],
)


@router.post(
    "/",
    response_model=TripResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_trip(
    trip: TripCreate,
    db: Session = Depends(get_db),
):
    return TripService.create_trip(db, trip)


@router.get(
    "/",
    response_model=list[TripResponse],
)
def get_all_trips(
    db: Session = Depends(get_db),
):
    return TripService.get_all_trips(db)


@router.get(
    "/{trip_id}",
    response_model=TripResponse,
)
def get_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return TripService.get_trip(db, trip_id)


@router.patch(
    "/{trip_id}/dispatch",
    response_model=TripResponse,
)
def dispatch_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return TripService.dispatch_trip(db, trip_id)


@router.patch(
    "/{trip_id}/complete",
    response_model=TripResponse,
)
def complete_trip(
    trip_id: int,
    payload: TripComplete,
    db: Session = Depends(get_db),
):
    return TripService.complete_trip(
        db,
        trip_id,
        payload,
    )


@router.delete(
    "/{trip_id}",
)
def delete_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return TripService.delete_trip(db, trip_id)