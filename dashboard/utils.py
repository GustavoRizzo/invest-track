import datetime

from django.db.models import F
from django.utils import timezone

from ativa_investimentos.models import StockPosition
from yahoo_finances.models import DailyStockHistory
from yahoo_finances.serializers import DateValueSerializer, NormalizedCloseSerializer, StockHistorySerializer


def get_my_position_stock_normalized() -> dict:
    """
    Get the normalized close price for each stock in the user's position.
    return a list of StockHistorySerializer(many=True)
    """
    # Get all Symbols form StockPosition
    stock_positions = StockPosition.objects.all()
    symbols = [stock.symbol_yahoo for stock in stock_positions]
    # Get date 6 months ago
    six_months_ago = datetime.date.today() - timezone.timedelta(days=183)
    formatted_date = six_months_ago.strftime("%Y-%m-%d")
    # Get DailyStockHistory for each symbol
    list_stock_history = []
    for symbol in symbols:
        queryset_normalized = DailyStockHistory.objects.get_normalized_close(
            symbol=symbol,
            start_date=formatted_date
            ).order_by('date')
        if queryset_normalized:
            list = queryset_normalized.annotate(value=F('normalized_close')).values('date', 'value')
            date_value = DateValueSerializer(list, many=True)
            data = {'symbol': symbol, 'history': date_value.data}
            list_stock_history.append(data)
    serializer = StockHistorySerializer(list_stock_history, many=True)
    return serializer.data
