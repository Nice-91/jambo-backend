from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import SavingsAccount, Transaction
from .serializers import SavingsAccountSerializer, TransactionSerializer


class AccountDetailView(generics.RetrieveAPIView):
    serializer_class = SavingsAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        account, _ = SavingsAccount.objects.get_or_create(user=self.request.user)
        return account


class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description', '')

        if not amount or float(amount) <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        account, _ = SavingsAccount.objects.get_or_create(user=request.user)
        account.balance += float(amount)
        account.save()

        transaction = Transaction.objects.create(account=account, transaction_type='deposit', amount=amount, description=description)
        return Response({"balance": account.balance, "transaction": TransactionSerializer(transaction).data})


class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = request.data.get('amount')
        description = request.data.get('description', '')

        if not amount or float(amount) <= 0:
            return Response({"error": "Amount must be greater than 0"}, status=status.HTTP_400_BAD_REQUEST)

        account, _ = SavingsAccount.objects.get_or_create(user=request.user)
        if account.balance < float(amount):
            return Response({"error": "Insufficient balance"}, status=status.HTTP_400_BAD_REQUEST)

        account.balance -= float(amount)
        account.save()

        transaction = Transaction.objects.create(account=account, transaction_type='withdraw', amount=amount, description=description)
        return Response({"balance": account.balance, "transaction": TransactionSerializer(transaction).data})


class TransactionHistoryView(generics.ListAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        account, _ = SavingsAccount.objects.get_or_create(user=self.request.user)
        return account.transactions.all().order_by('-timestamp')
