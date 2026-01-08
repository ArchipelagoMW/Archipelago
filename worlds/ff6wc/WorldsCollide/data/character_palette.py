from ..graphics.palette import Palette

class CharacterPalette(Palette):
    def __init__(self, id, data):
        self.id = id
        self.data = data

    def print(self):
        print(f"palette {self.id}:")
        print(super().__str__())
