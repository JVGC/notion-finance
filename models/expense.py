from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class Expense(BaseModel):
    title: str
    amount: float
    category: str
    date: datetime
    credit_card_id: Optional[str]
    debit: Optional[str]


class Category(BaseModel):
    id: str
    name: str
    color: str
    description: Optional[str]
