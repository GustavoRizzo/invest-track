import requests

from core.settings import ALPHAVANTAGE_API_KEY


def get_stock_data(symbol):
    base_url = 'https://www.alphavantage.co/query'

    params = {
        'function': 'TIME_SERIES_DAILY',
        'symbol': symbol,
        'outputsize': 'full',
        'apikey': ALPHAVANTAGE_API_KEY,
    }

    url = requests.Request('GET', base_url, params=params).prepare().url
    response = requests.get(url)
    data = response.json()

    return data
