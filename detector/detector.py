import os
from collections import namedtuple

from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray

from beautifiers.progress_bar import print_progress_bar
from templates.dataset_worker import DatasetAnalyzer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

Point = namedtuple("Point", "x y")


class FaceDetector(DatasetAnalyzer):
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory
        self.detector = MTCNN()  # not sure if detector maybe re-used

    @staticmethod
    def _fix_cords(results):
        x1, y1, width, height = results[0]['box']
        x2, y2 = abs(x1) + width, abs(y1) + height
        return Point(x1, y1), Point(x2, y2)

    def extract_face(self, filename, required_size=(160, 160)):
        image = Image.open(filename).convert("RGB")
        pixels = asarray(image)
        results = self.detector.detect_faces(pixels)
        p1, p2 = self._fix_cords(results)
        face = pixels[p1.y:p2.y, p1.x:p2.x]
        image = Image.fromarray(face).resize(required_size)
        return image  # , asarray(image)

    def detect_faces(self):
        self.create_output_directory()

        for i, file in enumerate(self.images_list):
            print(file)
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)

            img = self.extract_face(file)
            image_ext = 'jpeg'

            name = file.split("/")[-1].split(".")[0]
            output_filename = f"{self.output_directory}/{name}" if self.output_directory else name
            img.save(f"{output_filename}.{image_ext}", image_ext)
