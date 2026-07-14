"""
FuelLogService

Per folder rules: services/ contains business logic.
Owns: fuel efficiency calculations.
"""

from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status as http_status

from app.models.fuel_log import FuelLog
from app.repositories.fuel_log_repository import FuelLogRepository
from app.schemas.fuel_log import FuelLogCreate


class FuelLogService:

    def __init__(self, repo: FuelLogRepository):
        self.repo = repo

    def create_fuel_log(self, payload: FuelLogCreate) -> FuelLog:
        # NOTE: once Member 1's Trip model/repository exists, validate
        # trip_id exists and trip is not already COMPLETED/CANCELLED
        # before allowing a fuel log against it.
        fuel_log = FuelLog(**payload.model_dump())
        return self.repo.create(fuel_log)

    def get_fuel_log(self, fuel_log_id: int) -> FuelLog:
        fuel_log = self.repo.get_by_id(fuel_log_id)
        if fuel_log is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Fuel log not found.",
            )
        return fuel_log

    def list_for_trip(self, trip_id: int) -> List[FuelLog]:
        return self.repo.list_by_trip(trip_id)

    def total_fuel_cost(self, start: date, end: date) -> float:
        logs = self.repo.list_between(start, end)
        return round(sum(float(log.cost) for log in logs), 2)

    def total_liters(self, start: date, end: date) -> float:
        logs = self.repo.list_between(start, end)
        return round(sum(float(log.liters) for log in logs), 2)

    def average_efficiency_km_per_liter(self, trip_id: int) -> Optional[float]:
        """
        km/liter for a single trip, derived from consecutive odometer
        readings across that trip's fuel logs. Returns None if there
        isn't enough data (fewer than 2 logs).
        """
        logs = sorted(self.repo.list_by_trip(trip_id), key=lambda log: log.odometer_reading)
        if len(logs) < 2:
            return None

        distance = logs[-1].odometer_reading - logs[0].odometer_reading
        liters_consumed = sum(float(log.liters) for log in logs[:-1])

        if liters_consumed <= 0:
            return None

        return round(distance / liters_consumed, 2)