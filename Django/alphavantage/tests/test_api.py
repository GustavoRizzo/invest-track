from django.test import TestCase
from unittest.mock import patch, MagicMock

from ..api import get_time_serie_daily_stock, save_time_serie_daily_stock
from .data.time_serie_daily import TIME_SERIE_DAILY_MOCK


class Test(TestCase):

    @patch('requests.get')
    def test_get_time_serie_daily_stock(self, mock_requests_get):
        # Mocking the response
        mock_requests_get.return_value = MagicMock(json=lambda: TIME_SERIE_DAILY_MOCK)#
        # Arrange
        symbol = 'ITUB4.SA'
        # Act
        data = get_time_serie_daily_stock(symbol)
        # Assert
        self.assertEqual(data, TIME_SERIE_DAILY_MOCK)
        mock_requests_get.assert_called_once()
        symbol_data = data.get('Meta Data', {}).get('2. Symbol', None)
        self.assertEqual(symbol_data, symbol)
        time_series = data.get('Time Series (Daily)', None)
        self.assertIsNotNone(time_series)
        self.assertIsInstance(time_series, dict)
        self.assertGreater(len(time_series), 0)
        self.assertIsInstance(list(time_series.keys())[0], str)
        # Get dict from first key
        values = time_series[list(time_series.keys())[0]]
        self.assertIsInstance(values, dict)
        # Check has properties
        self.assertIn('1. open', values)
        self.assertIn('2. high', values)
        self.assertIn('3. low', values)
        self.assertIn('4. close', values)
        self.assertIn('5. volume', values)
        # Check values could be converted to float
        self.assertIsInstance(float(values['1. open']), float)
        self.assertIsInstance(float(values['2. high']), float)
        self.assertIsInstance(float(values['3. low']), float)
        self.assertIsInstance(float(values['4. close']), float)
        self.assertIsInstance(float(values['5. volume']), float)

