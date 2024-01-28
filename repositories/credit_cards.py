from typing import List

from notion_client import Client

from models.credit_card import CreditCard


class CreditCardRepository:
    def __init__(self, database_id: str, client: Client):
        self.db_id = database_id
        self.client = client
        self.parent = {
            "type": "database_id",
            "database_id": self.db_id,
        }

    def list_all(self) -> List[CreditCard]:
        cards = self.client.databases.query(
            database_id=self.db_id,
        ).get("results")

        return [
            CreditCard(
                id=card["id"],
                card_name=card["properties"]["Cartão"]["title"][0]["text"]["content"],
            )
            for card in cards
        ]
