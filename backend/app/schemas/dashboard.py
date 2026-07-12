from datetime import date
from typing import Optional

from pydantic import BaseModel


class FleetKPIResponse(BaseModel):
    """
    Aggregate KPIs for the fleet dashboard.
    Populated by DashboardService from fuel_log / expense repositories
    (and, once integrated, Member 1's trip repository + Member 2's
    vehicle repository).
    """

    period_start: Optional[date] = None
    period_end: Optional[date] = None

    total_fuel_cost: float
    total_expense_cost: float
    total_operational_cost: float
    average_fuel_efficiency_km_per_liter: Optional[float] = None
    active_drivers: int
    drivers_with_expiring_license: int