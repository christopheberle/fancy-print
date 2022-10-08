import time
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
    MessageType.OKAY : "[" + bcolors.OKGREEN + "OKAY" + bcolors.ENDC + "]",
    MessageType.WARN : "[" + bcolors.WARNING + "WARN" + bcolors.ENDC + "]",
    MessageType.FAIL : "[" + bcolors.FAIL + "FAIL" + bcolors.ENDC + "]",
    MessageType.INFO : "[" + bcolors.OKCYAN + "INFO" + bcolors.ENDC + "]",
    MessageType.BUSY : "[" + bcolors.OKCYAN + "BUSY" + bcolors.ENDC + "]",
    MessageType.DONE : "[" + bcolors.OKGREEN + "DONE" + bcolors.ENDC + "]",
    MessageType.BULLET : " --->"
}
    
CHECKMARK = f"[{bcolors.OKGREEN}✔︎{bcolors.ENDC}] "
FAILMARK = f"[{bcolors.FAIL}x{bcolors.ENDC}] "

@staticmethod
def _print(msg, mtype : MessageType, end = "\n"):
    print("".join([_msgtypedict[mtype], "\t", msg]), end=end)

@staticmethod
def print_ok(msg=""):
    _print(msg, mtype=MessageType.OKAY)

@staticmethod
def print_error(msg=""):
    _print(msg, mtype=MessageType.FAIL)

@staticmethod
def print_warning(msg=""):
    _print(msg, mtype=MessageType.WARN)

@staticmethod
def print_info(msg=""):
    _print(msg, mtype=MessageType.INFO)

@staticmethod
def print_bullet(msg):
    _print(msg, mtype=MessageType.BULLET)
class PendingTaskContext():
    def __init__(self, desc="", verbose=True):
        self.desc = desc
        self.verbose = verbose

    def __enter__(self):
        if self.verbose:
            _print(self.desc, MessageType.BUSY, end="\r")
            time.sleep(0.5)
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_value == None:
            if self.verbose:
                _print(self.desc, MessageType.DONE)
        else:
            if self.verbose:
                _print(self.desc, MessageType.FAIL)
                _print(f"ERROR: {str(exc_value)}", MessageType.FAIL)
        return True
        