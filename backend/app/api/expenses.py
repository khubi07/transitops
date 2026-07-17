"""
Expense API

Handles all Expense-related endpoints.
"""

from datetime import date

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.enums import ExpenseType
from app.schemas.expense import ExpenseCreate, ExpenseResponse
from app.schemas.services.expense_service import ExpenseService

router = APIRouter(
    prefix="/expenses",
    tags=["Expenses"],
)


@router.post(
    "/",
    response_model=ExpenseResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_expense(
    payload: ExpenseCreate,
    db: Session = Depends(get_db),
):
    return ExpenseService(db).create_expense(payload)


@router.get(
    "/{expense_id}",
    response_model=ExpenseResponse,
)
def get_expense(
    expense_id: int,
    db: Session = Depends(get_db),
):
    return ExpenseService(db).get_expense(expense_id)


@router.get(
    "/trip/{trip_id}",
    response_model=list[ExpenseResponse],
)
def list_expenses_for_trip(
    trip_id: int,
    db: Session = Depends(get_db),
):
    return ExpenseService(db).list_for_trip(trip_id)


@router.get("/summary/total")
def get_total_operational_cost(
    start: date,
    end: date,
    category: ExpenseType | None = None,
    db: Session = Depends(get_db),
):
    return {
        "total": ExpenseService(db).total_operational_cost(
            start,
            end,
            category,
        )
    }