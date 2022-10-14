from booking.models import Transaction
from .account import change_account_balance


def process_transaction(transaction: Transaction):
    change_account_balance(transaction.account, transaction.amount)
