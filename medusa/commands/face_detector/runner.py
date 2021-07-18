from termcolor import cprint

from medusa.commands.face_detector.detector import FaceDetector
from medusa.templates.runner_abstract import AbstractRunner


class CommandRunner(AbstractRunner):
    def parse_args(self, terminal_arguments=None):
        terminal_arguments = super().parse_args(terminal_arguments)

        self.insert_default_args()
        self.parser.add_argument(
            "--output-dir",
            type=str,
            default="detected_faces",
            help="Output directory.",
        )

        return self.parser.parse_args(terminal_arguments)

    def main(self, path, output_directory, image_ext, logger):
        d = FaceDetector(output_directory, logger)
        d.input(path)
        d.detect()
        logger.log_time("Face detection")
        cprint("Face detection finished.", "green")

    def run(self, logger):
        args = self.parse_args()

        if args.filename:
            self.main(args.filename, None, str(args.img_ext), logger)
        elif args.input_dir:
            self.main(args.input_dir, args.output_dir, str(args.img_ext), logger)
        else:
            # temporary
            cprint(
                f"Detector requires an --input-dir flag to specify directory of unconverted images. "
                f"Using hardcoded path: /converted_images",
                "red"
            )
            self.main(
                "/home/piotr/Documents/bsc-thesis/mc-dataset",
                args.output_dir,
                str(args.img_ext),
                logger
            )
