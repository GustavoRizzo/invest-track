from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import timedelta

from infomoney.apis import fetch_obj_tool_data


class Command(BaseCommand):
    help = 'Import data from Infomoney'

    def handle(self, *args, **options):
        print("Start import_infomoney")
        obj_tool_data = fetch_obj_tool_data()
        key = obj_tool_data["altas_e_baixas_table_nonce"]
        print(f"key 'altas_e_baixas_table_nonce': {key}")
        print("End import_infomoney")
