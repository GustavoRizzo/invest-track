from django.test import TestCase

from yahoo_finances.models import Company, DailyStockHistory

from ..scripts.load_all_company_info import main as load_all_company_info
from ..scripts.load_all_daily_stock_history import main as load_all_daily_stock_history
from ..models import StockPosition


class Test(TestCase):
    fixtures = ['stock_position.json',]

    def test_load_company_info(self):
        stock = StockPosition.objects.get(symbol="MGLU3")
        symbol_yahoo = stock.symbol_yahoo
        self.assertEqual(symbol_yahoo, "MGLU3.SA")
        stock.save()
        load_all_company_info()
        company = Company.objects.get(symbol=symbol_yahoo)
        self.assertEqual(company.symbol, symbol_yahoo)

    def test_load_all_daily_stock_history(self):
        stock = StockPosition.objects.get(symbol="MGLU3")
        start = '2024-01-01'
        end = '2024-01-07'
        load_all_daily_stock_history(start, end)
        daily_stock_history = DailyStockHistory.objects.filter(symbol=stock.symbol_yahoo)
        self.assertEqual(daily_stock_history.count(), 4)
