from dataclasses import dataclass


def is_bit_set(data: bytes, index: int, offset: int = 0) -> bool:
    """
    Checks to see if the given bit is set.

    :param data: the data to check
    :param index: the index of the bit to check
    :param offset: number of bytes to skip before counting index bits
    """
    return data[offset + (index // 8)] & 1 << (index % 8)


def int_to_bcd(integer: int) -> int:
    """Encode integer value as SNES Binary Coded Decimal (BCD)."""
    bcd: int = integer % 10
    remainder: int = integer // 10
    digit: int = 1

    while remainder != 0:
        bcd += (remainder % 10) * (0x10**digit)
        remainder //= 10
        digit += 1

    return bcd


def bcd_to_int(bcd: int) -> int:
    """Decodes SNES Binary Coded Decimal (BCD) value to integer."""
    integer: int = bcd % 0x10
    remainder: int = bcd // 0x10
    digit: int = 1

    while remainder != 0:
        integer += (remainder % 10) * (10**digit)
        remainder //= 0x10
        digit += 1

    return integer


# Uses ? for missing characters which dont have a "close-enough" mapping.
# Non-printing ascii is left as-is and is likely to cause problems.
character_map = {
    "#": "?",
    "$": "?",
    "%": "?",
    "&": "?",
    # All single-quotes are under the backtick charcode for some reason.
    "'": "`",
    "*": "?",
    "+": "?",
    # Best match.
    ";": ":",
    # '<' and '>' are used for 'smart' quotes.
    "<": "(",
    ">": ")",
    "=": "?",
    # This one is also a space chracter used with characters who speak in the small 8x8 font.
    "@": "?",
    # More "close-enough" mappings
    "[": "(",
    "]": ")",
    "\\": "/",
    "^": "?",
    "_": " ",
    "{": "(",
    "}": ")",
    "|": "?",
    "~": "?",
    "\t": " ",
    # Unicode mappings for some of the special encodings.
    # Unlikely to ever be useful, but you never know.
    "“": "<",
    "”": ">",
    "␈": "$",
    "␃": "#",
    "⚔️": "&",
    "🛡️": "'",
    "⏷": "=",
    "⏵": "+",
    "↑": "\\",
    "↗": "]",
    "→": "^",
    "↘": "_",
    "↓": "|",
    "↙": "}",
    "←": "~",
    "↖": "\x7F",
}


def encode_string(string: str, buffer_size: int) -> bytes:
    """Encodes a string into the format used by Soul Blazer."""
    mapped = str.join("", [character_map.get(char, char) for char in string])
    # TODO: Could also use libraries like unidecode and smartypants to make better transformations
    return mapped[: buffer_size - 1].encode("ascii", "replace") + bytes([0x00])


@dataclass(frozen=True)
class Rectangle:
    x: int
    """X coord of top left corner of Rectangle."""
    y: int
    """Y coord of top left corner of Rectangle."""
    width: int
    """0-indexed, so a two tile wide rect would have a width of 1"""
    height: int
    """0-indexed, so a two tile high rect would have a height of 1"""

    def contains(self, x: int, y: int) -> bool:
        return self.x <= x <= self.x + self.width and self.y <= y <= self.y + self.height
