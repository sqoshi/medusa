import argparse
import shutil
import sys
from enum import Enum

import termcolor

from converter import converter


def print_welcome():
    limit = shutil.get_terminal_size().columns
    welcome_msg = "Welcome in medusa. 🐍️"
    spacer = int((limit - len(welcome_msg)) / 2) * " "
    print(limit * "=")
    termcolor.cprint(spacer + welcome_msg, "green")
    print(limit * "=")


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

    if args.command is Command.convert:
        converter.run()
