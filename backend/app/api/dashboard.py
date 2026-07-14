"""
api/dashboard.py
"""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.repositories.driver_repository import DriverRepository
from app.repositories.expense_repository import ExpenseRepository
from app.repositories.fuel_log_repository import FuelLogRepository
from app.schemas.dashboard import FleetKPIResponse
from app.schemas.services.dashboard_service import DashboardService

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


def get_dashboard_service(db: Session = Depends(get_db)) -> DashboardService:
    return DashboardService(
        DriverRepository(db),
        FuelLogRepository(db),
        ExpenseRepository(db),
    )


@router.get("/kpis", response_model=FleetKPIResponse)
def get_fleet_kpis(start: date, end: date, service: DashboardService = Depends(get_dashboard_service)):
    return service.get_fleet_kpis(start, end)