import os
import sys
import threading
from functools import partial
import itertools as its
from time import sleep
from .utils import bcolors, MessageType, _msgtypedict
from .indicators import busyAnimations
    
CHECKMARK = f"[{bcolors.OKGREEN}✔︎{bcolors.ENDC}]"
FAILMARK = f"[{bcolors.FAIL}x{bcolors.ENDC}]"

def _print(msg, mtype : MessageType, end = "\n"):
    print("".join([_msgtypedict[mtype], "\t", msg]), end=end)

def print_ok(msg=""):
    _print(msg, mtype=MessageType.OKAY)

def print_error(msg=""):
    _print(msg, mtype=MessageType.FAIL)

def print_warning(msg=""):
    _print(msg, mtype=MessageType.WARN)

def print_info(msg=""):
    _print(msg, mtype=MessageType.INFO)

def print_bullet(msg):
    _print(msg, mtype=MessageType.BULLET)
            
class PendingTaskContext():    
    def __init__(self, desc="", anim=None):
        self.desc = desc
        self.anim = anim
        self.busy = False
        if self.anim is None:
            self.print_thread = threading.Thread(target=partial(_print, self.desc, MessageType.BUSY, end="\r"), daemon=True)
        else:
            self.print_thread = threading.Thread(target=self.animation, daemon=True)
        
    def __enter__(self):
        self.busy = True
        self.print_thread.start()

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.busy = False
        self.print_thread.join()
        if exc_value == None:
            _print(self.desc, MessageType.DONE)
        else:
            self._print_error_fancy(exc_type, exc_value, exc_traceback)
        
    def _print_error_fancy(self, exc_type, exc_value, exc_traceback):
        _print(self.desc, MessageType.FAIL)
        _print(f"ERROR: {str(exc_value)}", MessageType.FAIL)
        exc_traceback.print_tb()
        
    def animation(self):
        it = busyAnimations.get_iter_from_name(self.anim)
        while self.busy:
            print(f"[{next(it)}]\t{self.desc}", end="\r")
            sys.stdout.flush()
            sleep(0.35)

class NoPrint:
    """Suppresses print statements of functions encapsulated within this context.
    """
    
    def __enter__(self):
        self._default_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout.close()
        sys.stdout = self._default_stdout