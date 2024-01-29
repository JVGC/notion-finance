from datetime import datetime, timezone
from typing import List, Optional
from models.account import Account
from models.credit_card import CreditCard
from models.expense import Category, Expense
from repositories.accounts import AccountRepository
from repositories.credit_cards import CreditCardRepository
from repositories.expenses import ExpenseRepository


class CreateExpenseUseCase:
    def __init__(
        self,
        expense_repository: ExpenseRepository,
        account_repository: AccountRepository,
        credit_card_repository: CreditCardRepository,
    ):
        self.expense_repository = expense_repository
        self.account_repository = account_repository
        self.credit_card_repository = credit_card_repository

        self._categories = self._load_category_options()
        self._credit_cards = []
        self._accounts = []

    def _load_category_options(self) -> List[Category]:
        return self.expense_repository.get_category_options()

    def load_credit_cards(self):
        self._credit_cards = self.credit_card_repository.list_all()

    def load_accounts(self, account_type: str = "current"):
        match account_type:
            case "current":
                self._accounts = self.account_repository.list_all_current()
            case "investiment":
                self._accounts = self.account_repository.list_all_investiment()
            case "box":
                self._accounts = self.account_repository.list_all_boxes()

    @property
    def categories(self) -> List[Category]:
        return self._categories

    @property
    def credit_cards(self) -> List[CreditCard]:
        return self._credit_cards

    @property
    def accounts(self) -> List[Account]:
        return self._accounts

    def create(
        self,
        name: str,
        amount: int | float,
        date: datetime,
        category_name: Optional[str],
        account_name: Optional[str],
        credit_card_name: Optional[str],
    ):
        category = None
        if category_name:
            category = next(
                filter(lambda category: category.name == category_name, self.categories)
            )
        if account_name:
            account = next(
                filter(lambda account: account.name == account_name, self.accounts)
            )
            self.expense_repository.create_expense(
                Expense(
                    title=name,
                    amount=amount,
                    date=date.astimezone(timezone.utc).isoformat(),
                    category=category.name if category else None,
                    account_id=account.id,
                    credit_card_id=None,
                )
            )

        if credit_card_name:
            credit_card = next(
                filter(
                    lambda card: card.card_name == credit_card_name, self.credit_cards
                )
            )
            self.expense_repository.create_expense(
                Expense(
                    title=name,
                    amount=amount,
                    date=date.astimezone(timezone.utc).isoformat(),
                    category=category.name if category else None,
                    credit_card_id=credit_card.id,
                    account_id=None,
                )
            )
