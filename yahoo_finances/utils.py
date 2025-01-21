from django.db.models import F
from datetime import date
from rest_framework.serializers import Serializer
from .models import Company
from .serializers import DateValueSerializer, StockHistorySerializer


def get_company_serializer_history_data(company: Company, start_date: date, end_date: date = date.today()) \
        -> tuple[Serializer, bool]:
    """
    Recive a Company object and return the close history for the company.
    Return:
        - serializer (Serializer): The close history for the company of type StockHistorySerializer, or an
        error message.
        - err (bool): True if there is an error, False otherwise.
    """
    assert isinstance(company, Company), f"company must be a Company object, not {type(company)}"
    try:
        queryset = company.close_history(start_date=start_date, end_date=end_date)
    except ValueError as e:
        return {'error': str(e)}, True
    # If queryset is empty, return history equal []
    if queryset.count() == 0:
        return StockHistorySerializer({'symbol': company.symbol, 'history': []}), False
    data_list = queryset.annotate(value=F('close')).values('date', 'value')
    data_value = DateValueSerializer(data_list, many=True)
    serializer_stock_history = StockHistorySerializer({'symbol': company.symbol, 'history': data_value.data})
    return serializer_stock_history, False


def get_company_serializer_normalized_history_data(company: Company, start_date: date, end_date: date = date.today()) \
     -> tuple[Serializer, bool]:
    """
    Recive a Company object and return the normalized close history for the company.
    Return:
        - serializer (Serializer): The normalized close history for the company of type StockHistorySerializer, or an
        error message.
        - err (bool): True if there is an error, False otherwise.
    """
    assert isinstance(company, Company), f"company must be a Company object, not {type(company)}"
    try:
        queryset = company.normalized_close_history(start_date=start_date, end_date=end_date)
    except ValueError as e:
        return {'error': str(e)}, True
    # If queryset is empty, return history equal []
    if queryset.count() == 0:
        return StockHistorySerializer({'symbol': company.symbol, 'history': []}), False
    data_list = queryset.annotate(value=F('normalized_close')).values('date', 'value')
    data_value = DateValueSerializer(data_list, many=True)
    serializer_stock_history = StockHistorySerializer({'symbol': company.symbol, 'history': data_value.data})
    return serializer_stock_history, False
