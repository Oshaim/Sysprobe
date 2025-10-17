import os
import ctypes


LIBC = ctypes.CDLL(None, use_errno=True)

# TODO: Check about inotify_init1 for better flags support
LIBC.inotify_init.argtypes = []
LIBC.inotify_init.restype = ctypes.c_int
LIBC.inotify_add_watch.argtypes = [ctypes.c_int, ctypes.c_char_p, ctypes.c_uint32]
LIBC.inotify_add_watch.restype = ctypes.c_int
LIBC.inotify_rm_watch.argtypes = [ctypes.c_int, ctypes.c_uint32]
LIBC.inotify_rm_watch.restype = ctypes.c_int

IN_MODIFY =         0x00000002
IN_MOVED_FROM =     0x00000040
IN_MOVED_TO =       0x00000080
IN_CREATE =         0x00000100
IN_DELETE =         0x00000200
# TODO: ?
IN_DELETE_SELF =    0x00000400
IN_MOVE_SELF =      0x00000800


def watch(path, mask):
    inotify_instance = LIBC.inotify_init()
    assert inotify_instance != -1, "Failed to inotify_init, errno: {}".format(ctypes.get_errno())
    print("inotify instance:", inotify_instance)

    watch_descriptor = LIBC.inotify_add_watch(inotify_instance, path.encode(), mask)
    assert watch_descriptor != -1, "Failed to inotify_add_watch, errno: {}".format(ctypes.get_errno())

    assert LIBC.inotify_rm_watch(inotify_instance, watch_descriptor) != -1, \
        "Failed to inotify_rm_watch, errno: {}".format(ctypes.get_errno())

    os.close(inotify_instance)
    