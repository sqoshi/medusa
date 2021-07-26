from PIL import Image

from medusa.abstract_models.abstract_analyzer import DatasetAnalyzer
from medusa.beautifiers.progress_bar import print_progress_bar


class Converter(DatasetAnalyzer):
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory

    def standardize_images(self, image_ext):
        self.create_output_directory()

        for i, file in enumerate(self.images_list):
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)

            name = file.split("/")[-1].split(".")[0]
            img = Image.open(str(file)).convert("RGB")
            output_filename = f"{self.output_directory}/{name}" if self.output_directory else name
            img.save(f"{output_filename}.{image_ext}", image_ext)
