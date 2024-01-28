from typing import List
from notion_client import Client

from models.account import Account


class AccountRepository:
    def __init__(self, database_id: str, client: Client):
        self.db_id = database_id
        self.client = client
        self.parent = {
            "type": "database_id",
            "database_id": self.db_id,
        }

    def _list_all(self, filter_dict: dict) -> List[Account]:
        cards = self.client.databases.query(
            **{"database_id": self.db_id, "filter": filter_dict},
        ).get("results")
        return [
            Account(
                id=card["id"],
                name=card["properties"]["Name"]["title"][0]["text"]["content"],
                account_type=card["properties"]["Tipo"]["select"]["name"],
            )
            for card in cards
        ]

    def list_all_current(self) -> List[Account]:
        return self._list_all(
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Corrente",
                },
            },
        )

    def list_all_investiment(self) -> List[Account]:
        return self._list_all(
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Investimento",
                },
            },
        )

    def list_all_boxes(self) -> List[Account]:
        return self._list_all(
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Caixinha",
                },
            },
        )
