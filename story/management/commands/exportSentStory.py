from django.core.management.base import BaseCommand

from export_import.google_sheet_import import audit_stories


class Command(BaseCommand):
    def handle(self, *args, **options):
        audit_stories()
