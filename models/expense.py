from typing import Optional

from pydantic import BaseModel, Field


class Expense(BaseModel):
    title: str
    amount: float
    category: Optional[str] = Field(..., required=False)
    date: str
    credit_card_id: Optional[str] = Field(..., required=False)
    account_id: Optional[str] = Field(..., required=False)


class Category(BaseModel):
    id: str
    name: str
    color: str
    description: Optional[str]
