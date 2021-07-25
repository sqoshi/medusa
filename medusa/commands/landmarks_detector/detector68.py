import os
from bz2 import BZ2File
from http.client import HTTPException
from typing import Optional
from urllib.error import URLError, HTTPError
from urllib.request import urlretrieve

import numpy as np
from _dlib_pybind11 import shape_predictor
from cv2 import imread, rectangle, putText, FONT_HERSHEY_SIMPLEX, circle, cvtColor, COLOR_BGR2GRAY
from dlib import get_frontal_face_detector
from termcolor import cprint, colored

from medusa.abstract_models.abstract_analyzer import DatasetAnalyzer
from medusa.abstract_models.abstract_detector import AbstractDetector
from medusa.beautifiers.progress_bar import print_progress_bar
from medusa.exceptions import LandmarksNotFoundException

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


def rect_to_bb(rect):
    x = rect.left()
    y = rect.top()
    w = rect.right() - x
    h = rect.bottom() - y
    return x, y, w, h


def shape_to_np(shape, dtype="int"):
    coords = np.zeros((68, 2), dtype=dtype)
    for i in range(0, 68):
        coords[i] = (shape.part(i).x, shape.part(i).y)
    return coords


class Landmarks68Detector(DatasetAnalyzer, AbstractDetector):
    def __init__(self, output_directory, predictor_filepath: Optional[str], logger):
        self.logger = logger
        self.detector = get_frontal_face_detector()

        if predictor_filepath:
            self.predictor = shape_predictor(predictor_filepath)
        else:
            self.download_predictor()

    def download_predictor(self, shape_predictor_filepath="shape_predictor_68_face_landmarks.bz2"):
        cprint("Shape predictor not found.", "yellow")
        response = input(
            colored(f"Would you like to download ", "green") + colored('64 [MB]', 'red') + colored(" model ?\n",
                                                                                                   "green")
        )
        # todo search for model in curr dir
        if str(response).lower() in {"", "y", "yes"}:
            try:
                urlretrieve("http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2", shape_predictor_filepath)
                model_name = shape_predictor_filepath.replace(".bz2", ".dat")
                with open(model_name, 'wb') as fw:
                    fw.write(BZ2File(shape_predictor_filepath).read())
                self.predictor = shape_predictor(model_name)  # open the file
                # todo: download animation
            except URLError or HTTPError or HTTPException:
                cprint("Error occurred during model download.", "red")
                cprint("Please download model manually and input filepath via arguments. Process halt.", "red")
                exit()
            except Exception:
                cprint("Error occurred during model decompression.", "red")
                cprint("Please download model manually and input filepath via arguments. Process halt.", "red")
                exit()

        else:
            # todo search in /home for predictor
            cprint("Shape predictor not found. Detection interrupted.", "red")
            exit()

    def detect(self):
        failed_files = set()
        for i, file in enumerate(self.images_list):
            print_progress_bar(i, len(self.images_list) - 1, prefix="Progress:", suffix="Complete", length=50)
            try:
                self.extract_landmarks(file)
            except LandmarksNotFoundException:
                failed_files.add(file)
        self.display_failed_files(failed_files)

    def extract_landmarks(self, filename: str):
        image = imread(filename)
        rects = self.detector(image, 1)
        print(f"{filename}")
        print(len(rects))
        print(rects)
        # if not rects:
        #     raise LandmarksNotFoundException
        self.detect_landmarks(rects, image)

    def detect_landmarks(self, rects, image):
        # gray = image
        gray = cvtColor(image, COLOR_BGR2GRAY)
        for (i, rect) in enumerate(rects):
            shape = self.predictor(gray, rect)
            shape = shape_to_np(shape)
            x, y, w, h = rect_to_bb(rect)
            rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            for (x, y) in shape:
                circle(image, (x, y), 1, (0, 0, 255), -1)
        # imshow("Output", image)
        # waitKey(0)
