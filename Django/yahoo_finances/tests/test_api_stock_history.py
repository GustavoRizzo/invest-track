from datetime import date
from ..models import Company, DailyStockHistory
from core.base.test import BaseAPITestCase
from rest_framework import status


class ApiStockHistoryTest(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        super().setUpTestData()

    def setUp(self):
        # Delete all data from Company and DailyStock
        Company.objects.all().delete()
        DailyStockHistory.objects.all().delete()

    def test_no_content(self):
        # Arrange 1 - Call API without any data       
        data = {
            'start_date': '2024-01-01',
            'symbol': 'PETR4.SA'
        }
        self.client.force_authenticate(user=self.test_user)
        # Act 1
        response1 = self.client.post(self.url_stock_history, data)
        # Assert 1
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)

    def test_get_data(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbol': company.symbol
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['symbol'], company.symbol)
        self.assertEqual(len(response.data['history']), 10)
