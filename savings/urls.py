from django.urls import path
from .views import AccountDetailView, DepositView, WithdrawView, TransactionHistoryView

urlpatterns = [
    path('account/', AccountDetailView.as_view(), name='account-detail'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transactions/', TransactionHistoryView.as_view(), name='transaction-history'),
]
