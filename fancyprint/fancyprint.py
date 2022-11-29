import os
import sys
import threading
from functools import partial
import itertools as its
from time import sleep
from .utils import Symbols, TermColors, MessageType, _msgtype_color_dict, _msgtype_str_dict, Fancyfier
from .indicators import busyAnimations
import traceback   
from functools import partial
from contextlib import redirect_stdout

_force_print = partial(print, flush=True)
max_mtype_len = max(len(el.value) for el in MessageType)

def print_message_type(message, message_type : MessageType, end = "\n"):
    print(f"{_msgtype_color_dict[message_type]}{Symbols.SINGLE_CHUNK} {message_type.value.ljust(max_mtype_len)}:{TermColors.ENDC} {message}", end=end)

def print_ok(message):
    print_message_type(message, message_type=MessageType.OKAY)

def print_error(message):
    print_message_type(message, message_type=MessageType.FAIL)

def print_warning(message):
    print_message_type(message, message_type=MessageType.WARN)

def print_info(message):
    print_message_type(message, message_type=MessageType.INFO)
    
def print_debug(message):
    print_message_type(message, message_type=MessageType.DEBUG)
    

class ExtendableContext:
    def __init__(
        self, 
        message = None, 
        message_type : MessageType = None, 
        single=False
        ) -> None:
        if (message_type is None) ^ (message is None):
            raise ValueError(f"If `message` is provided, `message_type` must also be provided and vice-versa")
        
        self.message = message
        self.message_type = message_type
        self.curr_chunk_is_single = single
        self.orig_stdout = sys.stdout
            
        if message is not None:
            if (message_type not in MessageType):
                raise ValueError(f"Requested message type {message_type} is not supported. Supported types are {self._supported_message_types}")
            self.indicator_color = _msgtype_color_dict[message_type]
            self.status_str = message_type.value.ljust(max_mtype_len)
            self._start_chunk(message, message_type, single)
        else:
            self.chunk_open = False
        
        
    def _safe_print(self, message):
        with redirect_stdout(sys.__stdout__):
            print(message)
            
    def __enter__(self):
        if self.message is not None and not self.chunk_open:
            self.chunk_open = True
            self._start_chunk(self.message, self.message_type)
        return self
    
    def __exit__(self, exc_type, exc_value, exc_traceback):
        if exc_type is not None:
            self.new_chunk("An Exception occured", MessageType.FAIL)
            self.extend(f"Exception type: {exc_type.__name__}")
            self.extend(f"Exception description: {exc_value}")
            self.extend(f"Traceback:")
            tb_split = [l.split("\n") for l in traceback.format_tb(exc_traceback)]
            tb_flattened = [item for sublist in tb_split for item in sublist]
            for line in tb_flattened:
                self.extend(line)#.replace("\n", ""))
        self._end_chunk()
        
    def _end_chunk(self):
        """Ends the current chunk. Will be automatically called on exit of the context. Should not be called manually.
        """
        if not self.curr_chunk_is_single:
            self._safe_print(f"{self.indicator_color}{Symbols.END_CHUNK}{TermColors.ENDC}")
        
    def _start_chunk(self, message, message_type, single=False):
        """Prints a new chunk without overwriting the current settings. Should not be called manually. Use `new_chunk()` instead.

        Parameters
        ----------
        message : str
            The message to be printed
        message_type : fancyprint.MessageType
            The type of message to be indicated
        single : bool, optional
            Whether to print a single message chunk or a chunk that can contain multiple lines, by default False
        """
        self.chunk_open = True
        self.curr_chunk_is_single = single
        self.status_str = message_type.value.ljust(max_mtype_len)
        self._safe_print(f"{_msgtype_color_dict[message_type]}{Symbols.START_CHUNK if not single else Symbols.SINGLE_CHUNK} {self.status_str}:{TermColors.ENDC} {message}")
        
    
    def extend(self, message):
        """Prints a new message within the current chunk.

        Parameters
        ----------
        message : str
            The message to be printed
        """
        if not self.chunk_open:
            raise RuntimeError("No open chunk found to attach the current message to. Create a new chunk first with `new_chunk()`")
        self._safe_print(f"{self.indicator_color}{Symbols.CONT_CHUNK}{TermColors.ENDC}{(3+len(self.status_str))*' ' }{message}")
        
    def print_in_chunk(self, message, message_type):
        """Prints a single message of possibly different MessageType than the parent chunk without creating a new chunk.

        Parameters
        ----------
        message : str
            The message to be printed
        message_type : fancyprint.MessageType
            The type of message to be indicated
        """
        self._safe_print(f"{_msgtype_color_dict[self.message_type]}{Symbols.CONT_CHUNK}{_msgtype_color_dict[message_type]} {message_type.value.ljust(max_mtype_len)}:{TermColors.ENDC} {message}")
        
    def new_chunk(self, message, message_type, single=False):
        """Starts a new chunk overwriting the current settings.

        Parameters
        ----------
        message : str
            The message to be printed
        message_type : fancyprint.MessageType
            The type of message to be indicated
        single : bool, optional
            Whether to print a single message chunk or a chunk that can contain multiple lines, by default False
        """
        if self.chunk_open:
            self._end_chunk()
        else:
            self.chunk_open = True
        self.message = message
        self.message_type = message_type
        self.indicator_color = _msgtype_color_dict[message_type]
        self.status_str = message_type.value.ljust(max_mtype_len)
        self._start_chunk(self.message, self.message_type, single)
        
class PendingTaskContext():    
    def __init__(self, desc="", anim=None, total_progress=None):
        self.desc = desc
        self.anim = anim
        self.busy = False
        if self.anim is None:
            self.print_thread = AsyncBusyIndicator(self.desc, total_progress=total_progress, daemon=True) 
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
                self._update_pending = False
                _print(" " * len(self._print_str), MessageType.BUSY, end="\r") # clears the current line
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
                self._update_pending = False
                print((2 + len(next_frame) + len(self.desc)) * "", end="\r") # clears the current line
            print(f"[{next_frame}]\t{self._print_str}", end="\r")
            sys.stdout.flush()
            sleep(self.tick_rate)

        