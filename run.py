import argparse
import sys
from enum import Enum

from converter import converter
from informational_messages.welcome import print_welcome
from logger.time_logger import TimeLogger


class Command(Enum):
    convert = "convert"  # Allow to convert images to specified extension. (Example: jpg -> png)

    def __str__(self):
        return self.value


def main():
    parser = argparse.ArgumentParser(
        description="Python ML/DL package help in images preprocessing."
    )
    parser.add_argument(
        "command",
        type=Command,
        choices=list(Command),
        help="Command option.",
    )
    args = parser.parse_args(sys.argv[1:2])

    print_welcome()
    logger = TimeLogger()
    if args.command is Command.convert:
        converter.run(logger)
