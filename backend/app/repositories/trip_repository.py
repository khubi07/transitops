"""
Trip Repository

Only responsible for database operations.
No business logic.
"""

from sqlalchemy.orm import Session

from app.models.trip import Trip
from app.schemas.trip import TripCreate


class TripRepository:

    @staticmethod
    def create(db: Session, trip: TripCreate) -> Trip:
        db_trip = Trip(**trip.model_dump())

        db.add(db_trip)
        db.commit()
        db.refresh(db_trip)

        return db_trip

    @staticmethod
    def get_by_id(db: Session, trip_id: int) -> Trip | None:
        return db.query(Trip).filter(Trip.id == trip_id).first()

    @staticmethod
    def get_all(db: Session):
        return db.query(Trip).all()

    @staticmethod
    def update(db: Session, trip: Trip):
        db.commit()
        db.refresh(trip)
        return trip

    @staticmethod
    def delete(db: Session, trip: Trip):
        db.delete(trip)
        db.commit()