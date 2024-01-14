from typing import Optional
import requests
from .models import DailyStockPrices

from core.settings import ALPHAVANTAGE_API_KEY, URL_BASE_ALPHAVANTAGE


def get_time_serie_daily_stock(symbol: str, outputsize: Optional[str] = 'full') -> dict:

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': outputsize,
        'apikey': ALPHAVANTAGE_API_KEY,
    }

    url = requests.Request('GET', URL_BASE_ALPHAVANTAGE, params=params).prepare().url
    response = requests.get(url)
    data = response.json()

    return data


def deserializer_time_serie_daily_stock(data: dict) -> list:
    time_series = data.get('Time Series (Daily)', None)
    list_data = [
        {
            'date': date,
            'closing_price': float(values['4. close']),
        }
        for date, values in time_series.items()
    ]
    return list_data


def save_time_serie_daily_stock(symbol, outputsize='full'):
    # Get date from API
    data = get_time_serie_daily_stock(symbol, outputsize=outputsize)
    # Deserialize data
    list_data = deserializer_time_serie_daily_stock(data)
    symbol = data.get('Meta Data', {}).get('2. Symbol', None)
    # Get list of dates already saved
    list_already_saved = DailyStockPrices.days_with_prices_for_symbol(symbol)
    list_already_saved = [str(date) for date in list_already_saved]
    # Save data
    for data in list_data:
        # Not save if already exists on db
        if data['date'] not in list_already_saved:
            daily_stock = DailyStockPrices(symbol=symbol, **data)
            daily_stock.save()
