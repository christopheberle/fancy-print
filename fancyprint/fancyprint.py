import os
import sys
import threading
from functools import partial
import itertools as its
from time import sleep
from .utils import bcolors, MessageType, _msgtypedict
from .indicators import busyAnimations
# from .threading import AsyncBusyIndicator    
    
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
    def __init__(self, desc="", anim=None, total_progress=None):
        self.desc = desc
        self.anim = anim
        self.busy = False
        if self.anim is None:
            self.print_thread = AsyncBusyIndicator(self.desc, total_progress=total_progress, daemon=True) #threading.Thread(target=partial(_print, self.desc, MessageType.BUSY, end="\r"), daemon=True)
        else:
            self.print_thread = AsyncAnimatedBusyIndicator(self.desc, self.anim, total_progress=total_progress, daemon=True)
            
    def update(self, desc):
        self.desc = desc
        self.print_thread.update(desc)
        
    def __enter__(self):
        self.busy = True
        self.print_thread.start()
        return self

    def __exit__(self, exc_type, exc_value, exc_traceback):
        self.busy = False
        self.print_thread.stop()
        self.print_thread.join()
        if exc_value == None:
            _print(self.desc, MessageType.DONE)
        else:
            self._print_error_fancy(exc_type, exc_value, exc_traceback)
        
    def _print_error_fancy(self, exc_type, exc_value, exc_traceback):
        _print(self.desc, MessageType.FAIL)
        _print(f"ERROR: {str(exc_value)}", MessageType.FAIL)
        exc_traceback.print_tb()
        
    def update_progress(self, val):
        self.print_thread.update_progress(val)
            

class NoPrint:
    """Suppresses print statements of functions encapsulated within this context.
    """
    def __enter__(self):
        self._default_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        
    def __exit__(self, exc_type, exc_value, exc_traceback):
        sys.stdout.close()
        sys.stdout = self._default_stdout
        
class AsyncBusyIndicator(threading.Thread):
    
    def __init__(self, desc, *args, total_progress=None, tick_rate = 0.3, **kwargs):
        self.desc = desc
        self.total_progress = total_progress
        self._progress_str = "" if total_progress is None else f"(0/{total_progress})"
        self._print_str = f"{self.desc} {self._progress_str}"
        self._busy = False
        self._update_pending = False
        self.tick_rate = tick_rate
        super().__init__(*args, **kwargs)
        
    def run(self):
        self._busy = True
        _print(self._print_str, MessageType.BUSY, end="\r")
        
        while self._busy:
            if self._update_pending:
                _print(" " * len(self._print_str), MessageType.BUSY, end="\r")
                _print(self._print_str, MessageType.BUSY, end="\r")
            sleep(self.tick_rate)
    
    def update(self, new_desc):
        self.desc = new_desc
        self._print_str = f"{self.desc} {self._progress_str}"
        self._update_pending = True
        
    def update_progress(self, val):
        self._progress_str = f"({val}/{self.total_progress})"
        self._print_str = f"{self.desc} {self._progress_str}"
        self._update_pending = True
        
    def stop(self):
        self._busy = False
        
class AsyncAnimatedBusyIndicator(AsyncBusyIndicator):
    
    def __init__(self, desc, animation, *args, **kwargs):
        self.anim_iter = busyAnimations.get_iter_from_name(animation)
        super().__init__(desc, *args, **kwargs)
        
    def run(self):
        self._busy = True
        
        while self._busy:
            next_frame = next(self.anim_iter)
            if self._update_pending:
                print((2 + len(next_frame) + len(self.desc)) * "", end="\r")
            print(f"[{next_frame}]\t{self._print_str}", end="\r")
            sys.stdout.flush()
            sleep(self.tick_rate)

        