from django.contrib import admin

from yahoo_finances.models import Company, DailyStockHistory


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'short_name', 'long_name', 'sector', 'industry', 'exchange', 'quote_type', 'currency', 'financial_currency', 'load_date')
    search_fields = ('symbol', 'short_name', 'long_name', 'sector', 'industry', 'exchange', 'quote_type', 'currency', 'financial_currency', 'load_date')
    list_filter = ('sector', 'industry', 'exchange', 'quote_type', 'currency', 'financial_currency', 'load_date')
    date_hierarchy = 'load_date'
    ordering = ('symbol', 'short_name', 'long_name', 'sector', 'industry', 'exchange', 'quote_type', 'currency', 'financial_currency', 'load_date')


@admin.register(DailyStockHistory)
class DailyStockHistoryAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'splits', 'load_date')
    search_fields = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'splits', 'load_date')
    list_filter = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'splits', 'load_date')
    date_hierarchy = 'date'
    ordering = ('symbol', 'date', 'open', 'high', 'low', 'close', 'volume', 'dividends', 'splits', 'load_date')
