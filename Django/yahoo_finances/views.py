import time
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT

from .models import Company, DailyStockHistory
from .serializers import CompanySerializer, DailyStockHistorySerializer, DateValueSerializer, InputsNormalizedCloseSerializer, NormalizedCloseSerializer, StockHistorySerializer


class DailyStockHistoryViewSet(ModelViewSet):
    queryset = DailyStockHistory.objects.all()
    serializer_class = DailyStockHistorySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post',]

    @swagger_auto_schema(request_body=InputsNormalizedCloseSerializer, responses={200: NormalizedCloseSerializer})
    @action(detail=False, methods=['post'], url_path='normalized', url_name='normalized',
            permission_classes=[IsAuthenticated])
    def get_normalized_close(self, request):
        # Get the input data
        start_date = request.data.get('start_date')
        symbol = request.data.get('symbol')
        # Validate the input
        serializer_input = InputsNormalizedCloseSerializer(data={'start_date': start_date, 'symbol': symbol})
        serializer_input.is_valid(raise_exception=True)
        # Get the normalized close price
        stock_history = DailyStockHistory.objects.get_normalized_close(start_date, symbol)
        serializer_output = NormalizedCloseSerializer(stock_history, many=True)
        return Response(serializer_output.data, status=HTTP_200_OK)

    @swagger_auto_schema(request_body=InputsNormalizedCloseSerializer, responses={200: StockHistorySerializer})
    @action(detail=False, methods=['post'], url_path='normalized-v2', url_name='normalized-v2',
            permission_classes=[IsAuthenticated])
    def get_normalized_close_v2(self, request):
        # Get the input data
        start_date = request.data.get('start_date')
        symbol = request.data.get('symbol')
        # Validate the input
        serializer_input = InputsNormalizedCloseSerializer(data={'start_date': start_date, 'symbol': symbol})
        serializer_input.is_valid(raise_exception=True)
        # Get the normalized close price
        queryset = DailyStockHistory.objects.get_normalized_close(start_date, symbol)
        if not queryset:
            return Response({'error': 'No data found'}, status=HTTP_204_NO_CONTENT)
        # Convert to a DateValueSerializer
        list = queryset.annotate(value=F('normalized_close')).values('date', 'value')
        data_value = DateValueSerializer(list, many=True)
        serializer_output = StockHistorySerializer({'symbol': symbol, 'history': data_value.data})
        return Response(serializer_output.data, status=HTTP_200_OK)


def company_details(request, company_id):
    # Get the Company object
    company = get_object_or_404(Company, pk=company_id)
    # Get the DailyStockHistory for the Company
    stock_history = DailyStockHistory.objects.filter(symbol=company.symbol)
    return render(request, 'company_details.html', {'company': company, 'stock_history': stock_history})


def multiple_companies(request):
    # Symbols
    symbols = ['VALE3.SA', 'ASAI3.SA', 'PETR4.SA', 'MGLU3.SA']
    # Get DailyStockHistory for each symbol
    companies = []
    for symbol in symbols:
        stock_history = DailyStockHistory.objects.filter(symbol=symbol, date__gte='2024-01-01')
        companies.append({'symbol': symbol, 'stock_history': stock_history})
    return render(request, 'multiple_companies.html', {'companies': companies})


def multiple_normalized_companies(request):
    # Symbols
    symbols = ['VALE3.SA', 'ASAI3.SA', 'PETR4.SA', 'MGLU3.SA']
    # Get DailyStockHistory for each symbol
    stocks = []
    for symbol in symbols:
        stock_history = DailyStockHistory.objects.get_normalized_close('2024-01-01', symbol)
        stocks.append({'symbol': symbol, 'stock_history': stock_history})
    return render(request, 'multiple_normalized_companies.html', {'stocks': stocks})


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']


class FixedDataView(APIView):
    def post(self, request):
        # Deley 5 seconds
        time.sleep(2)
        data = [
            {
                "symbol": "VALE3.SA",
                "history": [
                    {"date": "2024-02-01", "value": 100},
                    {"date": "2024-02-02", "value": 97.96886582653818},
                    {"date": "2024-02-05", "value": 97.12379540400296},
                    {"date": "2024-02-06", "value": 98.84358784284656},
                    {"date": "2024-02-07", "value": 99.03632320237213},
                    {"date": "2024-02-08", "value": 98.16160118606375},
                    {"date": "2024-02-09", "value": 97.73165307635286},
                    {"date": "2024-02-14", "value": 97.4351371386212},
                    {"date": "2024-02-15", "value": 97.12379540400296},
                    {"date": "2024-02-16", "value": 100.81541882876205},
                    {"date": "2024-02-19", "value": 100.05930318754633},
                    {"date": "2024-02-20", "value": 97.8650852483321},
                    {"date": "2024-02-21", "value": 98.60637509266122},
                    {"date": "2024-02-22", "value": 99.6590066716086},
                    {"date": "2024-02-23", "value": 99.89621942179392}
                ]
            },
            {
                "symbol": "ASAI3.SA",
                "history": [
                    {"date": "2024-02-01", "value": 100},
                    {"date": "2024-02-02", "value": 97.96886582653818},
                    {"date": "2024-02-05", "value": 97.12379540400296},
                    {"date": "2024-02-06", "value": 98.84358784284656},
                    {"date": "2024-02-07", "value": 99.03632320237213},
                    {"date": "2024-02-08", "value": 99.16160118606375},
                    {"date": "2024-02-09", "value": 94.73165307635286},
                    {"date": "2024-02-14", "value": 97.4351371386212},
                    {"date": "2024-02-15", "value": 97.12379540400296},
                    {"date": "2024-02-16", "value": 101.81541882876205},
                    {"date": "2024-02-19", "value": 100.05930318754633},
                    {"date": "2024-02-20", "value": 105.8650852483321},
                    {"date": "2024-02-21", "value": 98.60637509266122},
                    {"date": "2024-02-22", "value": 99.6590066716086},
                    {"date": "2024-02-23", "value": 99.89621942179392}
                ]
            }
        ]
        return Response(data, status=HTTP_200_OK)
