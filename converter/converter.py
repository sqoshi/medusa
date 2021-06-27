import shutil
import sys
from os import listdir
from os import makedirs
from os.path import isfile, join

import termcolor
from PIL import Image


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100,
                     fill=termcolor.colored('█', "green"), print_end="\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filled_len = int(length * iteration // total)
    bar = str(fill * filled_len) + '-' * (length - filled_len)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=print_end)
    # Print New Line on Complete
    if iteration == total:
        print()


class Converter:
    def __init__(self, storage):
        self.images_extensions = ["jpg", "webp", "png", "jpeg"]
        self.images_root_directory = None
        self.images_list = None
        self.storage = storage

    def find_images(self) -> list:
        return [
            f
            for f in listdir(self.images_root_directory)
            if isfile(join(self.images_root_directory, f))
               and any([str(f).endswith(ext) for ext in self.images_extensions])
        ]

    def input(self, path):
        self.images_root_directory = path
        self.images_list = self.find_images()
        termcolor.cprint(
            termcolor.colored("Found ", 'yellow') +
            termcolor.colored(len(self.images_list), 'red') +
            termcolor.colored(" images in ", 'yellow') +
            termcolor.colored(self.images_root_directory, 'red')
        )

    def standardize_images(self, image_ext):
        try:
            shutil.rmtree(self.storage)
        except FileNotFoundError:
            pass
        makedirs(self.storage)

        printProgressBar(0, len(self.images_list), prefix='Progress:', suffix='Complete', length=50)
        for i, file in enumerate(self.images_list):
            printProgressBar(i + 1, len(self.images_list), prefix='Progress:', suffix='Complete', length=50)
            name = file.split(".")[0]
            img = Image.open(f"{self.images_root_directory}/{file}").convert("RGB")
            img.save(f"{self.storage}/{name}.{image_ext}", image_ext)


def run(path, storage="converted_images", image_ext="png"):
    print(sys.argv)
    c = Converter(storage)
    c.input(path)
    c.standardize_images(image_ext)
