from google_sheet import GoogleSheet
from google_sheet_names import spreadsheet_header_from_export_header
from story_io import import_story_row

from django.conf import settings

import logging

logger = logging.getLogger(__name__);

class GoogleSheetImport (GoogleSheet):
    READY_TO_IMPORT = 'Ready'
    DUPLICATE_IMPORT = 'Existing'
    REJECTED_IMPORT = 'Rejected'
    IMPORT_SUCCESS = 'Imported'
    
    def __init__(self, spreadsheet_name, sheet_name, key_column_name, export_method, issue_column, id_column_name, import_method):
        GoogleSheet.__init__(self, spreadsheet_name, sheet_name, key_column_name, None)
        self.issue_column = issue_column
        self.id_column_name = id_column_name
        self.import_method = import_method
        
        for col_idx in range(len(self.column_names)):
            if spreadsheet_header_from_export_header(self.column_names[col_idx]) == spreadsheet_header_from_export_header(issue_column):
                self.issue_idx = col_idx
        
    def import_rows(self):
        for key_idx in range(len(self.key_values)):
            if self.key_values[key_idx] == GoogleSheetImport.READY_TO_IMPORT:
                row_idx = key_idx + 2
                row_data = self.get_data(row_idx, 0, row_idx, self.colCount)[0]
                
                data = {}
                for col_idx in range(len(self.column_names)):
                    if col_idx >= len(row_data) or row_data[col_idx] == '':
                        data[spreadsheet_header_from_export_header(self.column_names[col_idx])] = None
                    else:
                        data[spreadsheet_header_from_export_header(self.column_names[col_idx])] = row_data[col_idx]
                    
                errList = self.import_method(data)
                if len(errList) > 0:
                    if errList[0] == 'Form already exists':
                        self.update_cell(row_idx, self.key_column_index, GoogleSheetImport.DUPLICATE_IMPORT)
                        self.update_cell(row_idx, self.issue_idx, errList[0])
                    else:
                        self.update_cell(row_idx, self.key_column_index, GoogleSheetImport.REJECTED_IMPORT)
                        sep = ""
                        err_string = ""
                        for err in errList:
                            err_string = err_string + sep + err
                            sep = '\n'
                            
                        self.update_cell(row_idx, self.issue_idx, err_string)
                else:
                    self.update_cell(row_idx, self.key_column_index, GoogleSheetImport.IMPORT_SUCCESS)
                    self.update_cell(key_idx+2, self.issue_idx, " ")
                    
    @staticmethod
    def import_stories():
        import_sheet = GoogleSheetImport(settings.SPREADSHEET_NAME, settings.STORY_WORKSHEET_NAME, 'Import Status', None, 'Import Issues', 'Unique ID', import_story_row)
        import_sheet.import_rows()    