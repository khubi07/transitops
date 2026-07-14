"""
DriverService

Per folder rules: services/ contains business logic.
Owns: license expiry checks, status transition rules.
"""

from datetime import date, timedelta
from typing import List, Optional

from fastapi import HTTPException, status as http_status

from app.models.driver import Driver
from app.models.enums import DriverStatus
from app.repositories.driver_repository import DriverRepository
from app.schemas.driver import DriverCreate, DriverUpdate

LICENSE_EXPIRY_WARNING_DAYS = 30

# Business rule: which status transitions are legal.
_ALLOWED_TRANSITIONS = {
    DriverStatus.AVAILABLE: {DriverStatus.ON_TRIP, DriverStatus.OFF_DUTY, DriverStatus.SUSPENDED},
    DriverStatus.ON_TRIP: {DriverStatus.AVAILABLE},
    DriverStatus.OFF_DUTY: {DriverStatus.AVAILABLE, DriverStatus.SUSPENDED},
    DriverStatus.SUSPENDED: {DriverStatus.AVAILABLE},
}


class DriverService:

    def __init__(self, repo: DriverRepository):
        self.repo = repo

    def create_driver(self, payload: DriverCreate) -> Driver:
        if self.repo.get_by_license_number(payload.license_number):
            raise HTTPException(
                status_code=http_status.HTTP_409_CONFLICT,
                detail="A driver with this license number already exists.",
            )
        if payload.license_expiry <= date.today():
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail="License expiry must be in the future.",
            )
        driver = Driver(**payload.model_dump())
        return self.repo.create(driver)

    def get_driver(self, driver_id: int) -> Driver:
        driver = self.repo.get_by_id(driver_id)
        if driver is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Driver not found.",
            )
        return driver

    def list_drivers(self, status: Optional[DriverStatus] = None) -> List[Driver]:
        return self.repo.list(status=status)

    def update_driver(self, driver_id: int, payload: DriverUpdate) -> Driver:
        driver = self.get_driver(driver_id)
        updates = payload.model_dump(exclude_unset=True)

        if "status" in updates:
            self._validate_transition(driver.status, updates["status"])

        for field, value in updates.items():
            setattr(driver, field, value)

        return self.repo.update(driver)

    def suspend_driver(self, driver_id: int) -> Driver:
        # Per guide Section 13: soft delete only - suspend, never delete the row.
        driver = self.get_driver(driver_id)
        self._validate_transition(driver.status, DriverStatus.SUSPENDED)
        return self.repo.set_status(driver, DriverStatus.SUSPENDED)

    def is_eligible_for_dispatch(self, driver: Driver) -> bool:
        """
        Business rule consumed by Member 1's Trip dispatch flow:
        driver must be AVAILABLE and license must not be expired.
        """
        if driver.status != DriverStatus.AVAILABLE:
            return False
        if driver.license_expiry <= date.today():
            return False
        return True

    def drivers_with_expiring_license(self, within_days: int = LICENSE_EXPIRY_WARNING_DAYS) -> List[Driver]:
        cutoff = date.today() + timedelta(days=within_days)
        return [d for d in self.repo.list() if date.today() < d.license_expiry <= cutoff]

    def _validate_transition(self, current: DriverStatus, new: DriverStatus) -> None:
        if new not in _ALLOWED_TRANSITIONS.get(current, set()):
            raise HTTPException(
                status_code=http_status.HTTP_400_BAD_REQUEST,
                detail=f"Cannot transition driver from {current} to {new}.",
            )