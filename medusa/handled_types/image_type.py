from enum import Enum
from os.path import isfile


class ImageExtension(Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    webp = "webp"

    def __str__(self):
        return self.value

    @staticmethod
    def is_image_ext(f):
        return isfile(f) and any([str(f).endswith(str(ext)) for ext in list(ImageExtension)])
