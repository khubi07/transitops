"""
api/expenses.py
"""

from datetime import date
from typing import List, Optional

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enums import ExpenseType
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.services.expense_service import ExpenseService

router = APIRouter(prefix="/expenses", tags=["Expenses"])


def get_expense_service(db: Session = Depends(get_db)) -> ExpenseService:
    return ExpenseService(ExpenseRepository(db))


@router.post("/", response_model=ExpenseResponse, status_code=201)
def create_expense(payload: ExpenseCreate, service: ExpenseService = Depends(get_expense_service)):
    return service.create_expense(payload)


@router.get("/{expense_id}", response_model=ExpenseResponse)
def get_expense(expense_id: int, service: ExpenseService = Depends(get_expense_service)):
    return service.get_expense(expense_id)


@router.get("/trip/{trip_id}", response_model=List[ExpenseResponse])
def list_expenses_for_trip(trip_id: int, service: ExpenseService = Depends(get_expense_service)):
    return service.list_for_trip(trip_id)


@router.get("/summary/total")
def get_total_operational_cost(
    start: date,
    end: date,
    category: Optional[ExpenseType] = None,
    service: ExpenseService = Depends(get_expense_service),
):
    return {"total": service.total_operational_cost(start, end, category=category)}