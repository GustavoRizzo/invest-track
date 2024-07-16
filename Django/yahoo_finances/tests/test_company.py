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

    def test_close_history_method(self):
        # Arrange 1
        company = self.create_company()
        daily_stock_history = self.create_daily_stock_history(symbol=company.symbol)
        # Act 1
        hist = company.close_history(start_date=daily_stock_history.date, end_date=daily_stock_history.date)
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
        hist2 = company2.close_history(start_date=date(2024, 1, 1), end_date=date(2024, 1, 10))
        # Assert 2
        self.assertEqual(hist2.count(), 10)
        self.assertEqual(hist2.first().symbol, company2.symbol)
        self.assertEqual(hist2.first().date, date(2024, 1, 1))
        self.assertEqual(hist2.last().symbol, company2.symbol)
        self.assertEqual(hist2.last().date, date(2024, 1, 10))
        # Act 3 - geting only 8 days 
        hist3 = company2.close_history(start_date=date(2024, 1, 2), end_date=date(2024, 1, 9))
        # Assert 3
        self.assertEqual(hist3.count(), 8)
        self.assertEqual(hist3.first().symbol, company2.symbol)
        self.assertEqual(hist3.first().date, date(2024, 1, 2))
        self.assertEqual(hist3.last().symbol, company2.symbol)
        self.assertEqual(hist3.last().date, date(2024, 1, 9))
        # Act 4 - out of range, will return only the results that are in the range
        hist4 = company2.close_history(start_date=date(2024, 1, 1), end_date=date(2024, 1, 11))
        # Assert 4
        self.assertEqual(hist4.count(), 10)
        self.assertEqual(hist4.first().symbol, company2.symbol)
        self.assertEqual(hist4.first().date, date(2024, 1, 1))
        self.assertEqual(hist4.last().symbol, company2.symbol)
        self.assertEqual(hist4.last().date, date(2024, 1, 10))
        # Act 5 - totally out of range, will return an empty queryset
        hist5 = company2.close_history(start_date=date(2024, 1, 11), end_date=date(2024, 1, 12))
        # Assert 5
        self.assertEqual(hist5.count(), 0)

    def test_normalized_close_history_method(self):
        # Arrange 1
        date1 = date(2024, 1, 1)
        date2 = date(2024, 1, 10)
        company = self.create_company_with_stock_history(
            symbol=self.fake.word(),
            start_date=date1,
            end_date=date2
        )
        hist = company.close_history(start_date=date1, end_date=date2)
        first_record = hist.first()
        last_record = hist.last()
        # Changing values
        first_record.close = 1
        first_record.save()
        last_record.close = 2
        last_record.save()
        # Act 1
        hist_normalized = company.normalized_close_history(start_date=date1, end_date=date2)
        # Assert 1
        self.assertEqual(hist_normalized.count(), 10)
        self.assertEqual(hist_normalized.first().symbol, company.symbol)
        self.assertEqual(hist_normalized.first().normalized_close, 100)
        self.assertEqual(hist_normalized.last().normalized_close, 200)
