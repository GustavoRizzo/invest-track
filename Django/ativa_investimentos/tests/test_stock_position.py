from django.test import TestCase

from yahoo_finances.models import Company

from ..scripts.load_all_company_info import main as load_all_company_info
from ..models import StockPosition


class Test(TestCase):

    def test_load_company_info(self):
        stock = StockPosition(symbol="PETR4", quantity=10)
        symbol_yahoo = stock.symbol_yahoo
        self.assertEqual(symbol_yahoo, "PETR4.SA")
        stock.save()
        load_all_company_info()
        company = Company.objects.get(symbol=symbol_yahoo)
        self.assertEqual(company.symbol, symbol_yahoo)
