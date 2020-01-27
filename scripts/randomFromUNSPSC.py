import xlrd
import xlwt
import random

FILE_NAME = "../sample_text/UNSPSC English v220601 project.xlsx"
EXTENSION_LOC = '../sample_text/'
FIELDS = []


def group_by(column_name="Family Title"):
    wb = xlrd.open_workbook(FILE_NAME)
    sheet = wb.sheets()[0]

    sheet.cell_value(0, 0)
    groups = {}

    for i in range(sheet.ncols):
        FIELDS.append(sheet.cell_value(12, i))

    for i in range(13, sheet.nrows):
        row = {}
        for j, val in zip(range(sheet.ncols), sheet.row_values(i)):
            row[FIELDS[j]] = val
        if row[column_name] not in groups:
            groups[row[column_name]] = []
        groups[row[column_name]].append(row)

    return groups


def write_from_group(groups, n=2, output='randSample.xls'):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Main')
    for index, value in enumerate(FIELDS):
        sheet.write(0, index, value)

    j = 1
    for k, rows in groups.items():
        if len(rows) < n:
            sample = rows
        else:
            sample = random.sample(rows, n)
        for row in sample:
            for i, field in enumerate(FIELDS):
                sheet.write(j, i, row[field])
            j += 1

    workbook.save(EXTENSION_LOC + output)


write_from_group(group_by())

