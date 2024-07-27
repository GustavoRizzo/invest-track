from datetime import datetime
from django.utils import timezone
from rest_framework.serializers import Serializer, ModelSerializer, DateField, CharField, FloatField

from .models import Company, DailyStockHistory


class DailyStockHistorySerializer(ModelSerializer):
    class Meta:
        model = DailyStockHistory
        fields = '__all__'


class InputsNormalizedCloseSerializer(Serializer):
    start_date = DateField(default=(datetime.today().date() - timezone.timedelta(days=30)))
    end_date = DateField(default=datetime.today().date())
    symbol = CharField(default='VALE3.SA')


class NormalizedCloseSerializer(ModelSerializer):
    normalized_close = FloatField()

    class Meta:
        model = DailyStockHistory
        fields = ['symbol', 'date', 'close', 'normalized_close']


class DateValueSerializer(Serializer):
    date = DateField()
    value = FloatField()


class StockHistorySerializer(Serializer):
    symbol = CharField()
    history = DateValueSerializer(many=True)


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
