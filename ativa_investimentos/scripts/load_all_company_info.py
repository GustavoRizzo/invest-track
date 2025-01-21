
from yahoo_finances.api import fetch_and_save_company_data
from ..models import StockPosition


def main():
    # Load all StockPosition
    stock_positions = StockPosition.objects.all()
    for stock_position in stock_positions:
        print(f"\nLoading company info for {stock_position.symbol_yahoo}")
        company = fetch_and_save_company_data(stock_position.symbol_yahoo)
        print(f"Company {company.symbol} loaded and saved")
