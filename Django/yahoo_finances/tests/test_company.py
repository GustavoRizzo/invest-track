from datetime import date
from ..models import Company, DailyStockHistory
from core.base.test import BaseAPITestCase
from rest_framework import status


class CompanyTest(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        super().setUpTestData()

    def setUp(self):
        # Delete all data from Company and DailyStock
        Company.objects.all().delete()
        DailyStockHistory.objects.all().delete()

    def test_no_data(self):
        # Arrange 1
        company = self.create_company()
        daily_stock_history = self.create_daily_stock_history(symbol=company.symbol)
        # Act 1
        hist = company.close_history(start_date=daily_stock_history.date)
        # Assert 1
        self.assertEqual(hist.count(), 1)
        self.assertEqual(hist.first().close, daily_stock_history.close)
        self.assertEqual(hist.first().symbol, daily_stock_history.symbol)
        self.assertEqual(hist.first().date, daily_stock_history.date)
        # Arrange 2 - using create_company_with_stock_history
        company2 = self.create_company_with_stock_history(
            symbol=self.fake.word(),
            start_date=date(2024, 1, 1),
            end_date=date(2024, 1, 10)
        )
        # Act 2
        hist2 = company2.close_history(start_date=date(2024, 1, 1))
        # Assert 2
        self.assertEqual(hist2.count(), 10)
        self.assertEqual(hist2.first().symbol, company2.symbol)
        self.assertEqual(hist2.first().date, date(2024, 1, 1))
        self.assertEqual(hist2.last().symbol, company2.symbol)
        self.assertEqual(hist2.last().date, date(2024, 1, 10))
