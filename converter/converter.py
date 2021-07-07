import argparse
import os
import sys
from os import listdir, makedirs
from os.path import isfile, join

import termcolor
from PIL import Image

from converter.image_type import ImageExtension
from converter.progress_bar import printProgressBar


class Converter:
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory

    def is_image(self, f):
        return isfile(join(self.input_directory, f)) and any(
            [str(f).endswith(str(ext)) for ext in list(ImageExtension)]
        )

    def find_images(self) -> list:
        if isfile(self.input_directory):
            rs = [self.input_directory]
        else:
            rs = [
                join(self.input_directory, f)
                for f in listdir(self.input_directory)
                if self.is_image(f)
            ]
        return rs

    def input(self, path):
        self.input_directory = path
        self.images_list = self.find_images()
        termcolor.cprint(
            termcolor.colored("Found ", "yellow")
            + termcolor.colored(len(self.images_list), "red")
            + termcolor.colored(" images in ", "yellow")
            + termcolor.colored(self.input_directory, "red")
        )
        if not len(self.images_list):
            exit()

    def standardize_images(self, image_ext):
        if self.output_directory and self.output_directory not in os.listdir():
            makedirs(self.output_directory)

        printProgressBar(
            0, len(self.images_list), prefix="Progress:", suffix="Complete", length=50
        )

        for i, file in enumerate(self.images_list):
            printProgressBar(
                i + 1,
                len(self.images_list),
                prefix="Progress:",
                suffix="Complete",
                length=50,
            )

            name = file.split("/")[-1].split(".")[0]
            img = Image.open(str(file)).convert("RGB")
            output_filename = (
                f"{self.output_directory}/{name}" if self.output_directory else name
            )
            img.save(f"{output_filename}.{image_ext}", image_ext)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str, nargs="?", default=None, help="Single file to convert"
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        default=None,  # os.getcwd(),
        help="Path to directory of images.",
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="converted_images",
        help="Name of directory in which converted images will be saved.",
    )
    parser.add_argument(
        "--img-ext",
        type=ImageExtension,
        choices=list(ImageExtension),
        default=ImageExtension.png,
        help="Specify target image extension.",
    )
    return parser.parse_args(sys.argv[2:])


def main(path, output_directory, image_ext, logger):
    c = Converter(output_directory, logger)
    c.input(path)
    c.standardize_images(image_ext)
    logger.log_time("Conversion")
    termcolor.cprint("Conversion finished.", "green")


def run(logger):
    args = parse_args()
    if args.filename:
        main(args.filename, None, str(args.img_ext), logger)
    elif args.input_dir:
        main(args.input_dir, args.output_dir, str(args.img_ext), logger)
    else:
        # temporary
        termcolor.cprint(
            f"Converter requires an --input-dir flag to specify directory of unconverted images. "
            f"Using hardcoded path: /home/piotr/Documents/bsc-thesis/mc-dataset",
            "red",
        )
        main(
            "/home/piotr/Documents/bsc-thesis/mc-dataset",
            args.output_dir,
            str(args.img_ext),
            logger,
        )


def asd():
    print()
    print()
    print()
    print()
    print()


def xddd():
    t = 1
