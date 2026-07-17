"""
DashboardService

Per folder rules: services/ contains business logic.
Owns: Fleet KPI aggregation for the dashboard.

NOTE:
This is the only service that aggregates data across multiple modules.
"""

from datetime import date

from sqlalchemy.orm import Session

from app.repositories.driver_repository import DriverRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.fuel_log_repository import FuelLogRepository

from app.schemas.dashboard import FleetKPIResponse
from app.schemas.services.driver_service import DriverService
from app.schemas.services.expense_service import ExpenseService
from app.schemas.services.fuel_log_service import FuelLogService


class DashboardService:
    def __init__(self, db: Session):
        self.driver_repository = DriverRepository(db)

        self.fuel_log_service = FuelLogService(db)
        self.expense_service = ExpenseService(db)
        self.driver_service = DriverService(db)

    def get_fleet_kpis(
        self,
        start: date,
        end: date,
    ) -> FleetKPIResponse:
        total_fuel_cost = self.fuel_log_service.total_fuel_cost(
            start,
            end,
        )

        total_expense_cost = self.expense_service.total_operational_cost(
            start,
            end,
        )

        expiring = self.driver_service.drivers_with_expiring_license()

        active_drivers = len(
            self.driver_service.list_drivers()
        )

        return FleetKPIResponse(
            period_start=start,
            period_end=end,
            total_fuel_cost=total_fuel_cost,
            total_expense_cost=total_expense_cost,
            total_operational_cost=round(
                total_fuel_cost + total_expense_cost,
                2,
            ),
            average_fuel_efficiency_km_per_liter=None,
            active_drivers=active_drivers,
            drivers_with_expiring_license=len(expiring),
        )