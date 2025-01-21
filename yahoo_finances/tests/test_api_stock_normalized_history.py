from datetime import date, timedelta
from ..models import Company, DailyStockHistory
from core.base.test import BaseAPITestCase
from rest_framework import status


class ApiStockNormalizedHistoryTest(BaseAPITestCase):

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
            'symbols': ['PETR4.SA']
        }
        self.client.force_authenticate(user=self.test_user)
        # Act 1
        response1 = self.client.post(self.url_stock_normalized_history, data)
        # Assert 1
        self.assertEqual(response1.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_data(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': [company.symbol]
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        stock_history = response.data[0]
        self.assertEqual(stock_history['symbol'], company.symbol)
        self.assertEqual(len(stock_history['history']), 10)

    def test_get_data_without_history(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company = self.create_company(symbol='PETR4.SA')
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': [company.symbol]
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        stock_history = response.data[0]
        self.assertEqual(stock_history['symbol'], company.symbol)
        self.assertEqual(len(stock_history['history']), 0)

    def test_get_data_of_two_symbols(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company1 = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        company2 = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': [company1.symbol, company2.symbol]
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # get stock history of company1
        stock_history1 = response.data[0] if response.data[0]['symbol'] == company1.symbol else response.data[1]
        self.assertEqual(stock_history1['symbol'], company1.symbol)
        self.assertEqual(len(stock_history1['history']), 10)
        stock_history2 = response.data[0] if response.data[0]['symbol'] == company2.symbol else response.data[1]
        self.assertEqual(stock_history2['symbol'], company2.symbol)
        self.assertEqual(len(stock_history2['history']), 10)

    def test_get_data_of_two_symbols_with_diff_hist_lenght(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company1 = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        company2 = self.create_company_with_stock_history(start_date=start_date, end_date=end_date - timedelta(days=1))
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': [company1.symbol, company2.symbol]
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        # get stock history of company1
        stock_history1 = response.data[0] if response.data[0]['symbol'] == company1.symbol else response.data[1]
        self.assertEqual(stock_history1['symbol'], company1.symbol)
        self.assertEqual(len(stock_history1['history']), 10)
        stock_history2 = response.data[0] if response.data[0]['symbol'] == company2.symbol else response.data[1]
        self.assertEqual(stock_history2['symbol'], company2.symbol)
        self.assertEqual(len(stock_history2['history']), 9)

    def test_error_if_symbol_not_exist(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': ['PETR4.SA']
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_error_if_one_of_symbols_not_exist(self):
        # Arrange
        start_date = date(2024, 1, 1)
        end_date = date(2024, 1, 10)
        company = self.create_company_with_stock_history(start_date=start_date, end_date=end_date)
        data = {
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'symbols': [company.symbol, 'PETR4.SA']
        }
        self.client.force_authenticate(user=self.test_user)
        # Act
        response = self.client.post(self.url_stock_normalized_history, data)
        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
