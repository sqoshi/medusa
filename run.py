import argparse
import sys
from enum import Enum

from src.beautifiers.printers import print_header
from src.commands.converter import converter, detector
from src.loggers.logger import Logger


class Command(Enum):
    convert = "convert"  # Allow to convert images to specified extension. (Example: jpg -> png)
    detect = "detect"  # Allow to detect faces on images. ( ONLY ON JPEG/JPG IMAGES)

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

    print_header()
    logger = Logger()
    if args.command is Command.convert:
        converter.runner.run(logger)
    elif args.command is Command.detect:
        detector.runner.run(logger)

    print_header("See you soon in medusa!")
