from datetime import date, timedelta
from django.urls import reverse
from faker import Faker
from model_bakery import baker
from rest_framework.test import APITestCase


from django.contrib.auth.models import User

from yahoo_finances.models import Company, DailyStockHistory


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):
        cls.fake = Faker()

        # Urls
        cls.url_stock_history = reverse('yahoo_finances:stock_history')

        # Create users
        cls.test_user = User.objects.create_user(username='tester', password='tester123')

    def create_company(self, symbol: str = None) -> Company:
        if not symbol:
            symbol = self.fake.word()
        return baker.make(Company, symbol=symbol)

    def create_daily_stock_history(self, symbol: str = None, date: date = date.today()) -> DailyStockHistory:
        if not symbol:
            symbol = self.fake.word()
        return baker.make(DailyStockHistory, symbol=symbol, date=date)

    def create_company_with_stock_history(self, symbol: str, start_date: date = date(2024, 1, 1), end_date: date = date(2024, 1, 10) ) -> Company:
        company = self.create_company(symbol)
        for d in range((end_date - start_date).days + 1):
            self.create_daily_stock_history(symbol, start_date + timedelta(days=d))
        return company
