import argparse
from abc import ABC, abstractmethod


class AbstractRunner(ABC):
    parser = argparse.ArgumentParser()

    def insert_default_args(self):
        self.parser.add_argument(
            "filename", type=str, nargs="?", default=None, help="Single file to detect face."
        )
        self.parser.add_argument(
            "--input-dir",
            type=str,
            default=None,  # os.getcwd(),
            help="Path to directory of images.",
        )

    @abstractmethod
    def parse_args(self):
        pass

    @abstractmethod
    def main(self, *args, **kwargs):
        pass

    @abstractmethod
    def run(self, logger):
        pass
