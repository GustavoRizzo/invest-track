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

    def __str__(self):
        return self.symbol
