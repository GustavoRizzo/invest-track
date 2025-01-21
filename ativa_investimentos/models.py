from django.db import models

from core.base.models import BaseModel
from yahoo_finances.models import Company
from yahoo_finances.api import fetch_and_save_company_data


class StockPosition(BaseModel):
    symbol = models.CharField(max_length=10, unique=True, blank=False, null=False)
    quantity = models.IntegerField(blank=False, null=False)

    @property
    def symbol_yahoo(self) -> str:
        return f"{self.symbol}.SA"

    def __str__(self):
        return f"{self.symbol} - {self.quantity}"
