import contextlib
import os
import subprocess
import time
from contextlib import contextmanager


DEBUGFS_PATH = "/sys/kernel/debug"
TRACING_PATH = os.path.join(DEBUGFS_PATH, "tracing")
TRACE_PIPE_PATH = os.path.join(TRACING_PATH, "trace_pipe")


@contextmanager
def _enable_event(event_path):
    event_enable_path = os.path.join(event_path, "enable")
    
    with open(event_enable_path, "w") as enable_file:
        enable_file.write("1")
        enable_file.flush()
        try:
            yield
        finally:
            enable_file.write("0")
            enable_file.flush()

def _read_trace_pipe(duration):
    with open(TRACE_PIPE_PATH, "r") as trace_pipe:
        start_time = time.time()    
        while time.time() - start_time < duration:
            print(trace_pipe.readline(), end="")
            
def trace(duration):
    if not os.path.ismount(DEBUGFS_PATH):
        subprocess.run(["mount", "-t", "debugfs", "none", "/sys/kernel/debug"], check=True)

    events = ["/sys/kernel/debug/tracing/events/syscalls/sys_enter_write"]

    with contextlib.ExitStack() as stack:
        for event in events:
            stack.enter_context(_enable_event(event))

        _read_trace_pipe(duration)
    