from enum import Enum


class Command(Enum):
    """Commands available in package."""
    convert = "convert"  # Allow to convert images to specified extension. (Example: jpg -> png)
    crop_faces = "crop-face"  # Crop faces from images.
    detect = "detect"  # Detects face landmarks ( 68 or 5)

    def __str__(self):
        return self.value
