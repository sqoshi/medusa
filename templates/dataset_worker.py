from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join

from termcolor import cprint, colored

from handled_types.image_type import ImageExtension


class DatasetAnalyzer(ABC):

    @property
    def input_directory(self):
        return self._input_directory

    @abstractmethod
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory

    def find_images(self) -> list:
        if isfile(self.input_directory):
            return [self.input_directory]
        return [
            join(self.input_directory, f)
            for f in listdir(self.input_directory)
            if ImageExtension.is_image_ext(join(self.input_directory, f))
        ]

    def input(self, path):
        self.input_directory = path
        self.images_list = self.find_images()
        cprint(
            colored("Found ", "yellow")
            + colored(str(len(self.images_list)), "red")
            + colored(" images in ", "yellow")
            + colored(self.input_directory, "red")
        )
        if not len(self.images_list):
            exit()

    @input_directory.setter
    def input_directory(self, value):
        self._input_directory = value
