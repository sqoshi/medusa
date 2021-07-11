import argparse
import sys

import termcolor

from converter.converter import Converter
from handled_types.image_type import ImageExtension


def parse_args(

):
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
    termcolor.cprint(f"Conversion finished. Files saved in {output_directory}", "green")


def run(logger):
    args = parse_args()
    if args.filename:
        main(args.filename, None, str(args.img_ext), logger)
    if args.input_dir:
        main(args.input_dir, args.output_dir, str(args.img_ext), logger)
    # temporary
    termcolor.cprint(
        f"Converter requires an --input-dir flag to specify directory of unconverted images. "
        f"Using hardcoded path: /home/piotr/Documents/bsc-thesis/mc-dataset",
        "red"
    )
    main(
        "/home/piotr/Documents/bsc-thesis/mc-dataset",
        args.output_dir,
        str(args.img_ext),
        logger
    )
