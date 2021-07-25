import os
import shutil
from abc import ABC, abstractmethod
from os import listdir
from os.path import isfile, join

from termcolor import cprint, colored

from medusa.dataset_inspector.inspector import validate
from medusa.definitions import ImageExtension


class DatasetAnalyzer(ABC):
    """Template/ Parent class of pre-dataset analyzer."""
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
        if len(self.images_list) > 1:
            cprint(
                colored("Found ", "yellow")
                + colored(str(len(self.images_list)), "red")
                + colored(" images in ", "yellow")
                + colored(self.input_directory, "red")
            )
        if not len(self.images_list):
            cprint(f"{self.input_directory} is empty.", "red")
            exit()

    def create_output_directory(self):
        if self.output_directory and self.output_directory not in os.listdir():
            os.makedirs(self.output_directory)
        elif self.output_directory in os.listdir():
            if len(os.listdir(self.output_directory)):
                print(colored(f"{self.output_directory}", "red") +
                      colored(" is not empty! Do you want to remove its contents? [Y/n]", "yellow"))
                if validate():
                    shutil.rmtree(self.output_directory)
                    os.makedirs(self.output_directory)

    @input_directory.setter
    def input_directory(self, value):
        self._input_directory = value
