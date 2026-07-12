"""
ExpenseService

Per folder rules: services/ contains business logic.
Owns: operational cost calculations.
"""

from datetime import date
from typing import List, Optional

from fastapi import HTTPException, status as http_status

from models.enums import ExpenseType
from models.expense import Expense
from repositories.expense_repository import ExpenseRepository
from schemas.expense import ExpenseCreate


class ExpenseService:

    def __init__(self, repo: ExpenseRepository):
        self.repo = repo

    def create_expense(self, payload: ExpenseCreate) -> Expense:
        expense = Expense(**payload.model_dump())
        return self.repo.create(expense)

    def get_expense(self, expense_id: int) -> Expense:
        expense = self.repo.get_by_id(expense_id)
        if expense is None:
            raise HTTPException(
                status_code=http_status.HTTP_404_NOT_FOUND,
                detail="Expense not found.",
            )
        return expense

    def list_for_trip(self, trip_id: int) -> List[Expense]:
        return self.repo.list_by_trip(trip_id)

    def total_operational_cost(
        self,
        start: date,
        end: date,
        category: Optional[ExpenseType] = None,
    ) -> float:
        expenses = self.repo.list_between(start, end, category=category)
        return round(sum(float(e.amount) for e in expenses), 2)

    def breakdown_by_category(self, start: date, end: date) -> dict:
        expenses = self.repo.list_between(start, end)
        breakdown: dict = {}
        for e in expenses:
            key = e.category.value
            breakdown[key] = round(breakdown.get(key, 0) + float(e.amount), 2)
        return breakdown