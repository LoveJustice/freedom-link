from parse import parse
from datetime import datetime
from django.db import models
from django.utils.timezone import make_naive, localtime, make_aware

def no_translation(title):
    return title

# export/import field value - no translation
class CopyCsvField:
    def __init__(self, data_name, title, use_none_for_blank, export_null_or_blank_as="", allow_null_or_blank_import = True):
        self.data_name = data_name
        self.title = title
        self.use_none_for_blank = use_none_for_blank
        self.export_null_or_blank_as = export_null_or_blank_as
        self.allow_null_or_blank_import = allow_null_or_blank_import

    def importField(self, instance, csv_map, title_prefix = None, name_translation = no_translation):
        errs = []
        if title_prefix is not None:
            column_title = self.title.format(title_prefix )
        else:
            column_title = self.title        
        
        value = csv_map[name_translation(column_title)]
        if value is None:
            if not self.allow_null_or_blank_import:
                errs.append(column_title)
            elif not self.use_none_for_blank:
                value = ""
          
        setattr(instance, self.data_name, value)
            
        return errs

    def exportField(self, instance):
        rv = getattr(instance, self.data_name)
        if rv is None or rv == "":
            rv = self.export_null_or_blank_as

        return rv

# export/import date value
class DateTimeCsvField:
    parse_options = ["%m/%d/%Y %H:%M:%S","%Y-%m-%d %H:%M:%S","%m/%d/%Y %I:%M:%S %p","%Y-%m-%d %I:%M:%S %p",
                     "%m/%d/%y %H:%M:%S","%m/%d/%y %I:%M:%S %p",
                     "%m/%d/%Y %H:%M","%Y-%m-%d %H:%M","%m/%d/%Y %I:%M %p","%Y-%m-%d %I:%M %p",
                     "%m/%d/%y %H:%M","%m/%d/%y %I:%M %p"];
    def __init__(self, data_name, title):
        self.data_name = data_name
        self.title = title

    def importField(self, instance, csv_map, title_prefix = None, name_translation = no_translation):
        errs = []
        if title_prefix is not None:
            column_title = self.title.format(title_prefix)
        else:
            column_title = self.title

        value = csv_map[name_translation(column_title)]
        if value is not None:
            parsed_value = None
            for fmt in DateTimeCsvField.parse_options:
                try:
                    parsed_value = datetime.strptime(value, fmt)
                    parsed_value = make_aware(parsed_value)
                    setattr(instance, self.data_name, parsed_value)
                    break
                except:
                    pass
                
            if parsed_value is None:
                errs.append(column_title)
        else:
            errs.append(column_title)
        
        return errs

    def exportField(self, instance):
        value = getattr(instance, self.data_name)        
        local_val = localtime(value)
        local_val = local_val.replace(microsecond=0)
        return str(make_naive(local_val, local_val.tzinfo))

# export text string for boolean field - one value for true alternate value for false
class BooleanCsvField:
    def __init__(self, data_name, title, true_string, false_string, depend_name = None, allow_null_or_blank_import = True):
        self.data_name = data_name
        self.title = title
        self.true_string = true_string
        self.false_string = false_string
        self.depend_name = depend_name
        self.allow_null_or_blank_import = allow_null_or_blank_import

    def importField(self, instance, csv_map, title_prefix = None, name_translation = no_translation):
        errs = []
        if title_prefix is not None:
            column_title = self.title.format(title_prefix)
        else:
            column_title = self.title
       
        value = csv_map[name_translation(column_title)]
        
        if value is None:
            value = ""
        
        if value == self.true_string:
            value = True
        elif value == self.false_string:
            value = False
        elif self.allow_null_or_blank_import:
            if value == "":
                value = None
        else:
            errs.append(column_title)
            return errs

        setattr(instance, self.data_name, value)
        
        return errs

    def exportField(self, instance):
        if self.depend_name is not None:
            dep_value = getattr(instance, self.depend_name)
            if dep_value is None or dep_value == False:
                return ""

        value = getattr(instance, self.data_name)
        rv = ""
        if value is not None:
            if value:
                rv = self.true_string
            else:
                rv = self.false_string

        return rv
        
        
      
# Export/import value from a field.  Map identifies the mapping from the database value
# to the export value
class MapValueCsvField:
    def __init__(self, data_name, title, value_map, export_default="", required_nonempty=False):
        self.data_name = data_name
        self.title = title
        self.value_map = value_map
        self.export_default = export_default
        self.required_nonempty = required_nonempty

    def importField(self, instance, csv_map, title_prefix = None, name_translation = no_translation):
        errs = []
        if title_prefix is not None:
            column_title = self.title.format(title_prefix)
        else:
            column_title = self.title
        
        value = csv_map[name_translation(column_title)]
        if value is not None:
            try:
                mapped_value = self.value_map[value]
                if mapped_value is not None:
                    setattr(instance, self.data_name, mapped_value)
                else:
                    errs.append(column_title)
            except:
                errs.append(column_title)
        else:
            if self.required_nonempty:
                errs.append(column_title)
            else:
                setattr(instance, self.data_name, value)
            
        return errs

    def exportField(self, instance):
        value = getattr(instance, self.data_name)

        for key, val in self.value_map.items():
            if val == value:
                return key

        return self.export_default