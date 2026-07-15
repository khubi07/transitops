"""
ExpenseService

Per folder rules: services/ contains business logic.
Owns: operational cost calculations.
"""

from datetime import date

from fastapi import HTTPException, status as http_status
from sqlalchemy.orm import Session

from app.models.enums import ExpenseType
from app.models.expense import Expense
from app.repositories.expense_repository import ExpenseRepository
from app.schemas.expense import ExpenseCreate


class ExpenseService:
    def __init__(self, db: Session):
        self.repository = ExpenseRepository(db)
        self.db = db

    def create_expense(self, payload: ExpenseCreate) -> Expense:
        expense = Expense(**payload.model_dump())
        return self.repository.create(expense)

    def get_expense(self, expense_id: int) -> Expense:
        expense = self.repository.get_by_id(expense_id)

        if expense is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Expense not found.",
            )

        return expense

    def list_for_trip(self, trip_id: int) -> list[Expense]:
        return self.repository.list_by_trip(trip_id)

    def total_operational_cost(
        self,
        start: date,
        end: date,
        category: ExpenseType | None = None,
    ) -> float:
        expenses = self.repository.list_between(
            start,
            end,
            category=category,
        )

        return round(
            sum(float(expense.amount) for expense in expenses),
            2,
        )

    def breakdown_by_category(
        self,
        start: date,
        end: date,
    ) -> dict[str, float]:
        expenses = self.repository.list_between(start, end)

        breakdown: dict[str, float] = {}

        for expense in expenses:
            key = expense.category.value
            breakdown[key] = round(
                breakdown.get(key, 0) + float(expense.amount),
                2,
            )

        return breakdown