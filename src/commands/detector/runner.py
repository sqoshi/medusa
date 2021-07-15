import sys

import termcolor

from src.commands.detector.detector import FaceDetector
from src.templates.runner_abstract import AbstractRunner


class CommandRunner(AbstractRunner):
    def parse_args(self):
        self.insert_default_args()
        self.parser.add_argument(
            "--output-dir",
            type=str,
            default="detected_faces",
            help="Name of directory in which converted images will be saved.",
        )

        self.parser.add_argument(
            "--show-examples",
            type=str,
            default=True,
            help="Name of directory in which converted images will be saved.",
        )

        return self.parser.parse_args(sys.argv[2:])

    def main(self, path, output_directory, logger):
        d = FaceDetector(output_directory, logger)
        d.input(path)
        d.detect_faces()
        logger.log_time("Face detection")
        termcolor.cprint("Face detection finished.", "green")

    def run(self, logger):
        args = self.parse_args()
        if args.filename:
            self.main(args.filename, None, logger)
        elif args.input_dir:
            self.main(args.input_dir, args.output_dir, logger)
        else:
            # temporary
            termcolor.cprint(
                f"Detector requires an --input-dir flag to specify directory of JPEG images."
                f"Using hardcoded path: converted_images",
                "red"
            )
            self.main(
                "converted_images",
                args.output_dir,
                logger
            )
