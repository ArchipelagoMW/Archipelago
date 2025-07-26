from collections import defaultdict
from typing import DefaultDict

MM3_WEAPON_ENCODING: DefaultDict[str, int] = defaultdict(lambda: 0x25, {
    '0': 0x00,
    '1': 0x01,
    '2': 0x02,
    '3': 0x03,
    '4': 0x04,
    '5': 0x05,
    '6': 0x06,
    '7': 0x07,
    '8': 0x08,
    '9': 0x09,
    'A': 0x0A,
    'B': 0x0B,
    'C': 0x0C,
    'D': 0x0D,
    'E': 0x0E,
    'F': 0x0F,
    'G': 0x10,
    'H': 0x11,
    'I': 0x12,
    'J': 0x13,
    'K': 0x14,
    'L': 0x15,
    'M': 0x16,
    'N': 0x17,
    'O': 0x18,
    'P': 0x19,
    'Q': 0x1A,
    'R': 0x1B,
    'S': 0x1C,
    'T': 0x1D,
    'U': 0x1E,
    'V': 0x1F,
    'W': 0x20,
    'X': 0x21,
    'Y': 0x22,
    'Z': 0x23,
    ' ': 0x25,
    '.': 0x26,
    ',': 0x27,
    '\'': 0x28,
    '!': 0x29,
    ':': 0x2B
})


class MM3TextEntry:
    def __init__(self, text: str = "", y_coords: int = 0xA5, row: int = 0x21):
        self.target_area: int = row  # don't change
        self.coords: int = y_coords  # 0xYX, Y can only be increments of 0x20
        self.text: str = text

    def resolve(self) -> bytes:
        data = bytearray()
        data.append(self.target_area)
        data.append(self.coords)
        data.append(12)
        data.extend([MM3_WEAPON_ENCODING[x] for x in self.text.upper()])
        data.extend([0x25] * (13 - len(self.text)))
        return bytes(data)
