
from datetime import datetime
from django.test import TestCase


from ..api import fetch_and_save_company_data, fetch_and_save_stock_history, fetch_company_data, convert_epoch_to_datetime, fetch_stock_history
from ..models import Company, DailyStockHistory


class Test(TestCase):

    def test_convert_epoch_to_datetime(self):
        # Arrange
        vale3sa_dict = {
            'firstTradeDateEpochUtc': 946900800,
            'timeZoneFullName': 'America/Sao_Paulo',
        }
        epoch_utc = vale3sa_dict['firstTradeDateEpochUtc']
        timezone_name = vale3sa_dict['timeZoneFullName']
        # Act
        date = convert_epoch_to_datetime(epoch_utc, timezone_name)
        # Assert
        self.assertIsInstance(date, datetime)
        self.assertEqual(date.year, 2000)
        self.assertEqual(date.month, 1)
        self.assertEqual(date.day, 3)

    def test_fetch_and_save_company_data_real_touch_api(self):
        # Arrange
        symbol = 'PETR4.SA'
        # Act
        company = fetch_and_save_company_data(symbol)
        # Assert
        self.assertIsInstance(company, Company)
        self.assertEqual(company.symbol, symbol)

    def test_fetch_and_save_company_data_if_Company_already_exists_update(self):
        # Arrange
        symbol = 'PETR4.SA'
        # Act (save firt time)
        company = fetch_and_save_company_data(symbol)
        # Assert
        self.assertEqual(company.country, 'Brazil')
        # Act 2 (change country, and fecth again)
        company.country = 'fake country'
        company.save()
        _ = fetch_and_save_company_data(symbol)
        company = Company.objects.get(symbol=symbol)
        # Assert
        self.assertNotEqual(company.country, 'fake country')

    def test_fetch_stock_history(self):
        # Arrange
        symbol = 'PETR4.SA'
        start = '2024-01-01'
        end = '2024-01-07'
        # Act
        hist = fetch_stock_history(symbol, start, end)
        # Assert
        daily_stock_history = hist[0]
        self.assertIsInstance(daily_stock_history, DailyStockHistory)
        self.assertEqual(daily_stock_history.symbol, symbol)
        self.assertEqual(daily_stock_history.date.year, 2024)
        self.assertEqual(daily_stock_history.date.month, 1)
        self.assertEqual(daily_stock_history.date.day, 2)

    def test_fetch_and_save_stock_history(self):
        # Arrange
        symbol = 'PETR4.SA'
        start = '2024-01-01'
        end = '2024-01-07'
        # Act
        hist = fetch_and_save_stock_history(symbol, start, end)
        # Assert
        self.assertEqual(len(hist), 4)
        # Arrange 2
        end = '2024-01-05'
        # Act 2
        hist = fetch_and_save_stock_history(symbol, start, end)
        hist_compete = DailyStockHistory.objects.filter(symbol=symbol)
        # Assert 2
        self.assertEqual(len(hist), 3)
        self.assertEqual(len(hist_compete), 4)
