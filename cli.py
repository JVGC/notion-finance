from datetime import datetime
import os
from typing import Optional

import click
from dotenv import load_dotenv
from notion_client import Client
import typer
from inquirer import prompt, List
from models.account import Account
from models.credit_card import CreditCard
from models.expense import Category
from repositories.accounts import AccountRepository
from repositories.credit_cards import CreditCardRepository

from repositories.expenses import ExpenseRepository
from use_cases.expenses import CreateExpenseUseCase

app = typer.Typer()

load_dotenv()

client = Client(auth=os.environ["CLIENT_SECRET"])

expense_repo = ExpenseRepository(
    database_id=os.environ["EXPENSES_DB_ID"], client=client
)
credit_repo = CreditCardRepository(
    database_id=os.environ["CREDIT_DB_ID"], client=client
)
account_repo = AccountRepository(
    database_id=os.environ["ACCOUNTS_DB_ID"], client=client
)


def get_category_choice(categories: list[Category]):
    categories_names = [category.name for category in categories]
    questions = [
        List("category", message="Select a category:", choices=categories_names)
    ]
    answers = prompt(questions)
    return answers["category"]


def get_payment_method_choice():
    payment_methods = ["Credit", "Debit"]
    questions = [
        List(
            "payment_method",
            message="Select a payment method:",
            choices=payment_methods,
        )
    ]
    answers = prompt(questions)
    return answers["payment_method"]


def get_credit_card_choice(credit_cards: list[CreditCard]):
    cards_names = [card.card_name for card in credit_cards]
    questions = [
        List("credit_card", message="Select a Credit Card:", choices=cards_names)
    ]
    answers = prompt(questions)
    return answers["credit_card"]


def get_account_choice(accounts: list[Account]):
    accounts_names = [account.name for account in accounts]
    questions = [
        List(
            "account",
            message="Select a the Account used to do it:",
            choices=accounts_names,
        )
    ]
    answers = prompt(questions)
    return answers["account"]


@app.command()
def create_expense():
    create_expense_use_case = CreateExpenseUseCase(
        expense_repository=expense_repo,
        account_repository=account_repo,
        credit_card_repository=credit_repo,
    )
    expense_name = typer.prompt("What's the expense?")
    cost = typer.prompt("How much did it cost?", type=float)
    purchase_date: datetime = typer.prompt(
        "When did you buy it?", type=click.DateTime(formats=["%d/%m/%y"])
    )

    # Asking for category
    selected_category = get_category_choice(create_expense_use_case.categories)

    # Asking for payment method
    selected_payment_method = get_payment_method_choice()

    if selected_payment_method == "Credit":
        # Asking for credit card selection
        create_expense_use_case.load_credit_cards()
        selected_credit_card = get_credit_card_choice(
            create_expense_use_case.credit_cards
        )
        create_expense_use_case.create(
            expense_name,
            cost,
            purchase_date.date(),
            selected_category,
            None,
            selected_credit_card,
        )
    else:
        # Asking for debit card selection
        create_expense_use_case.load_accounts()
        selected_account = get_account_choice(create_expense_use_case.accounts)
        create_expense_use_case.create(
            expense_name,
            cost,
            purchase_date.date(),
            selected_category,
            selected_account,
            None,
        )
    typer.echo("Expense created successfully!")


@app.command()
def hello(name: Optional[str] = None):
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


if __name__ == "__main__":
    app()
