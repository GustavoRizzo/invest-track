import datetime
import json

from django.http import HttpResponse
from django.shortcuts import render
from django.utils import timezone

from .utils import get_my_position_stock_normalized

from yahoo_finances.serializers import NormalizedCloseSerializer
from ativa_investimentos.models import StockPosition
from yahoo_finances.models import DailyStockHistory


def home(request):
    return render(request, 'pages/home.html')


def current_datetime(request):
    now = datetime.datetime.now()
    html = """<html><title>Current Time</title><body>It is now %s.</body><style>body {background-color: #637ed6;}
        </style></html>""" % now
    return HttpResponse(html)


def stock_quote(request):
    # Get all Symbols form StockPosition
    stock_positions = StockPosition.objects.all()
    symbols = [stock.symbol_yahoo for stock in stock_positions]
    # Get date 6 months ago
    six_months_ago = datetime.date.today() - timezone.timedelta(days=183)
    formatted_date = six_months_ago.strftime("%Y-%m-%d")
    # Get DailyStockHistory for each symbol
    stocks = []
    for symbol in symbols:
        stock_history = DailyStockHistory.objects.get_normalized_close(
            symbol=symbol, start_date=formatted_date).order_by('date')
        stocks.append({'symbol': symbol, 'stock_history': stock_history})
    # Using line chart JS
    stock_history = get_my_position_stock_normalized()
    return render(request, 'pages/stock_quote.html', {'stocks': stocks, 'stock_history': json.dumps(stock_history)})


def companies(request):
    return render(request, 'pages/companies.html')
