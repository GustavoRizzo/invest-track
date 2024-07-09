from django.urls import reverse
from rest_framework.test import APITestCase

from django.contrib.auth.models import User


class BaseAPITestCase(APITestCase):

    @classmethod
    def setUpTestData(cls):

        # Urls
        cls.url_stock_history = reverse('yahoo_finances:stock_history')

        # Create users
        cls.test_user = User.objects.create_user(username='tester', password='tester123')
