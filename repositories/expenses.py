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
        self.icon = {"type": "emoji", "emoji": "📤"}
        self.children = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [{"type": "text", "text": {"content": "Descrição"}}]
                },
            },
            {
                "object": "block",
                "type": "bulleted_list_item",
                "bulleted_list_item": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": "",
                            },
                        }
                    ],
                },
            },
        ]

    def create_expense(self, expense: Expense):
        data = {
            "parent": self.parent,
            "properties": {},
            "icon": self.icon,
            "children": self.children,
        }

        data["properties"]["Expense"] = {
            "title": [{"text": {"content": expense.title}}]
        }
        data["properties"]["Amount"] = {"number": expense.amount}
        if expense.category:
            data["properties"]["Categoria"] = {"select": {"name": expense.category}}
        data["properties"]["Date"] = {"date": {"start": expense.date}}

        if expense.credit_card_id:
            data["properties"]["Credit Card"] = {
                "relation": [{"id": expense.credit_card_id}]
            }
        if expense.account_id:
            data["properties"]["Debit"] = {"relation": [{"id": expense.account_id}]}
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
