import csv
import json
from abc import ABC, abstractmethod

from termcolor import cprint, colored

from medusa.beautifiers.progress_bar import print_progress_bar
from medusa.definitions import LandmarksFormat
from medusa.exceptions import LandmarksNotFoundException


class AbstractDetector(ABC):
    output_filename = None
    output_format = None
    detector = None
    images_list = None
    landmarks = {}

    def save_landmarks_coordinates(self):
        if self.output_format == LandmarksFormat.json:
            with open(f"{self.output_filename}.{self.output_format}", "w+") as fw:
                json.dump(self.landmarks, fw)
        elif self.output_format == LandmarksFormat.csv:
            with open(f"{self.output_filename}.{self.output_format}", "w") as f:
                for i, (k, v) in enumerate(self.landmarks.items()):
                    if i == 0:
                        w = csv.DictWriter(f, ["filename"] + list(v.keys()))
                        w.writeheader()
                    new_dict = {k: v for (k, v) in v.items()}
                    new_dict["filename"] = k
                    w.writerow(new_dict)  # fixme

    @staticmethod
    def display_failed_files(files):
        if files:
            print(colored("Could not detected face on ", "yellow") +
                  colored(str(len(files)), "red") +
                  colored(" images:", "yellow"))
            for f in files:
                cprint(f"\t- {f}", "red")
        else:
            cprint(f"Successfully detected face on every image.", "green")

    @abstractmethod
    def extract_landmarks(self, *args, **kwargs):
        pass

    @abstractmethod
    def update_landmarks(self, *args, **kwargs):
        pass

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
