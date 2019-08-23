from PIL import Image


class Annotation:

    def __init__(self, filename: str = "") -> None:
        self.image_name = filename
        self.labels = []

    def init_size(self) -> None:
        if self.image_name != "":
            img_name = "{}.jpg".format(self.image_name)
            self.size = Image.open(img_name).size
