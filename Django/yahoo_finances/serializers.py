from datetime import datetime
from django.utils import timezone
from rest_framework import serializers

from .models import Company, DailyStockHistory


class DailyStockHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyStockHistory
        fields = '__all__'


class InputsNormalizedCloseSerializer(serializers.Serializer):
    start_date = serializers.DateField(default=(datetime.today().date() - timezone.timedelta(days=30)))
    end_date = serializers.DateField(default=datetime.today().date())
    symbol = serializers.CharField(default='VALE3.SA')


class NormalizedCloseSerializer(serializers.ModelSerializer):
    normalized_close = serializers.FloatField()

    class Meta:
        model = DailyStockHistory
        fields = ['symbol', 'date', 'close', 'normalized_close']


class DateValueSerializer(serializers.Serializer):
    date = serializers.DateField()
    value = serializers.FloatField()


class StockHistorySerializer(serializers.Serializer):
    symbol = serializers.CharField()
    history = DateValueSerializer(many=True)


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
