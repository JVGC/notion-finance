from pydantic import BaseModel


class CreditCard(BaseModel):
    id: str
    card_name: str
