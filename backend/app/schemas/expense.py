
from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from app.models.enums import ExpenseType


class ExpenseCreate(BaseModel):
    trip_id: Optional[int] = None
    category: ExpenseType
    amount: float = Field(gt=0)
    description: Optional[str] = None
    expense_date: date


class ExpenseResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    trip_id: Optional[int] = None
    category: ExpenseType
    amount: float
    description: Optional[str] = None
    expense_date: date
    created_at: datetime
    updated_at: datetime