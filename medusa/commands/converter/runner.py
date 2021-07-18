from termcolor import cprint, colored

from medusa.commands.converter.converter import Converter
from medusa.templates.runner_abstract import AbstractRunner


class CommandRunner(AbstractRunner):
    def parse_args(self, terminal_arguments=None):
        terminal_arguments = super().parse_args(terminal_arguments)
        self.insert_default_args()

        self.parser.add_argument(
            "--output-dir",
            type=str,
            default="converted_images",
            help="Output directory.",
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
