from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import timedelta

from infomoney.apis import fetch_obj_tool_data, fetch_infomoney_high_low
from infomoney.converters import convert_infomoney_high_low_to_df


class Command(BaseCommand):
    help = 'Import data from Infomoney'

    def handle(self, *args, **options):
        print("Start import_infomoney")
        api_data = fetch_infomoney_high_low()
        df = convert_infomoney_high_low_to_df(api_data)
        print(f"\n\n df: {df.head()}\n\n")
        print("End import_infomoney")
