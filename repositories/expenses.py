from typing import List
from notion_client import Client

from models.expense import Category, Expense


class ExpenseRepository:
    def __init__(self, database_id: str, client: Client):
        self.db_id = database_id
        self.client = client
        self.parent = {
            "type": "database_id",
            "database_id": self.db_id,
        }

    def create_expense(self, expense: Expense):
        data = {"parent": self.parent, "properties": {}}

        data["properties"]["Expense"] = {
            "title": [{"text": {"content": expense.title}}]
        }
        data["properties"]["Amount"] = {"number": expense.amount}
        data["properties"]["Categoria"] = {"select": {"name": expense.category}}
        data["properties"]["Date"] = {"date": {"start": expense.date.isoformat()}}

        if expense.credit_card_id:
            data["properties"]["Credit Card"] = {
                "relation": [{"id": expense.credit_card_id}]
            }
        if expense.debit:
            data["properties"]["Debit"] = {"relation": [{"id": expense.debit}]}
        return self.client.pages.create(**data)

    def get_category_options(self) -> List[Category]:
        categories_dict = (
            self.client.databases.retrieve(database_id=self.db_id)
            .get("properties")
            .get("Categoria")
            .get("select")
            .get("options")
        )

        return [Category(**category) for category in categories_dict]
