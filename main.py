import argparse

from Commands.watch import InotifyEvent, watch


def main():
    watch(".", 
          InotifyEvent.IN_MODIFY | InotifyEvent.IN_CREATE | InotifyEvent.IN_DELETE | InotifyEvent.IN_DELETE_SELF | InotifyEvent.IN_MOVED_FROM | InotifyEvent.IN_MOVED_TO,
          20)

def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main()
