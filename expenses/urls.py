from .views import ExpenseDetailAPIView, ExpenseListAPIView
from django.urls import path
urlpatterns = [
    path('', ExpenseListAPIView.as_view(), name='expenseslist'),
    path('<int:pk>', ExpenseDetailAPIView.as_view(),
         name='expensedetail'),
]
