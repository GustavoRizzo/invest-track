
from datetime import datetime
from yahoo_finances.api import fetch_and_save_stock_history
from ..models import StockPosition


def main(start_date: datetime, end_date: datetime):
    # Validate start and end date
    assert start_date is not None, "Start date is required"
    assert end_date is not None, "End date is required"
    # Load all StockPosition
    stock_positions = StockPosition.objects.all()
    for stock_position in stock_positions:
        print(f"\nLoading company info for {stock_position.symbol_yahoo}")
        fetch_and_save_stock_history(stock_position.symbol_yahoo, start=start_date, end=end_date)
        print(f"Company {stock_position.symbol_yahoo} loaded and saved")
