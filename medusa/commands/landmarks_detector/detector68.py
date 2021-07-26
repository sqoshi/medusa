import os
from bz2 import BZ2File
from http.client import HTTPException
from typing import Optional
from urllib.error import URLError, HTTPError
from urllib.request import urlretrieve

import dlib
import numpy as np
from _dlib_pybind11 import shape_predictor
from cv2 import imread, COLOR_BGR2GRAY, cvtColor
from dlib import get_frontal_face_detector
from termcolor import cprint, colored

from medusa.abstract_models.abstract_analyzer import DatasetAnalyzer
from medusa.abstract_models.abstract_detector import AbstractDetector

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


def shape_to_dict(shape):
    result = {}
    for i in range(0, 68):
        result[i] = (shape.part(i).x, shape.part(i).y)
    return result


class Landmarks68Detector(DatasetAnalyzer, AbstractDetector):
    def __init__(self, output_filename, output_format, predictor_filepath: Optional[str], logger):
        self.logger = logger
        self.detector = get_frontal_face_detector()
        self.output_filename = output_filename  # "landmarks_5.json"
        self.output_format = output_format
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

    def update_landmarks(self, filename, landmarks_dictionary):
        self.landmarks[filename] = landmarks_dictionary

    def extract_landmarks(self, filename: str):
        image = imread(filename)
        height, width, _ = image.shape
        rect = dlib.rectangle(left=0, top=0, right=height, bottom=height)  # assume photo is a single front face
        gray = cvtColor(image, COLOR_BGR2GRAY)
        shape = self.predictor(gray, rect)
        self.update_landmarks(filename, shape_to_dict(shape))
        # shape = shape_to_np(shape)
        # x, y, w, h = rect_to_bb(rect)
        # rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        # putText(image, "Face", (x - 10, y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        # for (x, y) in shape:
        #     circle(image, (x, y), 1, (0, 0, 255), -1)
        # imshow("Output", image)
        # waitKey(0)

# fixme: for multiple images

#         print(shape)
#         shape = shape_to_np(shape)
#         x, y, w, h = rect_to_bb(rect)
#         rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         for (x, y) in shape:
#             circle(image, (x, y), 1, (0, 0, 255), -1)
# rects = self.detector(image, 1)
# if len(rects) > 1:
#     cprint(f"Multiple face boxes found on {filename} ", "red")
# elif not rects:
#     height, width, _ = image.shape
#     rects = [dlib.rectangle(left=0, top=0, right=height, bottom=height)]
# self.detect_landmarks(rects, image)

# def detect_landmarks(self, rects, image):
#     # gray = image
#     gray = cvtColor(image, COLOR_BGR2GRAY)
#     for i, rect in enumerate(rects):
#         shape = self.predictor(gray, rect)
#         print(shape)
#         shape = shape_to_np(shape)
#         x, y, w, h = rect_to_bb(rect)
#         rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
#         putText(image, "Face #{}".format(i + 1), (x - 10, y - 10), FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
#         for (x, y) in shape:
#             circle(image, (x, y), 1, (0, 0, 255), -1)
#     imshow("Output", image)
#     waitKey(0)
#
