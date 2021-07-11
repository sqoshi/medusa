import argparse
import sys

import termcolor

from detector.detector import FaceDetector


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "filename", type=str, nargs="?", default=None, help="Single file to detect face."
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
        default="detected_faces",
        help="Name of directory in which converted images will be saved.",
    )

    parser.add_argument(
        "--show-examples",
        type=str,
        default=True,
        help="Name of directory in which converted images will be saved.",
    )

    return parser.parse_args(sys.argv[2:])


def main(path, output_directory, logger):
    d = FaceDetector(output_directory, logger)
    d.input(path)
    d.detect_faces()
    logger.log_time("Face detection")
    termcolor.cprint("Face detection finished.", "green")


def run(logger):
    args = parse_args()
    if args.filename:
        main(args.filename, None, logger)
    if args.input_dir:
        main(args.input_dir, args.output_dir, logger)
    # temporary
    termcolor.cprint(
        f"Converter requires an --input-dir flag to specify directory of JPEG images."
        f"Using hardcoded path: converted_images",
        "red"
    )
    main(
        "converted_images",
        args.output_dir,
        logger
    )
