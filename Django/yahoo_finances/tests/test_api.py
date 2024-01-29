
from datetime import datetime
from django.test import TestCase


from ..api import fetch_and_save_company_data, fetch_company_data, convert_epoch_to_datetime
from ..models import Company


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
