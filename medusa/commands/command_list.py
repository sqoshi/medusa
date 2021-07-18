from enum import Enum


class Command(Enum):
    convert = "convert"  # Allow to convert images to specified extension. (Example: jpg -> png)
    detect = "detect"  # Allow to detect faces on images. ( ONLY ON JPEG/JPG IMAGES)
    detect_faces = "detect-faces"  # Allow to detect faces on images. ( ONLY ON JPEG/JPG IMAGES)
    detect_landmarks = "detect-landmarks"  # Allow to detect faces on images. ( ONLY ON JPEG/JPG IMAGES)

    def __str__(self):
        return self.value
