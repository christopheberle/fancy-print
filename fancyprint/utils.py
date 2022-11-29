from enum import Enum
from contextlib import redirect_stdout
import sys

class Fancyfier:
    """
    Fake file-like stream object that redirects prints to fancyprint.
    """
    
    def __init__(self, print_fn):
        self.print_fn = print_fn

    def write(self, buf):
        # temporarily redirect output back to stdout
        with redirect_stdout(sys.__stdout__):
            for line in buf.rstrip().splitlines():
                self.print_fn(line)
class Symbols:
    START_CHUNK = "┌"
    CONT_CHUNK = "│"
    END_CHUNK = "└"
    SINGLE_CHUNK = "["
class TermColors:
    BLACK = "\033[30m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    MAGENTA = "\033[35m"
    CYAN = "\033[36m"
    LIGHT_GREY = "\033[37m"
    GREY = "\033[90m"
    BRIGHT_RED = "\033[91m"
    BRIGHT_GREEN = "\033[92m"
    BRIGHT_YELLOW = "\033[93m"
    BRIGHT_BLUE = "\033[94m"
    BRIGHT_MAGENTA = "\033[95m"
    BRIGHT_CYAN = "\033[96m"
    WHITE = "\033[97m"
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class MessageType(Enum):
    NONE = "NONE"
    OKAY = "OKAY"
    WARN = "WARN"
    FAIL = "FAIL"
    INFO = "INFO"
    BUSY = "BUSY"
    DONE = "DONE"
    DEBUG = "DEBUG"
    
_msgtype_str_dict = {
    MessageType.OKAY :  f"OKAY",
    MessageType.WARN :  f"WARN",
    MessageType.FAIL :  f"FAIL",
    MessageType.INFO :  f"INFO",
    MessageType.DEBUG : f"DEBUG"
}

_msgtype_color_dict = {
    MessageType.OKAY :  TermColors.BRIGHT_GREEN,
    MessageType.WARN :  TermColors.BRIGHT_YELLOW,
    MessageType.FAIL :  TermColors.BRIGHT_RED,
    MessageType.INFO :  TermColors.BRIGHT_CYAN,
    MessageType.DEBUG : TermColors.MAGENTA
}