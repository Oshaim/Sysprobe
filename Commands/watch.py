import errno
import os
import ctypes
import struct
import time
from enum import IntFlag


LIBC = ctypes.CDLL(None, use_errno=True)

# TODO: Check about inotify_init1 for better flags support
LIBC.inotify_init.argtypes = []
LIBC.inotify_init.restype = ctypes.c_int
LIBC.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
LIBC.inotify_add_watch.restype = ctypes.c_int
LIBC.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_uint32]
LIBC.inotify_rm_watch.restype = ctypes.c_int

# The format of inotify_event struct without the name field
INOTIFY_EVENT_HEADER_FORMAT = "iIII"


class InotifyEvent(IntFlag):
    IN_MODIFY       = 0x00000002
    IN_MOVED_FROM   = 0x00000040
    IN_MOVED_TO     = 0x00000080
    IN_CREATE       = 0x00000100
    IN_DELETE       = 0x00000200
    # TODO: ?
    IN_DELETE_SELF  = 0x00000400
    IN_MOVE_SELF    = 0x00000800


def _read_inotify_events(inotify_fd, duration):
    start_time = time.time()
    
    while time.time() - start_time < duration:
        try:
            event_buffer = os.read(inotify_fd, 1024)
            for _, mask, _, name in _parse_inotify_event(event_buffer):
                # TODO: Add the directory path prefix
                print("{}\t{}\t{}".format(
                    time.strftime("%Y-%m-%dT%H:%M:%SZ"), InotifyEvent(mask).name, name.decode()
                ))
        except OSError as e:
            if e.errno == errno.EINTR:
                continue

def _parse_inotify_event(event_buffer):
    # Get the size of inotify_event struct without the name field
    header_size = struct.calcsize(INOTIFY_EVENT_HEADER_FORMAT)
    
    i = 0    
    while i + header_size <= len(event_buffer):
        wd, mask, cookie, name_length = struct.unpack_from(INOTIFY_EVENT_HEADER_FORMAT, event_buffer, i)

        name_start_offset = i + header_size
        name = event_buffer[name_start_offset:(name_start_offset + name_length)].rstrip(b"\0")

        i += header_size + name_length
        yield wd, mask, cookie, name

def watch(path, mask, duration):
    # TODO: If path doesn't exist, create it
    inotify_fd = LIBC.inotify_init()
    assert inotify_fd != -1, "Failed to inotify_init, errno: {}".format(ctypes.get_errno())
    print("inotify instance:", inotify_fd)

    watch_descriptor = LIBC.inotify_add_watch(inotify_fd, path.encode(), mask)
    assert watch_descriptor != -1, "Failed to inotify_add_watch, errno: {}".format(ctypes.get_errno())

    _read_inotify_events(inotify_fd, duration)
        
    assert LIBC.inotify_rm_watch(inotify_fd, watch_descriptor) != -1, \
        "Failed to inotify_rm_watch, errno: {}".format(ctypes.get_errno())

    os.close(inotify_fd)
    