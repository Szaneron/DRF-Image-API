from rest_framework import viewsets
from rest_framework.permissions import IsAdminUser
from .models import Account, AccountTier
from .serializers import AccountSerializer, AccountTierSerializer


class AccountViewSet(viewsets.ModelViewSet):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer


class AccountTierViewSet(viewsets.ModelViewSet):
    queryset = AccountTier.objects.all()
    serializer_class = AccountTierSerializer
    permission_classes = [IsAdminUser]
