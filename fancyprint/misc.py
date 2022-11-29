from .utils import TermColors

def color_num_by_val(val, threshold=0, col_above=TermColors.BRIGHT_GREEN, col_below=TermColors.BRIGHT_YELLOW, col_equal=TermColors.BRIGHT_YELLOW, decimals=None, sign=False):
    """Returns a number as a colored string where the color depends on whether the number if above, below or equal to the provided threshold.

    Parameters
    ----------
    val : int or float
        The number to be colored.
    threshold : int or float, optional
        The threshold with respect to which the color should be chosen, by default 0
    col_above : str, optional
        The color to chose if the number provided is above the threshold. Use fancyprint.utils.TermColors. By default fancyprint.utils.TermColors.BRIGHT_GREEN
    col_below : _type_, optional
        The color to chose if the number provided is below the threshold. Use fancyprint.utils.TermColors. By default fancyprint.utils.TermColors.BRIGHT_YELLOW
    col_equal : _type_, optional
        The color to chose if the number provided is equal to the threshold. Use fancyprint.utils.TermColors. By default fancyprint.utils.TermColors.BRIGHT_YELLOW
    decimals : int, optional
        If provided the number provided will be rounded to `decimals` decimals before conversion to string, by default None
    sign : bool, optional
        If True the number will be returned as a signed string, i.e. if `val` is 3 then '+3' will be returned, by default False

    Returns
    -------
    str
        A colored string.
    """
    col = None
    sign_str = None
    match val:
        case _ if val > threshold:
            col = col_above
            sign_str = "+"
        case _ if val < threshold:
            col = col_below
            sign_str = "±"
        case _:
            sign_str = ""
            col = col_equal
    if decimals is not None:
        return_str = f"{col}{round(val, decimals)}{TermColors.ENDC}"
    else:
        return_str = f"{col}{val}{TermColors.ENDC}"
    
    return f"{sign_str if sign else ''}{return_str}"