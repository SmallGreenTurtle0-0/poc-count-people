from ultralytics import YOLO
from PIL import Image
from typing import Union


class DetectPeople:
    @staticmethod
    def load(model_path) -> "DetectPeople":
        return DetectPeople(model_path).load_model()

    def __init__(self, model_path="yolov10n"):
        self.__model_path = model_path

    def load_model(self):
        self.__model = YOLO(self.__model_path)
        print("Model loaded")
        return self

    # image: PIL.Image
    def detect(self, image: Union[Image.Image, str], classes=[0]) -> list:
        result = self.__model.predict(image, classes=classes)
        return result
