from django.core.management.base import BaseCommand
from django.utils import timezone

from datetime import timedelta


class Command(BaseCommand):
    help = 'Import data from Infomoney'

    def handle(self, *args, **options):
        print("Start import_infomoney")
        print("End import_infomoney")
