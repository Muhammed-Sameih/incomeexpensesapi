from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
import datetime
from expenses.models import Expense
from incomes.models import Income
from rest_framework.permissions import IsAuthenticated
from expenses.permissions import IsOwner, IsVerified


class ExpenseSummaryStats(APIView):
    permission_classes = (IsAuthenticated, IsOwner, IsVerified)

    def get_category(self, financial_ele):
        return financial_ele.category

    def get_amount_for_category(self, financial_list, category):
        fin_list = financial_list.filter(category=category)
        total_amount_of_maony = 0
        for fin_ele in fin_list:
            total_amount_of_maony += fin_ele.amount_of_money
        return {'total_amount_of_maony': str(total_amount_of_maony)}

    def get_final(self, financial_list, categories):
        final = {}
        for fin_ele in financial_list:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    financial_list, category)
        return final

    def get(self, request: Request):
        """
        GET method
        Send an expenses summary Statistices for particular user 
        """
        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30*12)
        expenses_list = Expense.objects.filter(
            owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        categories = list(set(map(self.get_category, expenses_list)))
        final = {}
        final = self.get_final(
            financial_list=expenses_list, categories=categories)

        return Response({'category_data': final}, status=status.HTTP_200_OK)


class IncomeSummaryStats(APIView):
    permission_classes = (IsAuthenticated, IsOwner, IsVerified)

    def get_category(self, financial_ele):
        return financial_ele.category

    def get_amount_for_category(self, financial_list, category):
        fin_list = financial_list.filter(category=category)
        total_amount_of_maony = 0
        for fin_ele in fin_list:
            total_amount_of_maony += fin_ele.amount_of_money
        return {'total_amount_of_maony': str(total_amount_of_maony)}

    def get_final(self, financial_list, categories):
        final = {}
        for fin_ele in financial_list:
            for category in categories:
                final[category] = self.get_amount_for_category(
                    financial_list, category)
        return final

    def get(self, request: Request):
        """
        GET method
        Send an incomes summary Statistices for particular user 
        """
        todays_date = datetime.date.today()
        ayear_ago = todays_date - datetime.timedelta(days=30*12)
        incomes_list = Income.objects.filter(
            owner=request.user, date__gte=ayear_ago, date__lte=todays_date)
        categories = list(set(map(self.get_category, incomes_list)))
        final = {}
        final = self.get_final(incomes_list, categories)

        return Response({'category_data': final}, status=status.HTTP_200_OK)
