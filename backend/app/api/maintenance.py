from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.maintenance import MaintenanceCreate, MaintenanceResponse
from app.services.maintenance_service import MaintenanceService
from app.repositories.maintenance_repository import MaintenanceRepository

router = APIRouter(prefix="/maintenance", tags=["Maintenance"])


@router.get("/", response_model=list[MaintenanceResponse])
def list_maintenance(db: Session = Depends(get_db)):
    return MaintenanceRepository(db).get_all()


@router.post("/", response_model=MaintenanceResponse)
def create_maintenance(data: MaintenanceCreate, db: Session = Depends(get_db)):
    return MaintenanceService(db).create_maintenance(data)


@router.patch("/{maintenance_id}/close", response_model=MaintenanceResponse)
def close_maintenance(maintenance_id: int, db: Session = Depends(get_db)):
    return MaintenanceService(db).close_maintenance(maintenance_id)