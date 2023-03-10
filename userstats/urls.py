from .views import ExpenseSummaryStats, IncomeSummaryStats
from django.urls import path
urlpatterns = [
    path('expense-category-data/', ExpenseSummaryStats.as_view(),
         name='expense-category-data'),
    path('income-category-data/', IncomeSummaryStats.as_view(),
         name='income-category-data'),
]
