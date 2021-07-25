from termcolor import cprint

from medusa.abstract_models.abstract_runner import AbstractRunner
from medusa.commands.landmarks_detector.detector_5.detector import Landmarks5Detector
from medusa.definitions import LandmarksFormat


class CommandRunner(AbstractRunner):
    def parse_args(self, terminal_arguments=None):
        terminal_arguments = super().parse_args(terminal_arguments)
        self.insert_input_file_arg()
        self.insert_input_dir_arg()
        self.parser.add_argument(
            "--output-filename",
            type=str,
            default=None,
            help="Output filename with landmarks coordinates.",
        )
        self.parser.add_argument(
            "--output-format",
            type=str,
            choices=list(LandmarksFormat),
            default=LandmarksFormat.csv,
            help="Output file format/extension.",
        )
        self.parser.add_argument(
            "--mode"
        )

        return self.parser.parse_args(terminal_arguments)

    def main(self, path, output_directory, img_size, image_ext, logger):
        d = Landmarks5Detector(output_directory, img_size, str(image_ext), logger)
        d.input(path)
        d.detect()
        logger.log_time("Face detection")
        cprint("Face detection finished.", "green")

    def run(self, logger):
        args = self.parse_args()
        img_size = (args.target_width, args.target_height)
        if args.filename:
            self.main(args.filename, None, img_size, args.img_ext, logger)
        elif args.input_dir:
            self.main(args.input_dir, args.output_dir, img_size, args.img_ext, logger)
        else:
            # temporary
            cprint(
                f"Detector requires an --input-dir flag to specify directory of unconverted images. "
                f"Using hardcoded path: converted_images",
                "red"
            )
            self.main(
                "converted_images",
                args.output_dir,
                img_size,
                args.img_ext,
                logger
            )
