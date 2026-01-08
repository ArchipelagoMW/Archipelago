from __future__ import annotations

from io import StringIO
import itertools
import pkgutil
from typing import Iterable, SupportsIndex, overload


char_table = {}
character_widths = [
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    6, 6, 7, 7, 7, 8, 8, 4, 5, 5, 7, 7, 4, 8, 4, 7,
    7, 5, 7, 7, 7, 7, 7, 7, 7, 7, 4, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 8, 7, 7,
    7, 7, 7, 7, 6, 7, 8, 8, 8, 6, 7, 5, 7, 5, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 6, 6, 6, 6, 6, 5, 6, 6, 2, 5, 5, 3, 6, 6, 6,
    6, 6, 5, 6, 5, 6, 6, 6, 6, 6, 6, 5, 3, 5, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 6, 8, 8, 8, 8, 8, 16, 8, 11, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    14, 8, 14, 8, 14, 8, 14, 8, 14, 8, 14, 8, 16, 8, 16, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    6, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 7, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 7, 7, 7, 7, 7, 7, 7, 7, 6, 7, 7, 7, 7, 7, 7,
    7, 7, 7, 7, 6, 7, 7, 7, 7, 6, 7, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8,
    8, 6, 6, 6, 6, 6, 5, 6, 6, 2, 5, 5, 3, 6, 6, 6,
    6, 6, 5, 6, 5, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8
]


def _get_charmap():
    char_data = pkgutil.get_data(__name__, "data/charmap.txt").decode("utf-8")
    with StringIO(char_data) as stream:
        for line in stream:
            splits = line.rsplit("=", 1)
            if len(splits) == 1:
                continue
            char, enc = map(str.strip, splits)
            if "'" not in char:
                continue
            char = char[1:-1]
            if len(char) != 1:
                continue  # TODO: Check if there are any multi-codepoint sequences and if we want to encode those
            enc = int(enc, 16)
            char_table[char] = enc
    char_table["\'"] = 0x0047
    char_table["\n"] = 0xFE00


_get_charmap()


LINE_WIDTH = 224

SPACE = 0x0040
NEWLINE = 0xFE00
TERMINATOR_CHAR = 0xFF00


def get_width_of_encoded_character(char: int):
    if char & 0xFF00 == 0x8000:  # Padding control char
        return char & 0x00FF
    if char & 0xFF00 == 0x8100:  # Text color control char
        return 0
    if char == TERMINATOR_CHAR:
        return 0
    if char >= 1184:
        return 10
    if char >= len(character_widths):
        return 0
    return character_widths[char]


class Message:
    buffer: list[int]

    @overload
    def __init__(self, string: str):
        ...

    @overload
    def __init__(self, characters: Iterable[int]):
        ...

    def __init__(self, value: str | Iterable[int]):
        if isinstance(value, str):
            self.buffer = list(char_table.get(c, char_table[" "]) for c in value)
        else:
            self.buffer = list(value)
            for char in self.buffer:
                self._range_check(char)

    @staticmethod
    def _range_check(char: int):
        if char < 0:
            raise ValueError(f"Character value must be nonnegative: {char:04x}")
        if char > 0xFFFF:
            raise ValueError(f"Character value must be 0xFFFF or less: {char:04x}")

    def append(self, char: int):
        self._range_check(char)
        self.buffer.append(char)
        return self

    def insert(self, index: SupportsIndex, char: int):
        self._range_check(char)
        self.buffer.insert(index, char)
        return self

    def display_width(self):
        return sum(get_width_of_encoded_character(c) for c in self)

    def trim_to_max_width(self, max_width: int = LINE_WIDTH):
        if len(self.buffer) == 0:
            return self
        total_width = 0
        buffer: list[int] = []
        for char in self:
            next_width = total_width + get_width_of_encoded_character(char)
            if next_width > max_width:
                break
            buffer.append(char)
            total_width = next_width
        if self.buffer[-1] == TERMINATOR_CHAR and buffer[-1] != TERMINATOR_CHAR:
            buffer.append(TERMINATOR_CHAR)
        self.buffer = buffer
        return self

    def center_align(self, line_width: int = LINE_WIDTH):
        pad = ((line_width - self.display_width()) // 2) & 0xFF
        return self.insert(0, 0x8000 | pad)

    def to_bytes(self):
        return bytes(itertools.chain.from_iterable(c.to_bytes(2, "little") for c in self))

    def __add__(self, other: Message):
        return Message(self.buffer + other.buffer)

    def __iadd__(self, other: Message):
        self.buffer += other.buffer

    def __len__(self):
        return len(self.buffer)

    def __getitem__(self, key: int):
        return self.buffer[key]

    def __setitem__(self, key: int, value: int):
        self._range_check(value)
        self.buffer[key] = value

    def __delitem__(self, key: int):
        del self.buffer[key]

    def __iter__(self):
        return iter(self.buffer)

    def __reversed__(self):
        return reversed(self.buffer)

    def __contains__(self, item: int):
        return item in self.buffer


def make_item_message(first: str, second: str) -> Message:
    first_msg = Message(first).trim_to_max_width().insert(0, 0x8105).center_align()
    first_msg.append(NEWLINE)
    second_msg = Message(second).trim_to_max_width().center_align()
    second_msg.append(TERMINATOR_CHAR)
    return first_msg + second_msg
