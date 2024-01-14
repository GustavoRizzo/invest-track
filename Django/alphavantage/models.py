from django.db import models


class DailyStockPrices(models.Model):
    symbol = models.CharField(max_length=10, unique=False, null=False)
    date = models.DateField(null=False)
    closing_price = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    load_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} - {self.date} - R${self.closing_price:.2f}"

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['symbol', 'date'], name='unique_symbol_date'),
        ]

    @classmethod
    def days_with_prices_for_symbol(cls, symbol: str) -> list:
        return list(cls.objects.filter(symbol=symbol).values_list('date', flat=True))
