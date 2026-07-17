from datetime import date

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from app.models.fuel_log import FuelLog
from app.repositories.fuel_log_repository import FuelLogRepository
from app.schemas.fuel_log import FuelLogCreate


class FuelLogService:
    def __init__(self, db: Session):
        self.repository = FuelLogRepository(db)
        self.db = db

    def create_fuel_log(self, payload: FuelLogCreate) -> FuelLog:
        fuel_log = FuelLog(**payload.model_dump())
        return self.repository.create(fuel_log)

    def get_fuel_log(self, fuel_log_id: int) -> FuelLog:
        fuel_log = self.repository.get_by_id(fuel_log_id)

        if fuel_log is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Fuel log not found.",
            )

        return fuel_log

    def list_for_trip(self, trip_id: int) -> list[FuelLog]:
        return self.repository.list_by_trip(trip_id)

    def total_fuel_cost(self, start: date, end: date) -> float:
        logs = self.repository.list_between(start, end)
        return round(sum(float(log.cost) for log in logs), 2)

    def total_liters(self, start: date, end: date) -> float:
        logs = self.repository.list_between(start, end)
        return round(sum(float(log.liters) for log in logs), 2)

    def average_efficiency_km_per_liter(
        self,
        trip_id: int,
    ) -> float | None:
        logs = sorted(
            self.repository.list_by_trip(trip_id),
            key=lambda log: log.odometer_reading,
        )

        if len(logs) < 2:
            return None

        distance = logs[-1].odometer_reading - logs[0].odometer_reading
        liters_consumed = sum(float(log.liters) for log in logs[:-1])

        if liters_consumed <= 0:
            return None

        return round(distance / liters_consumed, 2)