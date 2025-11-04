from django.db import models
from accounts.models import User


class SavingsAccount(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='savings_account')
    balance = models.FloatField(default=0.0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.email} - Balance: {self.balance}"


class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('deposit', 'Deposit'),
        ('withdraw', 'Withdraw'),
    )

    account = models.ForeignKey(SavingsAccount, on_delete=models.CASCADE, related_name='transactions')
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.FloatField()
    description = models.CharField(max_length=255, blank=True, default="")
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.account.user.email} - {self.transaction_type} - {self.amount}"
