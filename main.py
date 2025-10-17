import argparse

from Commands.watch import (IN_CREATE, IN_DELETE, IN_DELETE_SELF, IN_MODIFY, IN_MOVED_FROM, IN_MOVED_TO, 
                            watch)

def main():
    watch(".", IN_MODIFY | IN_CREATE | IN_DELETE | IN_DELETE_SELF | IN_MOVED_FROM | IN_MOVED_TO)

def parse_args():
    parser = argparse.ArgumentParser()
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    main()
