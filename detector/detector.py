import os

from PIL import Image
from mtcnn.mtcnn import MTCNN
from numpy import asarray

from beautifiers.progress_bar import print_progress_bar
from templates.dataset_worker import DatasetAnalyzer

os.environ["CUDA_VISIBLE_DEVICES"] = "0"


class FaceDetector(DatasetAnalyzer):
    def __init__(self, output_directory, logger):
        self.logger = logger
        self.input_directory = None
        self.images_list = None
        self.output_directory = output_directory

    @classmethod
    def extract_face(cls, filename, required_size=(160, 160)):
        # load image from file
        image = Image.open(filename)
        # convert to RGB, if needed
        image = image.convert('RGB')
        # convert to array
        pixels = asarray(image)
        # create the detector, using default weights
        detector = MTCNN()
        # detect faces in the image
        results = detector.detect_faces(pixels)
        # extract the bounding box from the first face
        x1, y1, width, height = results[0]['box']
        # bug fix
        x1, y1 = abs(x1), abs(y1)
        x2, y2 = x1 + width, y1 + height
        # extract the face
        face = pixels[y1:y2, x1:x2]
        # resize pixels to the model size
        image = Image.fromarray(face)
        image = image.resize(required_size)
        face_array = asarray(image)
        return face_array, image

    def detect_faces(self):
        if self.output_directory and self.output_directory not in os.listdir():
            os.makedirs(self.output_directory)

        # enumerate files
        print_progress_bar(
            0, len(self.images_list), prefix="Progress:", suffix="Complete", length=50
        )

        for i, file in enumerate(self.images_list):
            print_progress_bar(
                i + 1,
                len(self.images_list),
                prefix="Progress:",
                suffix="Complete",
                length=50,
            )

            face, img = self.extract_face(file)
            image_ext = 'jpeg'
            name = file.split("/")[-1].split(".")[0]
            output_filename = (
                f"{self.output_directory}/{name}" if self.output_directory else name
            )
            img.save(f"{output_filename}.{image_ext}", image_ext)
