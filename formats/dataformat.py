import xml.etree.ElementTree as ET
import os
import json
from annotation import Annotation
from abc import ABC, abstractmethod
from typing import List


class DataFormat(ABC):

    def __init__(self, extension: str):
        self.extension = extension

    def parse_xml(self, filename: str) -> Annotation:
        name = os.path.splitext(filename)[0]
        annotation = Annotation(name)
        annotation.init_size()
        with open(filename, 'r') as xml_file:
            tree = ET.parse(xml_file)
            root = tree.getroot()
            labels = list()
            for obj in root.iter('object'):
                difficult = obj.find('difficult').text
                cls = obj.find('name').text
                if cls in self.classes.keys() and int(difficult) == 0:
                    cls_id = str(annotation.classes.get(cls))
                    xml_box = obj.find('bndbox')
                    bbox = (float(xml_box.find('xmin').text),
                            float(xml_box.find('xmax').text),
                            float(xml_box.find('ymin').text),
                            float(xml_box.find('ymax').text))
                    label = (cls_id, bbox)
                    print(label)
                    labels.append(label)
            annotation.labels = labels
            return annotation

    def parse_json(self, filename: str, classes: list) -> List[Annotation]:
        with open(filename, 'r') as json_file:
            json_data = json.load(json_file)
            images = json_data["images"]
            categories = json_data["categories"]
            annotations = []
            for anno in json_data["annotations"]:
                image_id = anno["image_id"]
                cls_id = anno["category_id"]

                for info in images:
                    if info["id"] == image_id:
                        annotation = Annotation(
                            info["file_name"].split(".")[0])
                        annotation.image_size()
                for category in categories:
                    if category["id"] == cls_id:
                        annotation.class_id = category["name"]
                bndbox = {
                    "xmin": anno["bbox"][0],
                    "ymin": anno["bbox"][1],
                    "xmax": anno["bbox"][2] + anno["bbox"][0],
                    "ymax": anno["bbox"][3] + anno["bbox"][1]
                }
                annotation.bbox = (bndbox["xmin"],
                                   bndbox["ymin"],
                                   bndbox["xmax"],
                                   bndbox["ymax"])
                annotations.append(annotation)
            return annotations

    def parse_txt(self, filename: str) -> Annotation:
        name = os.path.splitext(filename)[0]
        annotation = Annotation(name)
        annotation.init_size()
        labels = []
        with open(filename, "r") as txt_file:
            lines = txt_file.readlines()
            for line in lines:
                line = line.strip()
                words = line.split()
                class_id = words[0]
                w, h = annotation.size
                bbox_width = float(words[3]) * w
                bbox_height = float(words[4]) * h
                center_x = float(words[1]) * w
                center_y = float(words[2]) * h
                bbox = []
                bbox.append(center_x - (bbox_width / 2))
                bbox.append(center_y - (bbox_height / 2))
                bbox.append(center_x + (bbox_width / 2))
                bbox.append(center_y + (bbox_height / 2))
                labels.append((class_id, bbox))
            annotation.labels = labels
        return annotation

    @abstractmethod
    def save(self, annotation: Annotation):
        pass
