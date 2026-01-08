from ..graphics.palette import Palette

class PaletteFile(Palette):
    def __init__(self, path):
        self.path = path
        super().__init__()

        with open(path, "rb") as input_file:
            self.data = list(input_file.read())
