from booking.models import Account


def change_account_balance(account: Account, amount: float):
    account.balance += amount
    account.save()
