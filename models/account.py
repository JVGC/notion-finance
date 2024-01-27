from pydantic import BaseModel


class Account(BaseModel):
    id: str
    name: str
    account_type: str
