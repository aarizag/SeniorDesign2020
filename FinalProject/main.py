import xlwt
from itertools import chain
from os import path
from utils.load_excel import COMM, UNSPSC, UNSPSC_SLIM, UNSPSC_SLIM_LOC
from utils.compare_excels import compare_from_row

EXTENSION_LOC = '../sample_text/'
BASE_COL = 'Class Title'
E_COMM_COL = 'comm_dscr_up'


def assign_best_to_rows():
    all_rows = []
    wb = UNSPSC_SLIM if path.exists(UNSPSC_SLIM_LOC) else UNSPSC
    wb.set_workbook()
    fields = wb.fields
    additional_fields = [[f'Best_Match #{i}', f'Percent_Similarity #{i}', f'eComm_CD #{i}'] for i in range(1, 6)]
    additional_fields = list(chain.from_iterable(additional_fields))

    count = 0
    for row in wb.get_all_rows():
        if count % 100 == 0:
            print(f'Finished {count} evaluations')
        count += 1

        cur_row_val = [row[f] for f in fields]
        top_sims = compare_from_row(row, COMM, BASE_COL, E_COMM_COL, save_num=5)
        add_vals = [[title, round(sim, 3), ecomm['COMM_CD']] for (sim, title, ecomm) in top_sims[::-1]]
        cur_row_val += list(chain.from_iterable(add_vals))

        all_rows.append(cur_row_val)

    fields += additional_fields

    return all_rows, fields


def write_best_to_file():
    all_rows, fields = assign_best_to_rows()
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet('Main')
    for index, value in enumerate(fields):
        sheet.write(0, index, value)

    print('Writing to file...')

    for i, row in enumerate(all_rows, start=1):
        for j, cell in enumerate(row):
            sheet.write(i, j, cell)

    workbook.save(EXTENSION_LOC + 'UNSPSC_most_similar.xls')


if __name__ == '__main__':
    write_best_to_file()
