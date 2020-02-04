from typing import Optional, Any, List, Dict

import xlrd
import random

UNSPSC_LOC = "../sample_text/UNSPSC English v220601 project.xlsx"
UNSPSC_SLIM_LOC = "../sample_text/UNSPSC_randSample.xls"
COMM_LOC = "../sample_text/eCAPS_COMM_11072019.xlsx"


class ExcelFile:
    def __init__(self, loc, wb=None, sheet_no=0, start_row=0, fields=None):
        self.loc = loc
        self.wb: Optional[xlrd.Book] = wb
        self.sheet_no = sheet_no
        self.start_row = start_row
        self.fields = [] if fields is None else fields

    def set_workbook(self):
        self.wb = xlrd.open_workbook(self.loc)
        sheet_no, field_row = self.sheet_no, self.start_row

        sheet = self.wb.sheet_by_index(sheet_no)

        if not self.fields:
            for i in range(sheet.ncols):
                self.fields.append(sheet.cell_value(field_row, i))
            self.start_row = field_row + 1

    def get_rand_cell(self, column) -> Any:
        row = self.get_row()
        return row[column]

    def get_row(self, row_num: Optional[int] = None) -> Dict[str, Any]:
        if self.wb is None:
            self.set_workbook()

        sheet = self.wb.sheet_by_index(self.sheet_no)

        if row_num is None:
            row_num = random.randint(self.start_row, sheet.nrows)
        row = {}

        for i, val in enumerate(sheet.row_values(row_num)):
            row[self.fields[i]] = val

        return row

    def get_all_rows(self) -> List[Dict[str, Any]]:
        if self.wb is None:
            self.set_workbook()

        rows = []
        sheet = self.wb.sheet_by_index(self.sheet_no)

        for i in range(self.start_row, sheet.nrows):
            rows.append(self.get_row(row_num=i))
        return rows


UNSPSC = ExcelFile(UNSPSC_LOC, start_row=12)
UNSPSC_SLIM = ExcelFile(UNSPSC_SLIM_LOC)
COMM = ExcelFile(COMM_LOC, sheet_no=2)
