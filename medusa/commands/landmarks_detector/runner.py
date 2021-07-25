from typing import Tuple

from termcolor import cprint

from medusa.abstract_models.abstract_runner import AbstractRunner
from medusa.commands.landmarks_detector.detector5 import Landmarks5Detector
from medusa.commands.landmarks_detector.detector68 import Landmarks68Detector
from medusa.definitions import LandmarksFormat, DetectionMode
from medusa.exceptions import DetectionModeNotFoundException


def has_correct_extension(filename: str) -> bool:
    if filename:
        f_as_array = filename.split(".")
        if len(f_as_array) > 1 and f_as_array[-1] in list(LandmarksFormat):
            return True
    return False


def define_output_file(args) -> Tuple:
    if has_correct_extension(args.output_filename):
        return args.output_filename.split(".")
    return args.output_filename, args.output_format


class CommandRunner(AbstractRunner):
    def parse_args(self, terminal_arguments=None):
        terminal_arguments = super().parse_args(terminal_arguments)
        self.insert_input_file_arg()
        self.insert_input_dir_arg()
        self.parser.add_argument(
            "--output-filename",
            type=str,
            default="landmarks",
            help="Output filename with landmarks coordinates.",
        )
        self.parser.add_argument(
            "--output-format",
            type=LandmarksFormat,
            choices=list(LandmarksFormat),
            default=LandmarksFormat.csv,
            help="Output file format/extension.",
        )
        self.parser.add_argument(
            "--detection-mode",
            type=DetectionMode,
            choices=list(DetectionMode),
            default=DetectionMode.basic,
            help="Gives the choice to find 5 or 68 landmarks."
        )
        self.parser.add_argument(
            "--shape-predictor",
            default=None,
            help="Shape (68) prediction model filepath.",
        )

        return self.parser.parse_args(terminal_arguments)

    def main(self, path, predictor_filepath, detection_mode, output_filename, output_format, logger):
        if detection_mode == DetectionMode.basic:
            d = Landmarks5Detector(output_filename, output_format, logger)
            d.input(path)
            d.detect()
            logger.log_time("5-Landmarks detection")
        elif detection_mode == DetectionMode.extensive:
            # todo: 68 landmark detection using `dlib`
            d = Landmarks68Detector("", predictor_filepath, logger)
            d.input(path)
            d.detect()
            logger.log_time("68-Landmarks detection")
        else:
            raise DetectionModeNotFoundException(detection_mode)
        cprint("Landmarks detection finished.", "green")

    def run(self, logger):
        args = self.parse_args()
        output_filename, output_format = define_output_file(args)

        if args.filename:
            self.main(args.filename, args.shape_predictor, args.detection_mode, output_filename, output_format,
                      logger)
        elif args.input_dir:
            self.main(args.input_dir, args.shape_predictor, args.detection_mode, output_filename, output_format,
                      logger)
        else:
            # temporary
            cprint(
                f"Landmark Detector requires an --input-dir flag to specify directory of images. "
                f"Using hardcoded path: detected_images",
                "red"
            )
            self.main(
                "converted_images",
                args.shape_predictor,
                args.detection_mode,
                output_filename,
                output_format,
                logger
            )
