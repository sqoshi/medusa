import sys
from PIL import Image
from os import listdir
from os.path import isfile, join


class Converter:
    def __init__(self):
        self.images_extensions = ['jpg', 'webp', 'png', 'jpeg']
        self.images_directory_path = None

    def find_images(self) -> list:
        return [f for f in listdir(self.images_directory_path) if
                isfile(join(self.images_directory_path, f)) and any(
                    [str(f).endswith(ext) for ext in self.images_extensions])]

    def input(self, path):
        self.images_directory_path = path

    def standardize_images(self, images_type):
        images_list = self.find_images()


def run(path, goal_dir='converted_images', images_type='png'):
    print(sys.argv)
    c = Converter()
    c.input(path)
    c.standardize_images(images_type)
