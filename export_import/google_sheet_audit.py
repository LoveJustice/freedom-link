from django.conf import settings

from itertools import chain

import logging

from export_import.google_sheet_basic import GoogleSheetBasic
from google_sheet import GoogleSheet
from delivery_io import get_delivery_export_rows

from story.models import Story, Delivery, Donor

logger = logging.getLogger(__name__);
 
def replace_deliveries():
    logger.info("Begin replace Delivery")
    delieveries_gs = GoogleSheetBasic(settings.SPREADSHEET_NAME, settings.DELIVERY_WORKSHEET_NAME)
    db_deliveries = Delivery.objects.select_related('story', 'donor').all()
    new_rows = get_delivery_export_rows(db_deliveries)
    
    reqs = []
    reqs.append(delieveries_gs.delete_request(1, delieveries_gs.rowCount))
    reqs.append(delieveries_gs.expand_request(len(new_rows)))
    reqs.append(delieveries_gs.delete_request(0,0))
    delieveries_gs.batch_update(reqs)
    
    delieveries_gs.append_rows(new_rows)
    logger.info("Complete replace Delivery")
