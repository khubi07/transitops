"""
Trip Service

Contains all business logic related to Trips.
"""

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.repositories.trip_repository import TripRepository
from app.schemas.trip import TripCreate, TripComplete
from app.models.enums import TripStatus


class TripService:

    @staticmethod
    def create_trip(db: Session, trip: TripCreate):
        # TODO:
        # Validate Vehicle Exists
        # Validate Driver Exists
        # Validate Capacity
        return TripRepository.create(db, trip)

    @staticmethod
    def get_all_trips(db: Session):
        return TripRepository.get_all(db)

    @staticmethod
    def get_trip(db: Session, trip_id: int):

        trip = TripRepository.get_by_id(db, trip_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found."
            )

        return trip

    @staticmethod
    def dispatch_trip(db: Session, trip_id: int):

        trip = TripRepository.get_by_id(db, trip_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found."
            )

        trip.status = TripStatus.DISPATCHED

        return TripRepository.update(db, trip)

    @staticmethod
    def complete_trip(
        db: Session,
        trip_id: int,
        payload: TripComplete
    ):

        trip = TripRepository.get_by_id(db, trip_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found."
            )

        trip.status = TripStatus.COMPLETED

        # TODO:
        # Save fuel_used
        # Update odometer
        # Create FuelLog

        return TripRepository.update(db, trip)

    @staticmethod
    def delete_trip(db: Session, trip_id: int):

        trip = TripRepository.get_by_id(db, trip_id)

        if not trip:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Trip not found."
            )

        TripRepository.delete(db, trip)

        return {
            "message": "Trip deleted successfully."
        }