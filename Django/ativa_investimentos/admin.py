from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from .models import StockPosition


@admin.register(StockPosition)
class StockPositionAdmin(admin.ModelAdmin):
    list_display = ("symbol", "quantity", "created_at", "updated_at", "is_active", "is_deleted")
    list_filter = ("symbol", "is_active", "is_deleted")
    search_fields = ("symbol",)
    readonly_fields = ("created_at", "updated_at", "log_history")
    fieldsets = (
        (None, {
            "fields": ("symbol", "quantity")
        }),
        ("Status", {
            "fields": ("is_active", "is_deleted")
        }),
        ("History", {
            "fields": ("created_at", "updated_at", "log_history"),
            "classes": ("collapse",)
        })
    )
