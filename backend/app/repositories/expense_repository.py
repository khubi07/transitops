"""
ExpenseRepository

Per folder rules: repositories/ ONLY interacts with the database.
"""

from datetime import date

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.enums import ExpenseType
from app.models.expense import Expense


class ExpenseRepository:
    def __init__(self, db: Session):
        self.db = db

    def create(self, expense: Expense) -> Expense:
        self.db.add(expense)
        self.db.commit()
        self.db.refresh(expense)
        return expense

    def get_by_id(self, expense_id: int) -> Expense | None:
        return self.db.get(Expense, expense_id)

    def list_by_trip(self, trip_id: int) -> list[Expense]:
        stmt = select(Expense).where(Expense.trip_id == trip_id)
        return list(self.db.execute(stmt).scalars().all())

    def list_between(
        self,
        start: date,
        end: date,
        category: ExpenseType | None = None,
    ) -> list[Expense]:
        stmt = select(Expense).where(
            Expense.expense_date >= start,
            Expense.expense_date <= end,
        )

        if category is not None:
            stmt = stmt.where(Expense.category == category)

        return list(self.db.execute(stmt).scalars().all())