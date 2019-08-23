import xml.etree.ElementTree as ET
import os
from formats import dataformat
from annotation import Annotation


class VOC(dataformat.DataFormat):

    classes = {3: "person",  2: "head"}

    def create_xml_tree(self, annotation: Annotation) -> ET.Element:
        img_name = "{}.jpg".format(annotation.image_name)
        root = ET.Element("annotations")
        ET.SubElement(root, "folder").text = os.path.dirname(img_name)
        ET.SubElement(root, "filename").text = img_name
        size = ET.SubElement(root, "size")
        ET.SubElement(size, "width").text = str(annotation.size[0])
        ET.SubElement(size, "height").text = str(annotation.size[1])
        ET.SubElement(size, "depth").text = "3"
        for label in annotation.labels:
            print(type(label))
            obj = ET.SubElement(root, "object")
            ET.SubElement(obj, "name").text = self.classes.get(int(label[0]))
            ET.SubElement(obj, "pose").text = "Unspecified"
            ET.SubElement(obj, "truncated").text = str(0)
            ET.SubElement(obj, "difficult").text = str(0)
            bbox = ET.SubElement(obj, "bndbox")
            ET.SubElement(bbox, "xmin").text = str(label[1][0])
            ET.SubElement(bbox, "ymin").text = str(label[1][1])
            ET.SubElement(bbox, "xmax").text = str(label[1][2])
            ET.SubElement(bbox, "ymax").text = str(label[1][3])
        return root

    def save(self, annotation: Annotation):
        filename = "{}.{}".format(annotation.image_name, self.extension)
        root = self.create_xml_tree(annotation)
        tree = ET.ElementTree(root)
        tree.write(filename)
