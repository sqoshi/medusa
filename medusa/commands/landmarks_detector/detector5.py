import os
import warnings

from PIL import Image

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # must be above mtcnn import
from mtcnn import MTCNN
from medusa.abstract_models.abstract_detector import AbstractDetector

from numpy import asarray

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