from rest_framework import serializers

from .models import DailyStockHistory


class DailyStockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStockHistory
        fields = '__all__'
