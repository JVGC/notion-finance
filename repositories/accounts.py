from typing import List
from notion_client import Client

from models.account import Account


class AccountRepository:
    def __init__(self, database_id: str):
        self.db_id = database_id
        self.parent = {
            "type": "database_id",
            "database_id": self.db_id,
        }

    def _list_all(self, client: Client, filter_dict: dict) -> List[Account]:
        cards = client.databases.query(
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

    def list_all_current(self, client: Client) -> List[Account]:
        return self._list_all(
            client=client,
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Corrente",
                },
            },
        )

    def list_all_investiment(self, client: Client) -> List[Account]:
        return self._list_all(
            client=client,
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Investimento",
                },
            },
        )

    def list_all_boxes(self, client: Client) -> List[Account]:
        return self._list_all(
            client=client,
            filter_dict={
                "property": "Tipo",
                "select": {
                    "equals": "Caixinha",
                },
            },
        )
