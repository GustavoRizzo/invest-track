from datetime import date
from django.db.models import F
from django.shortcuts import render, get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK, HTTP_204_NO_CONTENT, HTTP_400_BAD_REQUEST

from .utils import get_company_serializer_history_data, get_company_serializer_normalized_history_data
from .models import Company, DailyStockHistory
from .serializers import CompanySerializer, DailyStockHistorySerializer, DateValueSerializer, \
    InputsNormalizedCloseSerializer, NormalizedCloseSerializer, StockHistorySerializer


class DailyStockHistoryViewSet(ModelViewSet):
    queryset = DailyStockHistory.objects.all()
    serializer_class = DailyStockHistorySerializer
    permission_classes = [IsAuthenticated]
    http_method_names = []


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
        stock_history = DailyStockHistory.objects.get_normalized_close(symbol=symbol, start_date='2024-01-01')
        stocks.append({'symbol': symbol, 'stock_history': stock_history})
    return render(request, 'multiple_normalized_companies.html', {'stocks': stocks})


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    permission_classes = [IsAuthenticated, IsAdminUser]
    http_method_names = ['get']


class StockHistoryView(APIView):
    @swagger_auto_schema(request_body=InputsNormalizedCloseSerializer,
                         responses={200: StockHistorySerializer(many=True)})
    def post(self, request):
        """
        Get stock history for a given symbol
        """
        serializer_input = InputsNormalizedCloseSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)
        # Try to find the company
        companys = serializer_input.get_companies()
        if not companys:
            return Response({'error': 'Company not found'}, status=HTTP_204_NO_CONTENT)
        list_serializer_data = []
        # Get serialized data for each company
        for company in companys:
            serializer_output, err = get_company_serializer_history_data(
                company=company,
                start_date=serializer_input.validated_data['start_date'],
                end_date=serializer_input.validated_data.get('end_date', date.today())
            )
            if err:
                return Response(serializer_output, status=HTTP_400_BAD_REQUEST)
            list_serializer_data.append(serializer_output.data)
        return Response(StockHistorySerializer(list_serializer_data, many=True).data, status=HTTP_200_OK)


class StockNormalizedHistoryView(APIView):
    @swagger_auto_schema(request_body=InputsNormalizedCloseSerializer,
                         responses={200: StockHistorySerializer})
    def post(self, request):
        """
        Get normalized stock history for a given symbol
        """
        serializer_input = InputsNormalizedCloseSerializer(data=request.data)
        serializer_input.is_valid(raise_exception=True)
        # Try to find the company
        companys = serializer_input.get_companies()
        if not companys:
            return Response({'error': 'Company not found'}, status=HTTP_204_NO_CONTENT)
        list_serializer_data = []
        # Get serialized data for each company
        for company in companys:
            serializer_output, err = get_company_serializer_normalized_history_data(
                company=company,
                start_date=serializer_input.validated_data['start_date'],
                end_date=serializer_input.validated_data.get('end_date', date.today())
            )
            if err:
                return Response(serializer_output, status=HTTP_400_BAD_REQUEST)
            list_serializer_data.append(serializer_output.data)
        return Response(StockHistorySerializer(list_serializer_data, many=True).data, status=HTTP_200_OK)
