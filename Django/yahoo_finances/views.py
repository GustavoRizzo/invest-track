from django.shortcuts import render, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import Company, DailyStockHistory
from .serializers import DailyStockHistorySerializer


class DailyStockHistoryViewSet(ModelViewSet):
    queryset = DailyStockHistory.objects.all()
    serializer_class = DailyStockHistorySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']


def company_details(request, company_id):
    # Get the Company object
    company = get_object_or_404(Company, pk=company_id)
    # Get the DailyStockHistory for the Company
    stock_history = DailyStockHistory.objects.filter(symbol=company.symbol)
    return render(request, 'company_details.html', {'company': company, 'stock_history': stock_history})


def multiple_companies(request):
    # Symbols
    symbols = ['VALE3.SA', 'ASAI3.SA', 'PETR4.SA', 'MGLU3.SA']
    # Get DailyStockHistory for each symbol
    companies = []
    for symbol in symbols:
        stock_history = DailyStockHistory.objects.filter(symbol=symbol, date__gte='2024-01-01')
        companies.append({'symbol': symbol, 'stock_history': stock_history})
    return render(request, 'multiple_companies.html', {'companies': companies})


def multiple_normalized_companies(request):
    # Symbols
    symbols = ['VALE3.SA', 'ASAI3.SA', 'PETR4.SA', 'MGLU3.SA']
    # Get DailyStockHistory for each symbol
    stocks = []
    for symbol in symbols:
        stock_history = DailyStockHistory.objects.get_normalized_close('2024-01-01', symbol)
        stocks.append({'symbol': symbol, 'stock_history': stock_history})
    return render(request, 'multiple_normalized_companies.html', {'stocks': stocks})
