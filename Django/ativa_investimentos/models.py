from django.db import models


class StockPosition(models.Model):
    symbol = models.CharField(max_length=10, unique=True, blank=False, null=False)
    quantity = models.IntegerField(required=True, blank=False, null=False)

    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
