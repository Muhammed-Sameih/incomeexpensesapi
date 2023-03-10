from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from expenses.models import Expense
from .serializers import ExpenseSerializer
from .permissions import IsOwner, IsVerified
from rest_framework.permissions import IsAuthenticated


class ExpenseListAPIView(ListCreateAPIView):
    serializer_class = ExpenseSerializer
    queryset = Expense.objects.all()
    permission_classes = (IsAuthenticated,)

    def perform_create(self, serializer):
        return serializer.save(owner=self.request.user)

    def get_queryset(self):
        return self.queryset.filter(owner=self.request.user.id)


class ExpenseDetailAPIView(RetrieveUpdateDestroyAPIView):
    serializer_class = ExpenseSerializer
    permission_classes = (IsAuthenticated, IsOwner, IsVerified)
    queryset = Expense.objects.all()

    def get_queryset(self):
        print(type(self.request.user))
        return self.queryset.filter(owner=self.request.user)
