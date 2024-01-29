from django.db import models


class Company(models.Model):
    currency = models.CharField(max_length=10)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    website = models.URLField()
    industry = models.CharField(max_length=255)
    industry_key = models.CharField(max_length=255)
    industry_disp = models.CharField(max_length=255)
    sector = models.CharField(max_length=255)
    sector_key = models.CharField(max_length=255)
    exchange = models.CharField(max_length=10)
    quote_type = models.CharField(max_length=50)
    symbol = models.CharField(max_length=50, unique=True)
    underlying_symbol = models.CharField(max_length=50)
    short_name = models.CharField(max_length=255)
    long_name = models.CharField(max_length=255)
    first_trade_date_epoch_utc = models.DateTimeField()
    time_zone_full_name = models.CharField(max_length=255)
    time_zone_short_name = models.CharField(max_length=50)
    financial_currency = models.CharField(max_length=10)
    long_business_summary = models.TextField()
    load_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.symbol


class DailyStockHistory(models.Model):
    symbol = models.CharField(max_length=10, db_index=True)
    date = models.DateField(null=False, db_index=True)
    open = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    high = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    low = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    close = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    volume = models.IntegerField(null=False)
    dividends = models.DecimalField(max_digits=10, decimal_places=6)
    splits = models.DecimalField(max_digits=10, decimal_places=6)
    load_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.date} - R${self.close:.2f}"

    @classmethod
    def days_with_prices_for_symbol(cls, symbol: str) -> list:
        return list(cls.objects.filter(symbol=symbol).values_list('date', flat=True))
