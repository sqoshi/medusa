import itertools
import warnings
from os import listdir
from os.path import join

from termcolor import cprint, colored

from medusa.definitions import ImageExtension


def validate():
    yes = {'yes', 'y', 'ye', ''}
    no = {'no', 'n'}
    choice = input().lower()
    if choice in yes:
        return True
    if choice in no:
        return False
    cprint("Please respond with 'yes' or 'no'", "orange")


def flatten(mult_dim_list):
    return list(itertools.chain(*mult_dim_list))


def get_name(file):
    return file.split('.')[0]


def get_ext(file):
    return file.split('.')[-1]


class CustomDatasetInspector:
    # input inspector

    @staticmethod
    def find_files(path):
        return [f for f in listdir(path) if ImageExtension.is_image_ext(join(path, f))]

    @staticmethod
    def check_files_extensions(files):
        ext = get_ext(files[0])

        for f in files:
            if not f.endswith(f".{ext}"):
                warnings.warn("Files extensions are not identity.")

    def match_images_recursive(self, files, matches):
        for f1 in [f for f in files if get_name(f) not in flatten(matches)]:
            f1_ne = get_name(f1)
            for f2 in files:
                f2_ne = get_name(f2)
                if f1_ne in f2_ne or f2_ne in f1_ne:
                    matches.append((f1, f2))
                    return self.match_images_recursive(files, matches)

    @classmethod
    def determine_divider(cls, matches):
        f1, f2 = matches.pop()
        f1, f2 = (f1, f2) if len(f1) > f2 else (f2, f1)
        divider = f1.replace(f2, "")
        validate()
        print(colored("Image divider is ", "orange") + colored("{divider}", "green"))
        return divider

    def match_images(self, files):
        matches = []

        self.match_images_recursive(files, matches)
        divider = self.determine_divider(matches)

        if len(files) != len(flatten(matches)):
            warnings.warn(f"Some files did not match:\n{[f for f in files if get_name(f) not in matches]}")

        return matches, divider

    def inspect(self, directory, logger):
        files = self.find_files(directory)
        if len(files) == 0:
            logger.warn('Images not found in %s' % directory)
        if len(files) % 2 == 0:
            logger.warn('Found odd number of images in dataset.')
            warnings.warn('Found odd number of images in dataset.')
        self.check_files_extensions(files)
        matches, divider = self.match_images(files)
        return files, matches, divider
