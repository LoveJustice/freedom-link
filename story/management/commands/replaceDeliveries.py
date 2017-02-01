from django.core.management.base import BaseCommand

from export_import.google_sheet_audit import replace_deliveries


class Command(BaseCommand):
    def handle(self, *args, **options):
        replace_deliveries()