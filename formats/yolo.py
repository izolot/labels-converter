from formats import dataformat
from annotation import Annotation


class YOLO(dataformat.DataFormat):

    classes = {"passager": 3, "rotate": 3, "back": 3, "face": 3}

    def convert_to_yolo(self, size: list, box: list) -> list:
        dw = 1./(size[0])
        dh = 1./(size[1])
        x = (box[0] + box[1])/2.0 - 1
        y = (box[2] + box[3])/2.0 - 1
        w = box[1] - box[0]
        h = box[3] - box[2]
        x = x*dw
        w = w*dw
        y = y*dh
        h = h*dh
        return (x, y, w, h)

    def save(self, annotation: Annotation) -> None:
        filename = "{}.{}".format(annotation.image_name, self.extension)
        with open(filename, "w+") as f:
            w, h = annotation.size
            for label in annotation.labels:
                bbox = label[1:5]
                params = self.convert_to_yolo((w, h), *bbox)
                f.write(label[0] + " " +
                        " ".join([str(p) for p in params]) + '\n')
