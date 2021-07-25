import os
import warnings

from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # must be above mtcnn import
from mtcnn import MTCNN
from medusa.abstract_models.abstract_detector import AbstractDetector

from numpy import asarray

from medusa.beautifiers.progress_bar import print_progress_bar
from medusa.exceptions import LandmarksNotFoundException
from medusa.abstract_models.abstract_analyzer import DatasetAnalyzer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class Landmarks5Detector(DatasetAnalyzer, AbstractDetector):

    def __init__(self, output_filename, output_format, logger=None):
        self.logger = logger
        self.output_filename = output_filename  # "landmarks_5.json"
        self.output_format = output_format
        self.detector = MTCNN()

    def update_landmarks(self, file: str, results):
        if results:
            if len(results) > 1:
                self.landmarks[str(file)] = [x['keypoints'] for x in results]
            elif len(results) == 1:
                self.landmarks[str(file)] = results[0]['keypoints']
            else:
                warnings.warn(f"Landmarks not found in {file}")

    def extract_landmarks(self, filename: str):
        pixels = asarray(Image.open(filename).convert("RGB"))
        results = self.detector.detect_faces(pixels)
        if not results:
            raise LandmarksNotFoundException(filename)
        self.update_landmarks(filename, results)

    def detect(self):
        failed_files = set()
        for i, file in enumerate(self.images_list):
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)
            try:
                self.extract_landmarks(file)
            except LandmarksNotFoundException:
                failed_files.add(file)
        self.display_failed_files(failed_files)

        self.save_landmarks_coordinates()
