from datetime import datetime, date
from django.db import models
from django.db.models import Manager, F, QuerySet, Q


class DailyStockHistoryManager(Manager):

    def get_normalized_close(self, start_date: date, symbol: str) -> models.QuerySet:
        """
        Get the normalized close price for a given symbol and start date.
        The normalized close price is calculated as the close price divided by the first day's close price.
        Parameters:
            - start_date (date): The start date to calculate the normalized close price.
            - symbol (str): The stock symbol to calculate the normalized close price.
        Returns:
            - models.QuerySet: A queryset with the normalized close price annotated as 'normalized_close'.
        """
        # Raise an error if the start date is not a date
        assert isinstance(start_date, date), f"start_date must be a date, not {type(start_date)}"
        # Get the first record for the symbol to calculate the normalization factor
        first_record = self.filter(symbol=symbol, date__gte=start_date).order_by('date').first()
        # If no record found, return empty queryset
        if not first_record:
            return self.none()
        # Calculate normalization factor based on the first day's close price
        normalization_factor = first_record.close
        # Raise an error if the normalization factor is zero
        if normalization_factor == 0:
            raise ValueError(f"Normalization factor is zero for {symbol}, date: {first_record.date}")
        # Annotate the queryset with normalized close price
        return self.filter(symbol=symbol, date__gte=start_date) \
            .annotate(normalized_close=((F('close') / normalization_factor)*100))


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

    def close_history(self, start_date: date, end_date: date) -> QuerySet['DailyStockHistory']:
        return DailyStockHistory.objects \
            .filter(symbol=self.symbol, date__gte=start_date, date__lte=end_date) \
            .order_by('date')

    def normalized_close_history(self, start_date: date, end_date: date = None) -> QuerySet['DailyStockHistory']:
        filter = Q()
        if end_date:
            filter = Q(date__gte=start_date, date__lte=end_date)
        return DailyStockHistory.objects \
            .get_normalized_close(start_date=start_date, symbol=self.symbol) \
            .filter(filter) \
            .order_by('date')

    def __str__(self):
        return self.symbol

    class Meta:
        verbose_name_plural = "Companies"


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

    objects = DailyStockHistoryManager()

    def __str__(self):
        return f"{self.symbol} - {self.date} - R${self.close:.2f}"

    @classmethod
    def days_with_prices_for_symbol(self, symbol: str) -> list:
        return list(self.objects.filter(symbol=symbol).values_list('date', flat=True))
