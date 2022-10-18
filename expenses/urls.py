from .views import ExpenseDetailAPIView, ExpensesListAPIView
from django.urls import path
from .views import ExpenseDetailAPIView, ExpensesListAPIView
urlpatterns = [
    path('', ExpensesListAPIView.as_view(), name='expenseslist'),
    path('<int:pk>', ExpenseDetailAPIView.as_view(),
         name='expensedetail'),
]
