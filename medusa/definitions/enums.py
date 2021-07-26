from enum import Enum
from os.path import isfile


class ImageExtension(Enum):
    """Handled image formats."""
    png = "png"
    jpg = "jpg"
    jpeg = "jpeg"
    webp = "webp"

    def __str__(self):
        return self.value

    @staticmethod
    def is_image_ext(f: str) -> bool:
        """Validates if file is image."""
        return isfile(f) and any([str(f).endswith(str(ext)) for ext in list(ImageExtension)])


class LandmarksFormat(Enum):
    """Possible formats in which landmarks may be saved."""
    json = "json"
    csv = "csv"

    def __str__(self):
        return self.value


class DetectionMode(Enum):
    """Determines how many landmarks will be detected."""
    basic = "basic"
    extensive = "extensive"

    def __str__(self):
        return self.value
