from typing import DefaultDict
from collections import defaultdict

MM2_WEAPON_ENCODING: DefaultDict[str, int] = defaultdict(lambda: 0x6F, {
    ' ': 0x40,
    'A': 0x41,
    'B': 0x42,
    'C': 0x43,
    'D': 0x44,
    'E': 0x45,
    'F': 0x46,
    'G': 0x47,
    'H': 0x48,
    'I': 0x49,
    'J': 0x4A,
    'K': 0x4B,
    'L': 0x4C,
    'M': 0x4D,
    'N': 0x4E,
    'O': 0x4F,
    'P': 0x50,
    'Q': 0x51,
    'R': 0x52,
    'S': 0x53,
    'T': 0x54,
    'U': 0x55,
    'V': 0x56,
    'W': 0x57,
    'X': 0x58,
    'Y': 0x59,
    'Z': 0x5A,
    # 0x5B is the small r in Dr Light
    '.': 0x5C,
    ',': 0x5D,
    '\'': 0x5E,
    '!': 0x5F,
    '(': 0x60,
    ')': 0x61,
    '#': 0x62,
    '$': 0x63,
    '%': 0x64,
    '&': 0x65,
    '*': 0x66,
    '+': 0x67,
    '/': 0x68,
    '\\': 0x69,
    ':': 0x6A,
    ';': 0x6B,
    '<': 0x6C,
    '>': 0x6D,
    '=': 0x6E,
    '?': 0x6F,
    '@': 0x70,
    '[': 0x71,
    ']': 0x72,
    '^': 0x73,
    '_': 0x74,
    '`': 0x75,
    '{': 0x76,
    '}': 0x77,
    '|': 0x78,
    '~': 0x79,
    '\"': 0x92,
    '-': 0x94,
    '0': 0xA0,
    '1': 0xA1,
    '2': 0xA2,
    '3': 0xA3,
    '4': 0xA4,
    '5': 0xA5,
    '6': 0xA6,
    '7': 0xA7,
    '8': 0xA8,
    '9': 0xA9,
})


class MM2TextEntry:
    def __init__(self, text: str = "", coords: int = 0x0B):
        self.target_area: int = 0x25  # don't change
        self.coords: int = coords  # 0xYX, Y can only be increments of 0x20
        self.text: str = text

    def resolve(self) -> bytes:
        data = bytearray()
        data.append(self.target_area)
        data.append(self.coords)
        data.extend([MM2_WEAPON_ENCODING[x] for x in self.text.upper()])
        data.extend([0x40] * (14 - len(self.text)))
        return bytes(data)
