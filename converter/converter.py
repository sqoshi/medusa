import os
from os import makedirs

from PIL import Image

from beautifiers.progress_bar import print_progress_bar
from templates.dataset_worker import DatasetAnalyzer


class Converter(DatasetAnalyzer):
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory

    def standardize_images(self, image_ext):
        if self.output_directory and self.output_directory not in os.listdir():
            makedirs(self.output_directory)

        print_progress_bar(
            0, len(self.images_list), prefix="Progress:", suffix="Complete", length=50
        )

        for i, file in enumerate(self.images_list):
            print_progress_bar(
                i + 1,
                len(self.images_list),
                prefix="Progress:",
                suffix="Complete",
                length=50,
            )

            name = file.split("/")[-1].split(".")[0]
            img = Image.open(str(file)).convert("RGB")
            output_filename = (
                f"{self.output_directory}/{name}" if self.output_directory else name
            )
            img.save(f"{output_filename}.{image_ext}", image_ext)
