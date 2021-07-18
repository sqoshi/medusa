import os
from collections import namedtuple

from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # must be above mtcnn import
from mtcnn.mtcnn import MTCNN
from numpy import asarray
from termcolor import cprint

from medusa.beautifiers.progress_bar import print_progress_bar
from medusa.exceptions import FaceNotFoundException
from medusa.templates.dataset_worker import DatasetAnalyzer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

Point = namedtuple("Point", "x y")


class FaceDetector(DatasetAnalyzer):
    def __init__(self, output_directory, logger, image_ext='jpeg'):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.target_size = (160, 160)
        self.output_directory = output_directory
        self.detector = MTCNN()  # not sure if face_detector maybe re-used
        self.target_ext = image_ext

    @staticmethod
    def _fix_cords(results):
        x1, y1, width, height = results[0]['box']
        x2, y2 = abs(x1) + width, abs(y1) + height
        return Point(x1, y1), Point(x2, y2)

    def extract_face(self, filename):
        pixels = asarray(Image.open(filename).convert("RGB"))
        results = self.detector.detect_faces(pixels)
        if not results:
            raise FaceNotFoundException(filename)
        p1, p2 = self._fix_cords(results)
        face = pixels[p1.y:p2.y, p1.x:p2.x]
        return Image.fromarray(face).resize(self.target_size)  # , asarray(image)

    @staticmethod
    def analyze_failed_files(files):
        if files:
            cprint(f"Face could not be detected on:", "yellow")
            for f in files:
                cprint(f"\t- {f}", "red")
        else:
            cprint(f"Successfully detected face on every image.", "green")

    def detect(self):
        self.create_output_directory()
        failed_files = set()
        for i, file in enumerate(self.images_list):
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)
            try:
                img = self.extract_face(file)
                name = file.split("/")[-1].split(".")[0]
                output_filename = f"{self.output_directory}/{name}" if self.output_directory else name
                img.save(f"{output_filename}.{self.target_ext}", self.target_ext)
            except FaceNotFoundException:
                failed_files.add(file)
        self.analyze_failed_files(failed_files)
