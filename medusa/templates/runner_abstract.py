import argparse
import sys
from abc import ABC, abstractmethod

from medusa.handled_types.image_type import ImageExtension


class AbstractRunner(ABC):
    parser = argparse.ArgumentParser()

    @abstractmethod
    def parse_args(self, terminal_arguments=None):
        if terminal_arguments is None:
            terminal_arguments = sys.argv[2:]
        return terminal_arguments

    def insert_default_args(self):
        self.parser.add_argument(
            "filename", type=str, nargs="?", default=None, help="Input single image."
        )
        self.parser.add_argument(
            "--input-dir",
            type=str,
            default=None,  # os.getcwd(),
            help="Input images directory.",
        )
        self.parser.add_argument(
            "--img-ext",
            type=ImageExtension,
            choices=list(ImageExtension),
            default=ImageExtension.png,
            help="Target image extension.",
        )
        self.parser.add_argument(
            "--show-examples",
            type=str,
            default=True,
            help="Display some results examples.",
        )

    @abstractmethod
    def main(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, logger):
        pass
