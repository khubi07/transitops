"""
Expense Model

Represents an operational expense, optionally linked to a trip.

Responsibilities

✓ Store expense details

✓ Support operational cost calculations

Relationships

Expense -> Trip (optional)
"""

from typing import TYPE_CHECKING, Optional

from sqlalchemy import Date, Enum, ForeignKey, Numeric, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.db.base import Base, BaseModel
# from app.models.base_model import BaseModel
from app.models.enums import ExpenseType

if TYPE_CHECKING:
    from models.trip import Trip  # owned by Member 1 - not created yet


class Expense(Base, BaseModel):

    __tablename__ = "expenses"

    # Per ER Diagram Section 8: Trip -> Expense is SET NULL, so this
    # must stay nullable (an expense can outlive/detach from its trip).
    trip_id: Mapped[Optional[int]] = mapped_column(
        ForeignKey("trips.id", ondelete="SET NULL"),
        nullable=True,
    )

    category: Mapped[ExpenseType] = mapped_column(
        Enum(ExpenseType),
        nullable=False,
    )

    amount: Mapped[float] = mapped_column(
        Numeric(10, 2),
        nullable=False,
    )

    description: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True,
    )

    expense_date: Mapped[Date] = mapped_column(
        Date,
        nullable=False,
    )

    trip: Mapped[Optional["Trip"]] = relationship(
        back_populates="expenses",
    )

    def __repr__(self) -> str:
        return f"<Expense id={self.id} category={self.category} amount={self.amount}>"