import sys

from termcolor import cprint, colored

from src.commands.converter.converter import Converter
from src.handled_types.image_type import ImageExtension
from src.templates.runner_abstract import AbstractRunner


class CommandRunner(AbstractRunner):
    def parse_args(self, terminal_arguments=None):
        if terminal_arguments is None:
            terminal_arguments = sys.argv[2:]

        self.insert_default_args()

        self.parser.add_argument(
            "--output-dir",
            type=str,
            default="converted_images",
            help="Name of directory in which converted images will be saved.",
        )
        self.parser.add_argument(
            "--img-ext",
            type=ImageExtension,
            choices=list(ImageExtension),
            default=ImageExtension.png,
            help="Specify target image extension.",
        )
        return self.parser.parse_args(terminal_arguments)

    def main(self, path, output_directory, image_ext, logger):
        c = Converter(output_directory, logger)
        c.input(path)
        c.standardize_images(image_ext)
        logger.log_time("Conversion")
        print(colored(f"Conversion finished. Files saved in ", "green") +
              colored(f"{output_directory}", "yellow"))

    def run(self, logger):
        args = self.parse_args()
        if args.filename:
            self.main(args.filename, None, str(args.img_ext), logger)
        elif args.input_dir:
            self.main(args.input_dir, args.output_dir, str(args.img_ext), logger)
        else:
            # temporary
            cprint(
                f"Converter requires an --input-dir flag to specify directory of unconverted images. "
                f"Using hardcoded path: /home/piotr/Documents/bsc-thesis/mc-dataset",
                "red"
            )
            self.main(
                "/home/piotr/Documents/bsc-thesis/mc-dataset",
                args.output_dir,
                str(args.img_ext),
                logger
            )
#
#
# def parse_args():
#     parser = argparse.ArgumentParser()
#     parser.add_argument(
#         "filename", type=str, nargs="?", default=None, help="Single file to convert"
#     )
#     parser.add_argument(
#         "--input-dir",
#         type=str,
#         default=None,  # os.getcwd(),
#         help="Path to directory of images.",
#     )
#     parser.add_argument(
#         "--output-dir",
#         type=str,
#         default="converted_images",
#         help="Name of directory in which converted images will be saved.",
#     )
#     parser.add_argument(
#         "--img-ext",
#         type=ImageExtension,
#         choices=list(ImageExtension),
#         default=ImageExtension.png,
#         help="Specify target image extension.",
#     )
#     return parser.parse_args(sys.argv[2:])
#
#
# def main(path, output_directory, image_ext, logger):
#     c = Converter(output_directory, logger)
#     c.input(path)
#     c.standardize_images(image_ext)
#     logger.log_time("Conversion")
#     print(colored(f"Conversion finished. Files saved in ", "green") +
#           colored(f"{output_directory}", "yellow"))
#
#
# def run(logger):
#     args = parse_args()
#     if args.filename:
#         main(args.filename, None, str(args.img_ext), logger)
#     elif args.input_dir:
#         main(args.input_dir, args.output_dir, str(args.img_ext), logger)
#     else:
#         # temporary
#         cprint(
#             f"Converter requires an --input-dir flag to specify directory of unconverted images. "
#             f"Using hardcoded path: /home/piotr/Documents/bsc-thesis/mc-dataset",
#             "red"
#         )
#         main(
#             "/home/piotr/Documents/bsc-thesis/mc-dataset",
#             args.output_dir,
#             str(args.img_ext),
#             logger
#         )
