from core.base.test import BaseAPITestCase
from rest_framework import status

from infomoney.converters import convert_high_low_dict_to_df

mack_api_data = {
    'sEcho': '1',
    'iTotalRecords': 2,
    'iTotalDisplayRecords': 2,
    'aaData': [
        ['BRASKEM PNA N1', 'BRKM5', '20/01', '13.74', '8.44', '8.45',
            '18.65', '18.65', '12.68', '14.20', '-22.15', '66676444.00'],
        ['ASSAI ON NM', 'ASAI3', '20/01', '6.10', '4.81', '4.81',
            '9.89', '9.89', '5.67', '6.21', '-56.73', '66813606.00']
    ]
}


class InfomoneyTest(BaseAPITestCase):

    @classmethod
    def setUpTestData(cls):
        # setUpTestData: Run once to set up non-modified data for all class methods.
        super().setUpTestData()

    def test_convert_high_low_dict_to_df(self):
        # Arrange
        data = mack_api_data
        # Act
        df = convert_high_low_dict_to_df(data)

        print(df.head())
        # Assert
        self.assertEqual(len(df), 2)
        self.assertEqual(df.columns, ['name', 'symbol', 'date', 'current_value', 'var_day', 'var_week', 'var_month',
                                      'var_year', 'var_12_months', 'min', 'max', 'volume'])
