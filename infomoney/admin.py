from django.contrib import admin
from core.base.admin import BaseAdmin
from .models import HighLow


@admin.register(HighLow)
class HighLowAdmin(BaseAdmin):
    list_display = ('name', 'symbol', 'date', 'current_value', 'var_day', 'var_week',
                    'var_month', 'var_year', 'var_12_months', 'min', 'max', 'volume')
