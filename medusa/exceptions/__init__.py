class FaceNotFoundException(Exception):
    def __init__(self, filename=""):
        self.message = f"Face not found in {filename}."
        super().__init__(self.message)
