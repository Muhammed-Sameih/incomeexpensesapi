from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from rest_framework.permissions import IsAuthenticated
from expenses.permissions import IsOwner, IsVerified


class ExpenseSummaryStats(APIView):
    permission_classes = (IsAuthenticated, IsOwner, IsVerified)

    def get_amount_for_category(self, expenses_list, category):
        exps = expenses_list.filter(category=category)
        total_amount_of_maony = 0
        for exp in exps:
            total_amount_of_maony += exp.amount_of_money
        return {'total_amount_of_maony': str(total_amount_of_maony)}

    def get_final(self, expenses_list, categories):
        final = {}
        for expense in expenses_list:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    expenses_list, category)
        return final

    def get_category(self, expense: Expense):
        return expense.category

    def get(self, request: Request):
        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30*12)
        expenses_list = Expense.objects.filter(
            owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        categories = list(set(map(self.get_category, expenses_list)))
        final = {}
        final = self.get_final(expenses_list, categories)

        return Response({'category_data': final}, status=status.HTTP_200_OK)
