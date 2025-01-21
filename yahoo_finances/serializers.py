from datetime import datetime
from django.utils import timezone
from django.db.models import QuerySet
from rest_framework.serializers import Serializer, ModelSerializer, DateField, CharField, FloatField, ListField, \
    ValidationError

from .models import Company, DailyStockHistory


class DailyStockHistorySerializer(ModelSerializer):
    class Meta:
        model = DailyStockHistory
        fields = '__all__'


class InputsNormalizedCloseSerializer(Serializer):
    start_date = DateField(default=(datetime.today().date() - timezone.timedelta(days=30)))
    end_date = DateField(default=datetime.today().date())
    symbols = ListField(child=CharField(), default=['VALE3.SA'])

    # Validate the symbols corresponde a valid Company
    def validate_symbols(self, value) -> list[str]:
        for symbol in value:
            if not Company.objects.filter(symbol=symbol).exists():
                raise ValidationError(f"Symbol {symbol} does not exist in the database.")
        return value

    # Return list of companies
    def get_companies(self) -> QuerySet[Company]:
        return Company.objects.filter(symbol__in=self.validated_data['symbols'])


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
