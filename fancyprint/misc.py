from .utils import bcolors

def color_num_by_val(val, threshold=0, col_above=bcolors.OKGREEN, col_below=bcolors.FAIL, col_equal=bcolors.WARNING, decimals=None):
    match val:
        case _ if val > threshold:
            col = col_above
        case _ if val < threshold:
            col = col_below
        case _:
            col = col_equal
    if decimals is not None:
        return f"{col}{round(val, decimals)}{bcolors.ENDC}"
    return f"{col}{val}{bcolors.ENDC}"