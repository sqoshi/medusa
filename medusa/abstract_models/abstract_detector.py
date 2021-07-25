import csv
import json
from abc import ABC, abstractmethod

from termcolor import cprint, colored

from medusa.definitions import LandmarksFormat


class AbstractDetector(ABC):
    output_filename = None
    output_format = None
    detector = None
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
    def detect(self):
        pass

    @abstractmethod
    def extract_landmarks(self, *args, **kwargs):
        pass
