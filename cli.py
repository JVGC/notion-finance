import os
from typing import Annotated, Literal, Optional

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


def get_category_choice(categories: list[Category]) -> str | None:
    categories.append(
        Category(id="No Category ID", name="No Category", color="", description="")
    )
    categories_names = [category.name for category in categories]
    questions = [
        List(
            "category",
            message="Select a category",
            choices=categories_names,
        )
    ]
    answers = prompt(questions)
    return answers["category"] if answers["category"] != "No Category" else None


def get_payment_method_choice() -> Literal["Debit", "Credit"]:
    payment_methods = ["Credit", "Debit"]
    questions = [
        List(
            "payment_method",
            message="Select a payment method",
            choices=payment_methods,
        )
    ]
    answers = prompt(questions)
    return answers["payment_method"]


def get_credit_card_choice(credit_cards: list[CreditCard]) -> str:
    cards_names = [card.card_name for card in credit_cards]
    questions = [
        List("credit_card", message="Select a Credit Card", choices=cards_names)
    ]
    answers = prompt(questions)
    return answers["credit_card"]


def get_account_choice(accounts: list[Account]) -> str:
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


@app.command(
    help="Create a new expense. It will ask for the expense name, cost, purchase date, category, payment method and credit card or account used to do it."
)
def create_expense(
    expense_name: Annotated[str, typer.Option(prompt="What's the expense?")],
    cost: Annotated[float, typer.Option(prompt="How much did it cost?")],
    payment_method="",
    account="",
    credit_card="",
):
    create_expense_use_case = CreateExpenseUseCase(
        expense_repository=expense_repo,
        account_repository=account_repo,
        credit_card_repository=credit_repo,
    )
    purchase_date = typer.prompt(
        "When did you buy it?", type=click.DateTime(formats=["%d/%m/%y"])
    )
    # Asking for category
    selected_category = get_category_choice(create_expense_use_case.categories)

    # Asking for payment method
    if not payment_method and not account and not credit_card:
        payment_method = get_payment_method_choice()

    if payment_method == "Credit" or credit_card:
        # Asking for credit card selection
        create_expense_use_case.load_credit_cards()
        selected_credit_card = credit_card
        if not credit_card:
            selected_credit_card = get_credit_card_choice(
                create_expense_use_case.credit_cards
            )
        created_url = create_expense_use_case.create(
            expense_name,
            cost,
            purchase_date,
            selected_category,
            None,
            selected_credit_card,
        )
        typer.echo("Expense created successfully!")
        typer.echo(
            f"Expense: {expense_name}, Cost: {cost}, Date: {purchase_date}, Category: {selected_category}, Credit Card: {selected_credit_card}"
        )
        typer.echo(f"Access the created page here: {created_url}")
    elif payment_method == "Debit" or account:
        # Asking for debit card selection
        create_expense_use_case.load_accounts()
        selected_account = account
        if not account:
            selected_account = get_account_choice(create_expense_use_case.accounts)
        created_url = create_expense_use_case.create(
            expense_name,
            cost,
            purchase_date,
            selected_category,
            selected_account,
            None,
        )
        typer.echo("Expense created successfully!")
        typer.echo(
            f"Expense: {expense_name}, Cost: {cost}, Date: {purchase_date}, Category: {selected_category}, Account: {selected_account}"
        )
        typer.echo(f"Access the created page here: {created_url}")
        # TODO Show link to access the created page
    else:
        typer.echo("Invalid payment method")
        return


@app.command()
def hello(name: Optional[str] = None):
    if name:
        typer.echo(f"Hello {name}")
    else:
        typer.echo("Hello World!")


if __name__ == "__main__":
    app()
