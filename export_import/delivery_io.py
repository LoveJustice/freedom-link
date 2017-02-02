from django.db import transaction

from story.models import Delivery, Story, Donor

from django.conf import settings

import traceback
import logging

from field_types import BooleanCsvField
from field_types import CopyCsvField
from field_types import DateTimeCsvField
from field_types import MapValueCsvField

from field_types import no_translation

from google_sheet_names import spreadsheet_header_from_export_header

logger = logging.getLogger(__name__);        

story_data =[
    CopyCsvField("unique_story_code", "Unique ID", False),
    CopyCsvField("story_text", "Full Story", False),
]

delivery_data = [
    DateTimeCsvField("date_sent", "Date Sent"),
]

donor_data = [
    CopyCsvField("email", "Donor", False),
    CopyCsvField("first_name", "Donor First", False),
    CopyCsvField("last_name", "Donor Last", False),    
]


def get_delivery_export_rows(deliveries):
    logger.debug("Enter get_delivery_export_rows delivery count=" + str(len(deliveries)))
    rows = []
    delivery_headers = []
    for field in story_data:
        delivery_headers.append(field.title)

    for field in delivery_data:
        delivery_headers.append(field.title)

    for field in donor_data:
        delivery_headers.append(field.title)

    rows.append(delivery_headers)

    for delivery in deliveries:
        row = []

        # export base story
        for field in story_data:
            row.append(field.exportField(delivery.story))
        
        # export delivery
        for field in delivery_data:
            row.append(field.exportField(delivery))
        # export donor
        for field in donor_data:
            row.append(field.exportField(delivery.donor))
        rows.append(row)
    return rows