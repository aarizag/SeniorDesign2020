from load_excel import COMM, UNSPSC_SLIM, ExcelFile
import time
from utils import compare_sentences as cs

from typing import Dict, Any


def sort(sims):
    if not sims:
        return []
    pivot = sims[0]
    return [l for l in sims[1:] if l[0] < pivot[0]] + [pivot] + [m for m in sims[1:] if m[0] >= pivot[0]]


def compare_excels(excel1: ExcelFile, excel2: ExcelFile, col_name1: str, col_name2: str, save_num=10):
    """
    Get the defined column from a random row from the first Excel File (the base comparator).
        Then iterate through the rows in the second excel files and compare the base comparator
        to the designated column
    The functions of 'compare_excel' has been abstracted into 3 layers:
        'compare_excels': Gets most similar rows in excel2 for a RANDOM row in excel1
        'compare_from_row': Returns most similar rows in excel2 for a given row
        'compare_from_cell': Returns most similar rows in excel2 for a given string
    :return: (Dict[str, Any], List[Tuple[float, str, Dict]])
    """

    base_row = excel1.get_row()
    top_sim = compare_from_row(base_row, excel2, col_name1, col_name2, save_num=save_num)

    return base_row, top_sim


def compare_from_row(base_row: Dict[str, Any], other_excel: ExcelFile, base_col: str, other_col: str, save_num=10):
    base = base_row[base_col]
    return compare_from_cell(base, other_excel, other_col, save_num=save_num)


def compare_from_cell(base: str, other_excel: ExcelFile, other_col: str, save_num=10):
    top_sim = []

    for row in other_excel.get_all_rows():
        similarity = cs.deep_compare(base, row[other_col])
        if len(top_sim) <= save_num or similarity > top_sim[0][0]:
            top_sim.append((similarity, row[other_col], row))
            top_sim = sort(top_sim)
            if len(top_sim) > save_num:
                del top_sim[0]

    return top_sim


if __name__ == "__main__":
    U_COLUMN_NAME = "Class Title"
    COMM_COL_NAME = "COMM_DSCR_UP"

    start = time.time()
    base_row, top_sim = compare_excels(UNSPSC_SLIM, COMM, U_COLUMN_NAME, COMM_COL_NAME)
    print(f'Total time: {time.time()-start}')
    print(base_row)
    print("Class Title:", base_row[U_COLUMN_NAME])
    for sim, col, row in top_sim[::-1]:
        print(f'Similarity: {sim}, COMM_CD: {row["COMM_CD"]}, DESC: {col}')