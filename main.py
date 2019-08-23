import argparse
import os
from formats import yolo, voc


extensions = [".txt", ".json", ".xml"]


def run():
    parser = argparse.ArgumentParser(description="Converter formats")
    parser.add_argument("-in_path",
                        help="Relative location of input files directory",
                        required=True)
    parser.add_argument("-format",
                        help="Kind of format for converting",
                        default="yolo")
    args = parser.parse_args()
    if args.format == "yolo":
        dataformat = yolo.YOLO("txt")
    if args.format == "voc":
        dataformat = voc.VOC("xml")
    for file in os.listdir(args.in_path):
        name, extension = os.path.splitext(file)
        if extension in extensions:
            filename = os.path.join(args.in_path, name + extension)
            print(filename)
            # if extension == ".txt":
            #     annotation = dataformat.parse_txt(filename)
            if extension == ".xml":
                annotation = dataformat.parse_xml(filename)
            print(annotation.labels)
            print(annotation.size)
            dataformat.save(annotation)
    print(dataformat.classes)


if __name__ == "__main__":
    run()
