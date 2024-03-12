from django.db import models

from core.base.models import BaseModel


class StockPosition(BaseModel):
    symbol = models.CharField(max_length=10, unique=True, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)

    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
