from django.contrib import admin
from .models import SavingsAccount, Transaction

# -----------------------------
# Savings Account Admin
# -----------------------------
@admin.register(SavingsAccount)
class SavingsAccountAdmin(admin.ModelAdmin):
    list_display = ('user', 'balance', 'created_at', 'updated_at')
    readonly_fields = ('created_at', 'updated_at')
    search_fields = ('user__email',)

# -----------------------------
# Transaction Admin
# -----------------------------
@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('account', 'transaction_type', 'amount', 'timestamp', 'description')
    readonly_fields = ('timestamp',)
    search_fields = ('account__user__email',)
    list_filter = ('transaction_type',)
