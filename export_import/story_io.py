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
    BooleanCsvField("wife_under_18", "3.2 Wife is under 18", "Wife is under 18", ""),
    BooleanCsvField("meeting_someone_across_border", "3.3 Is meeting someone just across border", "Is meeting someone just across border", ""),
    BooleanCsvField("seen_in_last_month_in_nepal", "3.4 Meeting someone he/she's seen in Nepal", "Meeting someone he/she's seen in Nepal", ""),
    BooleanCsvField("traveling_with_someone_not_with_her", "3.5 Was traveling with someone not with him/her", "Was traveling with someone not with him/her", ""),
    BooleanCsvField("married_in_past_2_weeks", "3.6 Was married in the past two weeks", "Was married in the past two weeks", ""),
    BooleanCsvField("married_in_past_2_8_weeks", "3.7 Was married within the past 2-8 weeks", "Was married within the past 2-8 weeks", ""),
    BooleanCsvField("less_than_2_weeks_before_eloping", "3.8 Met less than 2 weeks before eloping", "Met less than 2 weeks before eloping", ""),
    BooleanCsvField("between_2_12_weeks_before_eloping", "3.9 Met 2 - 12 weeks before eloping", "Met 2 - 12 weeks before eloping", ""),
    BooleanCsvField("caste_not_same_as_relative", "3.10 Caste not the same as alleged relative", "Caste not the same as alleged relative", ""),
    BooleanCsvField("caught_in_lie", "3.11 Caught in a lie or contradiction", "Caught in a lie or contradiction", ""),
    
    BooleanCsvField("doesnt_know_going_to_india", "3.13 Doesn't know he/she's going to India", "Doesn't know he/she's going to India", ""),
    BooleanCsvField("running_away_over_18", "3.14 Running away from home (over 18)", "Running away from home (over 18)", ""),
    BooleanCsvField("running_away_under_18", "3.15 Running away from home (under 18)", "Running away from home (under 18)", ""),
    #BooleanCsvField("going_to_gulf_for_work", "3.16 Going to Gulf for work through India", "Going to Gulf for work through India", ""),
    BooleanCsvField("no_address_in_india", "3.17 Going for job, no address in India", "Going for job, no address in India", ""),
    BooleanCsvField("no_company_phone", "3.18 Going for job, no company phone number", "Going for job, no company phone number", ""),
    BooleanCsvField("no_appointment_letter", "3.19 Going for job, no appointment letter", "Going for job, no appointment letter", ""),
    BooleanCsvField("valid_gulf_country_visa", "3.20 Has a valid Gulf country visa in passport", "Has a valid Gulf country visa in passport", ""),
    BooleanCsvField("passport_with_broker", "3.21 Passport is with a broker", "Passport is with a broker", ""),
    BooleanCsvField("job_too_good_to_be_true", "3.22 Job is too good to be true", "Job is too good to be true", ""),
    BooleanCsvField("not_real_job", "3.23 Called, not a real job", "Called, not a real job", ""),
    BooleanCsvField("couldnt_confirm_job", "3.24 Called, could not confirm job", "Called, could not confirm job", ""),
    
    BooleanCsvField("no_bags_long_trip",  "3.25 No bags though claim to be going for a long time", "No bags though claim to be going for a long time", ""),
    BooleanCsvField("shopping_overnight_stuff_in_bags",  "3.26 Shopping - stuff for overnight stay in bags", "Shopping - stuff for overnight stay in bags", ""),
    
    BooleanCsvField("no_enrollment_docs", "3.27 Going to study, no documentation of enrollment", "Going to study, no documentation of enrollment", ""),
    BooleanCsvField("doesnt_know_school_name", "3.28 Going to study, does not know school's name and location", "Going to study, does not know school's name and location", ""),
    BooleanCsvField("no_school_phone", "3.29 Going to study, no phone number for school", "Going to study, no phone number for school", ""),
    BooleanCsvField("not_enrolled_in_school", "3.30 Called, not enrolled in school", "Called, not enrolled in school", ""),
    
    BooleanCsvField("reluctant_treatment_info", "3.31 Reluctant to give info about treatment", "Reluctant to give info about treatment", ""),
    BooleanCsvField("no_medical_documents", "3.32 Going for treatment, doesn't have medical documents", "Going for treatment, doesn't have medical documents", ""),
    BooleanCsvField("fake_medical_documents", "3.33 Going for treatment, fake medical documents", "Going for treatment, fake medical documents", ""),
    BooleanCsvField("no_medical_appointment", "3.34 Called doctor, no medical appointment", "Called doctor, no medical appointment", ""),
  
    # Staff reason for noticing
    BooleanCsvField("noticed_hesitant", "7.2 Seemed Hesitant", "Noticed they were hesitant", ""),
    BooleanCsvField("noticed_nervous_or_afraid", "7.3 Was nervous or afraid", "Noticed they were nervous or afraid", ""),
    BooleanCsvField("noticed_hurrying", "7.4 Was hurrying", "Noticed they were hurrying", ""),
    BooleanCsvField("noticed_drugged_or_drowsy", "7.5 Seemed Drugged or Drowsy", "Noticed they were drugged or drowsy", ""),
    
    BooleanCsvField("noticed_new_clothes", "7.6 They Were Wearing New Clothes", "Noticed they were wearing new clothes", ""),
    BooleanCsvField("noticed_dirty_clothes", "7.7 They Had Dirty Clothes", "Noticed they had dirty clothes", ""),
    BooleanCsvField("noticed_carrying_full_bags", "7.8 They Were Carrying Full Bags", "Noticed they were carrying full bags", ""),
    BooleanCsvField("noticed_village_dress", "7.9 They Were Wearing Village Dress", "Noticed they were wearing village dress", ""),
    
    BooleanCsvField("noticed_indian_looking", "7.1 That They Looked Indian", "Noticed that they looked Indian", ""),
    BooleanCsvField("noticed_typical_village_look", "7.11 They Had A Typical Village Look", "Noticed they had a typical village look", ""),
    BooleanCsvField("noticed_looked_like_agent", "7.12 They Looked Like An Agent", "Noticed they looked like an agent", ""),
    BooleanCsvField("noticed_caste_difference", "7.13 Their Caste Was Different", "Noticed their caste was different", ""),
    BooleanCsvField("noticed_young_looking", "7.14 That They Looked Young", "Noticed that they looked young", ""),
    
    BooleanCsvField("noticed_waiting_sitting", "7.15 That They Were Sitting/Waiting", "Noticed that they were sitting/waiting", ""),
    BooleanCsvField("noticed_walking_to_border", "7.16 They Were Walking To The Border", "Noticed they were walking to the border", ""),
    BooleanCsvField("noticed_roaming_around", "7.17 They Were Roaming Around", "Noticed they were roaming around", ""),
    BooleanCsvField("noticed_exiting_vehicle", "7.18 Them Exiting A Vehicle", "Noticed them exiting a vehicle", ""),
    BooleanCsvField("noticed_heading_to_vehicle", "7.19 Them Heading Into A Vehicle", "Noticed them heading into a vehicle", ""),
    BooleanCsvField("noticed_in_a_vehicle", "7.2 Them In A Vehicle", "Noticed them in a vehicle", ""),
    BooleanCsvField("noticed_in_a_rickshaw", "7.21 Them In A Rickshaw", "Noticed them in a rickshaw", ""),
    BooleanCsvField("noticed_in_a_cart", "7.22 Them In A Cart", "Noticed them in a cart", ""),
    BooleanCsvField("noticed_carrying_a_baby", "7.23 Them Carrying A Baby", "Noticed them carrying a baby", ""),
    
        
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