import json
import os
import warnings
from collections import namedtuple

from PIL import Image

from medusa.abstract_models.abstract_detector import Detector

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'  # must be above mtcnn import
from mtcnn.mtcnn import MTCNN
from numpy import asarray

from medusa.beautifiers.progress_bar import print_progress_bar
from medusa.exceptions import LandmarksNotFoundException
from medusa.abstract_models.abstract_analyzer import DatasetAnalyzer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"

Point = namedtuple("Point", "x y")


class Landmarks5Detector(DatasetAnalyzer, Detector):
    def __init__(self, output_filename, output_format, logger=None):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.detector = MTCNN()
        self.landmarks = {}
        self.output_filename = output_filename  # "landmarks_5.json"
        # self.output_format =

    @staticmethod
    def get_landmarks(image_detection_info):
        landmarks_dictionary = image_detection_info['keypoints']
        x, y, _, _ = image_detection_info['box']
        print(landmarks_dictionary)
        return landmarks_dictionary

    def save_landmarks(self, file: str, results):
        if results:
            if len(results) > 1:
                self.landmarks[str(file)] = [x['keypoints'] for x in results]
            elif len(results) == 1:
                self.landmarks[str(file)] = self.get_landmarks(results[0])
            else:
                warnings.warn(f"Landmarks not found in {file}")

    def extract_landmarks(self, filename: str):
        pixels = asarray(Image.open(filename).convert("RGB"))
        results = self.detector.detect_faces(pixels)
        if not results:
            raise LandmarksNotFoundException(filename)
        self.save_landmarks(filename, results)

    def save_landmarks_coordinates(self):
        with open(self.output_filename, "w+") as fw:
            json.dump(self.landmarks, fw)

    def detect(self):
        self.create_output_directory()
        failed_files = set()
        for i, file in enumerate(self.images_list):
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)
            try:
                self.extract_landmarks(file)
            except LandmarksNotFoundException:
                failed_files.add(file)
        self.analyze_failed_files(failed_files)

        self.save_landmarks_coordinates()
