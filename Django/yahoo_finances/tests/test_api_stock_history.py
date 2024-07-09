from core.base.test import BaseAPITestCase
from rest_framework import status


class ApiStockHistoryTest(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        super().setUpTestData()

    def test_erro(self):
        # Arrange 1 - Call API without any data       
        data = {
            'start_date': '2024-01-01',
            'symbol': 'PETR4.SA'
        }
        self.client.force_authenticate(user=self.test_user)
        # Act 1
        response1 = self.client.post(self.url_stock_history, data)
        # Assert 1
        self.assertEqual(response1.status_code, status.HTTP_204_NO_CONTENT)
