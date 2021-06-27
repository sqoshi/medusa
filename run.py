import argparse
import shutil
from enum import Enum

import termcolor

from converter import converter


def print_welcome():
    limit = shutil.get_terminal_size().columns
    welcome_msg = "Welcome in medusa. 🐍️"
    spacer = int((limit - len(welcome_msg)) / 2) * " "
    print(limit * '=')
    termcolor.cprint(spacer + welcome_msg, "green")
    print(limit * '=')


class ImageExtension(Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    webp = "webp"

    def __str__(self):
        return self.value


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
    parser.add_argument('--dir',
                        type=str,
                        default=None,
                        help="Path to directory of images.")
    parser.add_argument('--img-ext',
                        type=ImageExtension,
                        default=ImageExtension.png,
                        help="Specify goal image extension.")

    args = parser.parse_args()

    print_welcome()

    if args.command is Command.convert:
        if args.dir:
            converter.run(args.dir, args.img_ext)
        else:
            termcolor.cprint(
                f"Converter requires a --dir flag to specify directory of unconverted images.\n"
                f" Using hardcoded path: /home/piotr/Documents/bsc-thesis/mc-dataset",
                "red")
            converter.run("/home/piotr/Documents/bsc-thesis/mc-dataset", args.img_ext)
