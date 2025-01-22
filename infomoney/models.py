from django.db import models

from core.base.models import BaseModel


class HighLow(BaseModel):
    name = models.CharField(max_length=100, null=True)
    symbol = models.CharField(max_length=10, null=False)
    date = models.DateField(null=False)
    current_value = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    var_day = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    var_week = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    var_month = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    var_year = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    var_12_months = models.DecimalField(
        max_digits=10, decimal_places=2, null=True)
    min = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    max = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    volume = models.DecimalField(max_digits=15, decimal_places=2, null=True)

    def __str__(self):
        return f"{self.symbol} - {self.date} - R${self.current_value:.2f}"

    class Meta:
        verbose_name = "High Low"
        verbose_name_plural = "High Lows"
