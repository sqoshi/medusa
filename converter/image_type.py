from enum import Enum


class ImageExtension(Enum):
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    webp = "webp"

    def __str__(self):
        return self.value
