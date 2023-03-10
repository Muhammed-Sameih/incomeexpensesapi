from rest_framework import generics

from incomes.models import Income
from .serializers import IncomeSerializer
from expenses.permissions import IsOwner, IsVerified
from rest_framework.permissions import IsAuthenticated
# Create your views here.


class IncomesListAPIView(generics.ListCreateAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, ]

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.id)


class IncomeDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = IncomeSerializer
    queryset = Income.objects.all()
    permission_classes = [IsAuthenticated, IsOwner, IsVerified]
    lookup_field = "id"

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.id)
