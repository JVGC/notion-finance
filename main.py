from datetime import datetime
import os
from notion_client import Client
from dotenv import load_dotenv
from models.expense import Expense
from repositories.accounts import AccountRepository
from repositories.credit_cards import CreditCardRepository

from repositories.expenses import ExpenseRepository

load_dotenv()


def main():
    client = Client(auth=os.environ["CLIENT_SECRET"])
    expense_repo = ExpenseRepository(database_id=os.environ["EXPENSES_DB_ID"])
    credit_repo = CreditCardRepository(database_id=os.environ["CREDIT_DB_ID"])

    account_repo = AccountRepository(database_id=os.environ["ACCOUNTS_DB_ID"])
    credit_cards = credit_repo.list_all(client=client)
    print(credit_cards[0].card_name)

    accounts = account_repo.list_all_current(client=client)
    print(accounts)

    categories = expense_repo.get_category_options(client=client)
    print(categories[0].color)
    expense_repo.create_expense(
        Expense(
            title="Teste",
            amount=100.0,
            category=categories[0].name,
            date=datetime.now().date(),
            credit_card_id=None,
            debit=accounts[0].id,
        ),
        client=client,
    )


if __name__ == "__main__":
    main()
