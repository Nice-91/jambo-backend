from savings.models import SavingsAccount, Transaction
from decimal import Decimal


# Deposit

def deposit(user, amount, description="Deposit"):
    account, _ = SavingsAccount.objects.get_or_create(user=user)
    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("Deposit amount must be positive")

    account.deposit(amount)

    transaction = Transaction.objects.create(
        account=account,
        transaction_type=Transaction.DEPOSIT,
        amount=amount,
        description=description
    )
    return account, transaction


# -----------------------------
# Withdraw
# -----------------------------
def withdraw(user, amount, description="Withdrawal"):
    account, _ = SavingsAccount.objects.get_or_create(user=user)
    amount = Decimal(amount)
    if amount <= 0:
        raise ValueError("Withdrawal amount must be positive")
    if amount > account.balance:
        raise ValueError("Insufficient balance")

    account.withdraw(amount)

    transaction = Transaction.objects.create(
        account=account,
        transaction_type=Transaction.WITHDRAWAL,
        amount=amount,
        description=description
    )
    return account, transaction


# -----------------------------
# View Balance & Transaction History
# -----------------------------
def get_account_info(user):
    account, _ = SavingsAccount.objects.get_or_create(user=user)
    transactions = account.transactions.all()
    return account, transactions
