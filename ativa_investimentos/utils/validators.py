from ..models import StockPosition


def validate_all_symbols_exists(symbols: list[str]) -> None:
    """
    Validate if all symbols exists on StockPosition
    args:
        symbols: list of symbols to validate
    return:
        None
    """
    # Validate arguments
    assert symbols is not None, "Symbols is required"
    assert len(symbols) > 0, "Symbols list is empty"
    # Check if all symbols exists on StockPosition
    stock_positions = StockPosition.objects.filter(symbol__in=symbols)
    if len(stock_positions) != len(symbols):
        missing_symbols = set(symbols) - {stock_position.symbol for stock_position in stock_positions}
        raise ValueError(f"Symbols {missing_symbols} not exists on StockPosition")
