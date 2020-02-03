from load_excel import COMM, UNSPSC_SLIM
import compare_sentences as cs

U_COLUMN_NAME = "Class Title"
BASE_COL_NAME = "COMM_DSCR_UP"


def compare_rand():
    """
    Get a random row from the UNSPSC file and sort rows in the eComm xls by similarity
        based on the "COMM_DSCR_UP" column
    :return: None
    """

    base_row = UNSPSC_SLIM.get_row()
    base = base_row[U_COLUMN_NAME]
    deep_sim = []

    for row in COMM.get_all_rows():
        similarity = cs.deep_compare(base, row[BASE_COL_NAME])
        deep_sim.append((similarity, row[BASE_COL_NAME]))

    deep_sim.sort()

    print(base_row)
    print(base)
    for s in deep_sim[::-1][:10]:
        print(s)


if __name__ == "__main__":
    compare_rand()
