import argparse

from Commands.watch import InotifyEvent, watch


def parse_args():
    parser = argparse.ArgumentParser()

    subparser = parser.add_subparsers(dest="command", required=True, help="The command to run")
    watch_command = subparser.add_parser("watch", help="Monitor a given directory for create/modify/move/delete events")
    watch_command.add_argument("--dir", type=str, default=".", help="The directory to monitor")
    watch_command.add_argument("--timeout", type=int, default=20, help="The monitoring duration of the directory (in seconds)")

    return parser.parse_args()

def main(args):
    if args.command == "watch":
        watch(args.dir, 
              InotifyEvent.IN_MODIFY | InotifyEvent.IN_CREATE | InotifyEvent.IN_DELETE | InotifyEvent.IN_DELETE_SELF | InotifyEvent.IN_MOVED_FROM | InotifyEvent.IN_MOVED_TO,
              args.timeout)

if __name__ == "__main__":
    args = parse_args()
    main(args)
