from django.urls import path
from .views import IncomeDetailAPIView, IncomesListAPIView
urlpatterns = [
    path('', IncomesListAPIView.as_view(), name='incomeslist'),
    path('<int:pk>', IncomeDetailAPIView.as_view(),
         name='incomedetail'),
]
