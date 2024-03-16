import datetime

from django.utils import timezone
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .scripts.load_all_company_info import main as load_all_company_info
from .scripts.load_all_daily_stock_history import main as load_all_daily_stock_history


class LoadDataAPIView(APIView):
    def post(self, request, format=None):
        # Update Company Info
        load_all_company_info()
        # Get date 6 months ago
        six_months_ago = (datetime.date.today() - timezone.timedelta(days=183)).strftime("%Y-%m-%d")
        today = datetime.date.today().strftime("%Y-%m-%d")
        # Update Daily Stock History
        load_all_daily_stock_history(start_date=six_months_ago, end_date=today)
        msg = "Data loaded successfully"
        return Response(msg, status=status.HTTP_200_OK)
