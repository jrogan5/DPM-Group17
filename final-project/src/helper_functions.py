import threading
import ctypes

def force_kill_thread(thread:threading.Thread, exception_type):
    """Inject an exception into a running thread."""
    tid = thread.ident
    if tid is None:
        raise ValueError("Thread has not started or has already finished.")
    
    res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
        ctypes.c_long(tid), ctypes.py_object(exception_type)
    )
    if res > 1:  # If more than one thread was affected, reset it
        ctypes.pythonapi.PyThreadState_SetAsyncExc(ctypes.c_long(tid), None)
        raise SystemError("PyThreadState_SetAsyncExc failed.")
        