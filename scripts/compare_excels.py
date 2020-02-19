from load_excel import COMM, UNSPSC_SLIM, UNSPSC, ExcelFile
import time
import compare_sentences as cs


def compare_excels(excel1: ExcelFile, excel2: ExcelFile, col_name1: str, col_name2: str, save_num=10):
    """
    Get the defined column from a random row from the first Excel File (the base comparator).
        Then iterate through the rows in the second excel files and compare the base comparator
        to the designated column
    :return: None
    """

    base_row = excel1.get_row()
    base = base_row[col_name1]
    top_sim = []

    for row in excel2.get_all_rows():
        similarity = cs.deep_compare(base, row[col_name2])
        if len(top_sim) <= save_num or similarity > top_sim[0][0]:
            top_sim.append((similarity, row[col_name2], row))
            top_sim.sort()
            if len(top_sim) > save_num:
                del top_sim[0]
    #
    # print(base_row)
    # print(base)
    return base_row, top_sim


if __name__ == "__main__":
    U_COLUMN_NAME = "Class Title"
    COMM_COL_NAME = "COMM_DSCR_UP"

    start = time.time()
    base_row, top_sim = compare_excels(UNSPSC_SLIM, COMM, U_COLUMN_NAME, COMM_COL_NAME)
    print(f'Total time: {time.time()-start}')
    print(base_row)
    print("Class Title:", base_row[U_COLUMN_NAME])
    for sim, col, row in top_sim[::-1]:
        print(f'Similarity: {sim}, DESC: {col}')
        for k in ['COMM_CD', 'COMM_CLS', 'COMM_ITM']:
            print(f'{k}: {row[k]}', end=", ")
        print()
