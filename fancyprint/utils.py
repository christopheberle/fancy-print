from enum import Enum

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    
class MessageType(Enum):
    NONE = -1
    OKAY = 0
    WARN = 1
    FAIL = 2
    INFO = 3
    BUSY = 4
    DONE = 5
    BULLET = 6
    
_msgtypedict = {
    MessageType.NONE : "",
    MessageType.OKAY :  f"[{bcolors.OKGREEN}OKAY{bcolors.ENDC}]",
    MessageType.WARN :  f"[{bcolors.WARNING}WARN{bcolors.ENDC}]",
    MessageType.FAIL :  f"[{bcolors.FAIL}FAIL{bcolors.ENDC}]",
    MessageType.INFO :  f"[{bcolors.OKCYAN}INFO{bcolors.ENDC}]",
    MessageType.BUSY : f"[{bcolors.OKCYAN}BUSY{bcolors.ENDC}]", 
    MessageType.DONE :  f"[{bcolors.OKGREEN}DONE{bcolors.ENDC}]",
    MessageType.BULLET : " --->"
}

_msgtype_str_dict = {
    MessageType.OKAY :  f"OKAY",
    MessageType.WARN :  f"WARN",
    MessageType.FAIL :  f"FAIL",
    MessageType.INFO :  f"INFO",
}

_msgtype_color_dict = {
    MessageType.OKAY :  bcolors.OKGREEN,
    MessageType.WARN :  bcolors.WARNING,
    MessageType.FAIL :  bcolors.FAIL,
    MessageType.INFO :  bcolors.OKCYAN
}