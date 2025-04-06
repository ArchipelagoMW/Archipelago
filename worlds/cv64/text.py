from typing import Tuple

cv64_char_dict = {"\n": (0x01, 0), " ": (0x02, 4), "!": (0x03, 2), '"': (0x04, 5), "#": (0x05, 6), "$": (0x06, 5),
                  "%": (0x07, 8), "&": (0x08, 7), "'": (0x09, 4), "(": (0x0A, 3), ")": (0x0B, 3), "*": (0x0C, 4),
                  "+": (0x0D, 5), ",": (0x0E, 3), "-": (0x0F, 4), ".": (0x10, 3), "/": (0x11, 6), "0": (0x12, 5),
                  "1": (0x13, 3), "2": (0x14, 5), "3": (0x15, 4), "4": (0x16, 5), "5": (0x17, 5), "6": (0x18, 5),
                  "7": (0x19, 5), "8": (0x1A, 5), "9": (0x1B, 5), ":": (0x1C, 3), ";": (0x1D, 3), "<": (0x1E, 3),
                  "=": (0x1F, 4), ">": (0x20, 3), "?": (0x21, 5), "@": (0x22, 8), "A": (0x23, 7), "B": (0x24, 6),
                  "C": (0x25, 5), "D": (0x26, 7), "E": (0x27, 5), "F": (0x28, 6), "G": (0x29, 6), "H": (0x2A, 7),
                  "I": (0x2B, 3), "J": (0x2C, 3), "K": (0x2D, 6), "L": (0x2E, 6), "M": (0x2F, 8), "N": (0x30, 7),
                  "O": (0x31, 6), "P": (0x32, 6), "Q": (0x33, 8), "R": (0x34, 6), "S": (0x35, 5), "T": (0x36, 6),
                  "U": (0x37, 6), "V": (0x38, 7), "W": (0x39, 8), "X": (0x3A, 6), "Y": (0x3B, 7), "Z": (0x3C, 6),
                  "[": (0x3D, 3), "\\": (0x3E, 6), "]": (0x3F, 3), "^": (0x40, 6), "_": (0x41, 5), "a": (0x43, 5),
                  "b": (0x44, 6), "c": (0x45, 4), "d": (0x46, 6), "e": (0x47, 5), "f": (0x48, 5), "g": (0x49, 5),
                  "h": (0x4A, 6), "i": (0x4B, 3), "j": (0x4C, 3), "k": (0x4D, 6), "l": (0x4E, 3), "m": (0x4F, 8),
                  "n": (0x50, 6), "o": (0x51, 5), "p": (0x52, 5), "q": (0x53, 5), "r": (0x54, 4), "s": (0x55, 4),
                  "t": (0x56, 4), "u": (0x57, 5), "v": (0x58, 6), "w": (0x59, 8), "x": (0x5A, 5), "y": (0x5B, 5),
                  "z": (0x5C, 4), "{": (0x5D, 4), "|": (0x5E, 2), "}": (0x5F, 3), "`": (0x61, 4), "「": (0x62, 3),
                  "」": (0x63, 3), "~": (0x65, 3), "″": (0x72, 3), "°": (0x73, 3), "∞": (0x74, 8)}
# [0] = CV64's in-game ID for that text character.
# [1] = How much space towards the in-game line length limit it contributes.


def cv64_string_to_bytearray(cv64text: str, a_advance: bool = False, append_end: bool = True) -> bytearray:
    """Converts a string into a bytearray following CV64's string format."""
    text_bytes = bytearray(0)
    for i, char in enumerate(cv64text):
        if char == "\t":
            text_bytes.extend([0xFF, 0xFF])
        else:
            if char in cv64_char_dict:
                text_bytes.extend([0x00, cv64_char_dict[char][0]])
            else:
                text_bytes.extend([0x00, 0x21])

    if a_advance:
        text_bytes.extend([0xA3, 0x00])
    if append_end:
        text_bytes.extend([0xFF, 0xFF])
    return text_bytes


def cv64_text_truncate(cv64text: str, textbox_len_limit: int) -> str:
    """Truncates a string at a given in-game text line length."""
    line_len = 0

    for i in range(len(cv64text)):
        if cv64text[i] in cv64_char_dict:
            line_len += cv64_char_dict[cv64text[i]][1]
        else:
            line_len += 5

        if line_len > textbox_len_limit:
            return cv64text[0x00:i]

    return cv64text


def cv64_text_wrap(cv64text: str, textbox_len_limit: int) -> Tuple[str, int]:
    """Rebuilds a string with some of its spaces replaced with newlines to ensure the text wraps properly in an in-game
    textbox of a given length."""
    words = cv64text.split(" ")
    new_text = ""
    line_len = 0
    num_lines = 1

    for i in range(len(words)):
        word_len = 0
        word_divider = " "

        if line_len != 0:
            line_len += 4
        else:
            word_divider = ""

        for char in words[i]:
            if char in cv64_char_dict:
                line_len += cv64_char_dict[char][1]
                word_len += cv64_char_dict[char][1]
            else:
                line_len += 5
                word_len += 5

            if word_len > textbox_len_limit or char in ["\n", "\t"]:
                word_len = 0
                line_len = 0
                if num_lines < 4:
                    num_lines += 1

            if line_len > textbox_len_limit:
                word_divider = "\n"
                line_len = word_len
                if num_lines < 4:
                    num_lines += 1

        new_text += word_divider + words[i]

    return new_text, num_lines
