"""
Dashboard API
"""

from datetime import date

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.dashboard import FleetKPIResponse
from app.schemas.services.dashboard_service import DashboardService

router = APIRouter(
    prefix="/dashboard",
    tags=["Dashboard"],
)


@router.get(
    "/kpis",
    response_model=FleetKPIResponse,
)
def get_fleet_kpis(
    start: date,
    end: date,
    db: Session = Depends(get_db),
):
    return DashboardService(db).get_fleet_kpis(start, end)