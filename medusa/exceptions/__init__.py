class FaceNotFoundException(Exception):
    def __init__(self, filename=""):
        self.message = f"Face not found in {filename}."
        super().__init__(self.message)


class LandmarksNotFoundException(Exception):
    def __init__(self, filename=""):
        self.message = f"Landmarks not detected in {filename}."
        super().__init__(self.message)


class DetectionModeNotFoundException(Exception):
    def __init__(self, dmode=""):
        self.message = f"Detection mode {dmode} is not handled. Program supports only 5 or 68 landmark points."
        super().__init__(self.message)
