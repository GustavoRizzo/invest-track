from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import timedelta

from infomoney.apis import fetch_obj_tool_data, fetch_infomoney_hight_low


class Command(BaseCommand):
    help = 'Import data from Infomoney'

    def handle(self, *args, **options):
        print("Start import_infomoney")
        data = fetch_infomoney_hight_low()
        print(f"\n\n data: {data}")
        print("End import_infomoney")
