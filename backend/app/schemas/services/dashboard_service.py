"""
DashboardService

Per folder rules: services/ contains business logic.
Owns: Fleet KPI aggregation for the dashboard.

NOTE: this is the one place your module reaches across boundaries.
Today it only aggregates fuel + expense + driver data (your own
modules). Once Member 1 (trips) and Member 2 (vehicles/maintenance)
have repositories, extend this service to pull in trip counts and
vehicle status counts too - do NOT let DriverService/FuelLogService/
ExpenseService themselves depend on other modules; keep cross-module
aggregation isolated here.
"""

from datetime import date

from repositories.driver_repository import DriverRepository
from repositories.expense_repository import ExpenseRepository
from repositories.fuel_log_repository import FuelLogRepository
from schemas.dashboard import FleetKPIResponse
from backend.app.schemas.services.expense_service import ExpenseService
from services.fuel_log_service import FuelLogService


class DashboardService:

    def __init__(
        self,
        driver_repo: DriverRepository,
        fuel_log_repo: FuelLogRepository,
        expense_repo: ExpenseRepository,
    ):
        self.driver_repo = driver_repo
        self.fuel_log_service = FuelLogService(fuel_log_repo)
        self.expense_service = ExpenseService(expense_repo)

    def get_fleet_kpis(self, start: date, end: date) -> FleetKPIResponse:
        total_fuel_cost = self.fuel_log_service.total_fuel_cost(start, end)
        total_expense_cost = self.expense_service.total_operational_cost(start, end)

        from backend.app.schemas.services.driver_service import DriverService  # local import avoids a cycle

        driver_service = DriverService(self.driver_repo)
        expiring = driver_service.drivers_with_expiring_license()

        active_drivers = len(driver_service.list_drivers())

        return FleetKPIResponse(
            period_start=start,
            period_end=end,
            total_fuel_cost=total_fuel_cost,
            total_expense_cost=total_expense_cost,
            total_operational_cost=round(total_fuel_cost + total_expense_cost, 2),
            average_fuel_efficiency_km_per_liter=None,  # needs per-trip aggregation once Trip exists
            active_drivers=active_drivers,
            drivers_with_expiring_license=len(expiring),
        )