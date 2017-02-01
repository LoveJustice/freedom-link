from django.db import transaction

from story.models import InterceptionRecord, Story

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

inv_how_sure = {}
for tup in InterceptionRecord.HOW_SURE_TRAFFICKING_CHOICES:
    inv_how_sure[tup[1]] = tup[0]

irf_data = [
    CopyCsvField("irf_number", "IRF #", False),

    # Red Flags
    BooleanCsvField("wife_under_18", "3.2 Wife is under 18", "True", "", "True", ""),
    BooleanCsvField("meeting_someone_across_border", "3.3 Is meeting someone just across border", "True", ""),
    BooleanCsvField("seen_in_last_month_in_nepal", "3.4 Meeting someone he/she's seen in Nepal", "True", ""),
    BooleanCsvField("traveling_with_someone_not_with_her", "3.5 Was traveling with someone not with him/her", "True", ""),
    BooleanCsvField("married_in_past_2_weeks", "3.6 Was married in the past two weeks", "True", ""),
    BooleanCsvField("married_in_past_2_8_weeks", "3.7 Was married within the past 2-8 weeks", "True", ""),
    BooleanCsvField("less_than_2_weeks_before_eloping", "3.8 Met less than 2 weeks before eloping", "True", ""),
    BooleanCsvField("between_2_12_weeks_before_eloping", "3.9 Met 2 - 12 weeks before eloping", "True", ""),
    BooleanCsvField("caste_not_same_as_relative", "3.10 Caste not the same as alleged relative", "True", ""),
    BooleanCsvField("caught_in_lie", "3.11 Caught in a lie or contradiction", "True", ""),
    
    BooleanCsvField("doesnt_know_going_to_india", "3.13 Doesn't know he/she's going to India", "True", ""),
    BooleanCsvField("running_away_over_18", "3.14 Running away from home (over 18)", "True", ""),
    BooleanCsvField("running_away_under_18", "3.15 Running away from home (under 18)", "True", ""),
    #BooleanCsvField("going_to_gulf_for_work", "3.16 Going to Gulf for work through India", "True", ""),
    BooleanCsvField("no_address_in_india", "3.17 Going for job, no address in India", "True", ""),
    BooleanCsvField("no_company_phone", "3.18 Going for job, no company phone number", "True", ""),
    BooleanCsvField("no_appointment_letter", "3.19 Going for job, no appointment letter", "True", ""),
    BooleanCsvField("valid_gulf_country_visa", "3.20 Has a valid Gulf country visa in passport", "True", ""),
    BooleanCsvField("passport_with_broker", "3.21 Passport is with a broker", "True", ""),
    BooleanCsvField("job_too_good_to_be_true", "3.22 Job is too good to be true", "True", ""),
    BooleanCsvField("not_real_job", "3.23 Called, not a real job", "True", ""),
    BooleanCsvField("couldnt_confirm_job", "3.24 Called, could not confirm job", "True", ""),
    
    BooleanCsvField("no_bags_long_trip",  "3.25 No bags though claim to be going for a long time", "True", ""),
    BooleanCsvField("shopping_overnight_stuff_in_bags",  "3.26 Shopping - stuff for overnight stay in bags", "True", ""),
    
    BooleanCsvField("no_enrollment_docs", "3.27 Going to study, no documentation of enrollment", "True", ""),
    BooleanCsvField("doesnt_know_school_name", "3.28 Going to study, does not know school's name and location", "True", ""),
    BooleanCsvField("no_school_phone", "3.29 Going to study, no phone number for school", "True", ""),
    BooleanCsvField("not_enrolled_in_school", "3.30 Called, not enrolled in school", "True", ""),
    
    BooleanCsvField("reluctant_treatment_info", "3.31 Reluctant to give info about treatment", "True", ""),
    BooleanCsvField("no_medical_documents", "3.32 Going for treatment, doesn't have medical documents", "True", ""),
    BooleanCsvField("fake_medical_documents", "3.33 Going for treatment, fake medical documents", "True", ""),
    BooleanCsvField("no_medical_appointment", "3.34 Called doctor, no medical appointment", "True", ""),
  
    # Staff reason for noticing
    BooleanCsvField("noticed_hesitant", "7.2 Seemed Hesitant", "True", ""),
    BooleanCsvField("noticed_nervous_or_afraid", "7.3 Was nervous or afraid", "True", ""),
    BooleanCsvField("noticed_hurrying", "7.4 Was hurrying", "True", ""),
    BooleanCsvField("noticed_drugged_or_drowsy", "7.5 Seemed Drugged or Drowsy", "True", ""),
    
    BooleanCsvField("noticed_new_clothes", "7.6 They Were Wearing New Clothes", "True", ""),
    BooleanCsvField("noticed_dirty_clothes", "7.7 They Had Dirty Clothes", "True", ""),
    BooleanCsvField("noticed_carrying_full_bags", "7.8 They Were Carrying Full Bags", "True", ""),
    BooleanCsvField("noticed_village_dress", "7.9 They Were Wearing Village Dress", "True", ""),
    
    BooleanCsvField("noticed_indian_looking", "7.1 That They Looked Indian", "True", ""),
    BooleanCsvField("noticed_typical_village_look", "7.11 They Had A Typical Village Look", "True", ""),
    BooleanCsvField("noticed_looked_like_agent", "7.12 They Looked Like An Agent", "True", ""),
    BooleanCsvField("noticed_caste_difference", "7.13 Their Caste Was Different", "True", ""),
    BooleanCsvField("noticed_young_looking", "7.14 That They Looked Young", "True", ""),
    
    BooleanCsvField("noticed_waiting_sitting", "7.15 That They Were Sitting/Waiting", "True", ""),
    BooleanCsvField("noticed_walking_to_border", "7.16 They Were Walking To The Border", "True", ""),
    BooleanCsvField("noticed_roaming_around", "7.17 They Were Roaming Around", "True", ""),
    BooleanCsvField("noticed_exiting_vehicle", "7.18 Them Exiting A Vehicle", "True", ""),
    BooleanCsvField("noticed_heading_to_vehicle", "7.19 Them Heading Into A Vehicle", "True", ""),
    BooleanCsvField("noticed_in_a_vehicle", "7.2 Them In A Vehicle", "True", ""),
    BooleanCsvField("noticed_in_a_rickshaw", "7.21 Them In A Rickshaw", "True", ""),
    BooleanCsvField("noticed_in_a_cart", "7.22 Them In A Cart", "True", ""),
    BooleanCsvField("noticed_carrying_a_baby", "7.23 Them Carrying A Baby", "True", ""),
    
        
    MapValueCsvField("how_sure_was_trafficking", "How sure", inv_how_sure)
]

story_data =[

    CopyCsvField("unique_story_code", "Unique ID", False),
    CopyCsvField("story_text", "Full Story", False),
    CopyCsvField("full_name", "Name", False, allow_null_or_blank_import=False),
]


               
# define default values on import as array of arrays
#    inner array defines
#      position 0 - title of field to default
#      position 1 - function to invoke to determine and set default value
#      position 2... - additional values required by the function to determine the default
default_import = []

def import_story_row(storyDict):
    errList = []
    
    #for key in storyDict:
    #    logger.info(storyDict[key])
    
    #default column values
    for default_op in default_import:
        try:
            default_op[1](storyDict, default_op, name_translation=spreadsheet_header_from_export_header)
        except:
            logger.error ("Failed to set default for field " + default_op[0] + traceback.format_exc() )
            errList.append("Failed to set default for field " + default_op[0])
        
    
  
    story_code = storyDict[spreadsheet_header_from_export_header(story_data[0].title)]
    if story_code is None:
        errList.append("Unable to find data for Story Code")
        return errList
    else:
        try:
            Story.objects.get(unique_story_code=story_code)
            errList.append("Story already exists")
            return errList
        except:
            pass

    story = Story()
    for field in story_data:
        try:
            errs = field.importField(story, storyDict, "", name_translation = spreadsheet_header_from_export_header)
            if errs is not None:
                errList.extend(errs)
        except:
            errList.append(field.title + ":Unexpected error -contact developer")
    
    # If IRF has already been created, link this story to it
    irf_nbr = storyDict[spreadsheet_header_from_export_header(irf_data[0].title)]
    try:
        irf = InterceptionRecord.objects.get(irf_number=irf_nbr)
    except:
        irf = InterceptionRecord()
        for field in irf_data:
            try:
                errs = field.importField(irf, storyDict, "", name_translation = spreadsheet_header_from_export_header)
                if errs is not None:
                    errList.extend(errs)
            except:
                errList.append(field.title + ":Unexpected error - contact developer")

        
    if len(errList) == 0:
        try:
            with transaction.atomic():
                irf.save()
                irfdb = InterceptionRecord.objects.get(id=irf.id)
                story.interception_record = irfdb
                story.save()
        except:
            logger.error ("Unexpected error saving Story in database Story Code=" + story_code + traceback.format_exc() )
            errList.append("Unexpected error saving Story in database")  
        
    return errList