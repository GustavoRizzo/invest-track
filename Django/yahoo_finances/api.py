import logging
import yfinance as yf

from datetime import datetime
from pytz import timezone
from django.core.exceptions import ValidationError
from django.db import IntegrityError

from .models import Company


logger = logging.getLogger(__name__)


def convert_epoch_to_datetime(epoch_utc: int, timezone_name: str) -> datetime:
    # Convert epoch to datetime
    date = datetime.fromtimestamp(epoch_utc, tz=timezone(timezone_name))
    return date


def convert_yahoo_date_to_Company(date: dict) -> Company:
    # try to get symbol, if none rasie error
    symbol = date.get('symbol', None)
    assert symbol is not None, "Symbol is required"
    # try to get first_trade_date_epoch_utc, if none rasie error
    epoch_utc = date.get('firstTradeDateEpochUtc', None)
    time_zone_full_name = date.get('timeZoneFullName', '')
    first_trade_date_epoch_utc = convert_epoch_to_datetime(epoch_utc, time_zone_full_name)
    assert first_trade_date_epoch_utc is not None, "first_trade_date_epoch_utc is required"
    # Return Company
    return Company(
        currency=date.get('currency', ''),
        city=date.get('city', ''),
        state=date.get('state', ''),
        country=date.get('country', ''),
        website=date.get('website', ''),
        industry=date.get('industry', ''),
        industry_key=date.get('industryKey', ''),
        industry_disp=date.get('industryDisp', ''),
        sector=date.get('sector', ''),
        sector_key=date.get('sectorKey', ''),
        exchange=date.get('exchange', ''),
        quote_type=date.get('quoteType', ''),
        symbol=symbol,
        underlying_symbol=date.get('underlyingSymbol', ''),
        short_name=date.get('shortName', ''),
        long_name=date.get('longName', ''),
        first_trade_date_epoch_utc=first_trade_date_epoch_utc,
        time_zone_full_name=time_zone_full_name,
        time_zone_short_name=date.get('timeZoneShortName', ''),
        financial_currency=date.get('financialCurrency', ''),
        long_business_summary=date.get('longBusinessSummary', ''),
    )


def fetch_company_data(symbol: str) -> Company:
    # Fetch data from Yahoo Finance
    ticker = yf.Ticker(symbol)
    data = ticker.info
    return convert_yahoo_date_to_Company(data)


def fetch_and_save_company_data(symbol: str) -> Company:
    # Fetch data from Yahoo Finance
    company = fetch_company_data(symbol)
    symbol = company.symbol
    # Check Company already exists on db, if exist delete and create again
    try:
        old_company = Company.objects.get(symbol=symbol)
        logger.info(f"Company {symbol} already exists, deleting and creating again")
        old_company.delete()
    except Company.DoesNotExist:
        pass

    # Save
    company.save()
    return company
