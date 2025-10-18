import argparse

from .commands.trace import trace
from .commands.watch import InotifyEventMask, watch


def parse_args():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="command", required=True, help="The command to run")
    watch_command = subparser.add_parser("watch", help="Monitor a given directory for create/modify/move/delete events")
    watch_command.add_argument("--dir", type=str, default=".", help="The directory to monitor")
    watch_command.add_argument("--secs", type=int, default=20, help="The monitoring duration of the directory (in seconds)")
    trace_command = subparser.add_parser("trace", help="Trace pre-selected events of debugfs")
    trace_command.add_argument("--secs", type=int, default=5, help="The tracing duration (in seconds)")

    return parser.parse_args()

def main(args):
    if args.command == "watch":
        watch(args.dir, 
              InotifyEventMask.IN_MODIFY | InotifyEventMask.IN_CREATE | InotifyEventMask.IN_DELETE | InotifyEventMask.IN_DELETE_SELF | InotifyEventMask.IN_MOVED_FROM | InotifyEventMask.IN_MOVED_TO,
              args.secs)
    elif args.command == "trace":
        trace(args.secs)
    else:
        raise ValueError(f"Unknown command: {args.command}")

if __name__ == "__main__":
    args = parse_args()
    main(args)
