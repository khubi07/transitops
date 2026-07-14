"""
ExpenseRepository

Per folder rules: repositories/ ONLY interacts with the database.
"""

from datetime import date
from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.expense import Expense
from app.models.enums import ExpenseType


class ExpenseRepository:

    def __init__(self, db: Session):
        self.db = db

    def create(self, expense: Expense) -> Expense:
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_by_id(self, expense_id: int) -> Optional[Expense]:
        return self.db.get(Expense, expense_id)

    def list_by_trip(self, trip_id: int) -> List[Expense]:
        stmt = select(Expense).where(Expense.trip_id == trip_id)
        return list(self.db.execute(stmt).scalars().all())

    def list_between(
        self,
        start: date,
        end: date,
        category: Optional[ExpenseType] = None,
    ) -> List[Expense]:
        stmt = select(Expense).where(
            Expense.expense_date >= start,
            Expense.expense_date <= end,
        )
        if category is not None:
            stmt = stmt.where(Expense.category == category)
        return list(self.db.execute(stmt).scalars().all())