from ...data.structures import DataArray
from ...memory.space import Space

class Widths:
    WIDTHS_START = 0x048fc0
    WIDTHS_END = 0x0490bf
    WIDTH_SIZE = 1

    def __init__(self):
        self.widths = DataArray(Space.rom, self.WIDTHS_START, self.WIDTHS_END, self.WIDTH_SIZE)

    def __len__(self):
        return len(self.widths)

    def __getitem__(self, index):
        return self.widths[index][0]

    def width(self, string):
        from ...data.text.text1 import text_value

        result = 0
        for character in string:
            result += self[text_value[character]]
        return result
