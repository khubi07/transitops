"""
FuelLogRepository

Per folder rules: repositories/ ONLY interacts with the database.
"""

from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.fuel_log import FuelLog


class FuelLogRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, fuel_log: FuelLog) -> FuelLog:
        self.db.add(fuel_log)
        self.db.commit()
        self.db.refresh(fuel_log)
        return fuel_log

    def get_by_id(self, fuel_log_id: int) -> Optional[FuelLog]:
        return self.db.get(FuelLog, fuel_log_id)

    def list_by_trip(self, trip_id: int) -> List[FuelLog]:
        stmt = select(FuelLog).where(FuelLog.trip_id == trip_id)
        return list(self.db.execute(stmt).scalars().all())

    def list_between(self, start: date, end: date) -> List[FuelLog]:
        stmt = select(FuelLog).where(
            FuelLog.fuel_date >= start,
            FuelLog.fuel_date <= end,
        )
        return list(self.db.execute(stmt).scalars().all())