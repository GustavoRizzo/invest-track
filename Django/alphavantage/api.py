import requests

from core.settings import ALPHAVANTAGE_API_KEY, URL_BASE_ALPHAVANTAGE


def get_stock_data(symbol):

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'apikey': ALPHAVANTAGE_API_KEY,
    }

    url = requests.Request('GET', URL_BASE_ALPHAVANTAGE, params=params).prepare().url
    response = requests.get(url)
    data = response.json()

    return data
