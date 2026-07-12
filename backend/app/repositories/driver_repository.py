"""
DriverRepository

Per folder rules: repositories/ ONLY interacts with the database.
No business logic here - that belongs in services/driver_service.py.
"""

from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from models.driver import Driver
from models.enums import DriverStatus


class DriverRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, driver: Driver) -> Driver:
        self.db.add(driver)
        self.db.commit()
        self.db.refresh(driver)
        return driver

    def get_by_id(self, driver_id: int) -> Optional[Driver]:
        return self.db.get(Driver, driver_id)

    def get_by_license_number(self, license_number: str) -> Optional[Driver]:
        stmt = select(Driver).where(Driver.license_number == license_number)
        return self.db.execute(stmt).scalar_one_or_none()

    def list(self, status: Optional[DriverStatus] = None) -> List[Driver]:
        stmt = select(Driver)
        if status is not None:
            stmt = stmt.where(Driver.status == status)
        return list(self.db.execute(stmt).scalars().all())

    def update(self, driver: Driver) -> Driver:
        self.db.commit()
        self.db.refresh(driver)
        return driver

    # Per guide Section 13: never permanently delete. Status update only.
    def set_status(self, driver: Driver, status: DriverStatus) -> Driver:
        driver.status = status
        return self.update(driver)