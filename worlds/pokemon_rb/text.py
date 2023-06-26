special_chars = {
    "PKMN": 0x4A,
    "LINE": 0x4F,
    "PARA": 0x51,
    "CONT": 0x55,
    "DONE": 0x57,
    "PROMPT": 0x58,
    "'d": 0xBB,
    "'l": 0xBC,
    "'t": 0xBE,
    "'v": 0xBF,
    "PK": 0xE1,
    "MN": 0xE2,
    "'r": 0xE4,
    "'m": 0xE5,
    "MALE": 0xEF,
    "FEMALE": 0xF5,
}

char_map = {
    "@": 0x50,  # String terminator
    "#": 0x54,  # Poké
    "‘": 0x70,
    "’": 0x71,
    "“": 0x72,
    "”": 0x73,
    "·": 0x74,
    "…": 0x75,
    " ": 0x7F,
    "A": 0x80,
    "B": 0x81,
    "C": 0x82,
    "D": 0x83,
    "E": 0x84,
    "F": 0x85,
    "G": 0x86,
    "H": 0x87,
    "I": 0x88,
    "J": 0x89,
    "K": 0x8A,
    "L": 0x8B,
    "M": 0x8C,
    "N": 0x8D,
    "O": 0x8E,
    "P": 0x8F,
    "Q": 0x90,
    "R": 0x91,
    "S": 0x92,
    "T": 0x93,
    "U": 0x94,
    "V": 0x95,
    "W": 0x96,
    "X": 0x97,
    "Y": 0x98,
    "Z": 0x99,
    "(": 0x9A,
    ")": 0x9B,
    ":": 0x9C,
    ";": 0x9D,
    "[": 0x9E,
    "]": 0x9F,
    "a": 0xA0,
    "b": 0xA1,
    "c": 0xA2,
    "d": 0xA3,
    "e": 0xA4,
    "f": 0xA5,
    "g": 0xA6,
    "h": 0xA7,
    "i": 0xA8,
    "j": 0xA9,
    "k": 0xAA,
    "l": 0xAB,
    "m": 0xAC,
    "n": 0xAD,
    "o": 0xAE,
    "p": 0xAF,
    "q": 0xB0,
    "r": 0xB1,
    "s": 0xB2,
    "t": 0xB3,
    "u": 0xB4,
    "v": 0xB5,
    "w": 0xB6,
    "x": 0xB7,
    "y": 0xB8,
    "z": 0xB9,
    "é": 0xBA,
    "'": 0xE0,
    "-": 0xE3,
    "?": 0xE6,
    "!": 0xE7,
    ".": 0xE8,
    "+": 0xEA,
    "=": 0xEB,
    "♂": 0xEF,
    "¥": 0xF0,
    "$": 0xF0,
    "×": 0xF1,
    "*": 0xF1,  # alias
    "/": 0xF3,
    ",": 0xF4,
    "♀": 0xF5,
    "0": 0xF6,
    "1": 0xF7,
    "2": 0xF8,
    "3": 0xF9,
    "4": 0xFA,
    "5": 0xFB,
    "6": 0xFC,
    "7": 0xFD,
    "8": 0xFE,
    "9": 0xFF,
}

unsafe_chars = ["@", "#", "PKMN", "LINE", "DONE", "CONT", "PROMPT"]


def encode_text(text: str, length: int=0, whitespace=False, force=False, safety=False):
    encoded_text = bytearray()
    spec_char = ""
    special = False
    for char in text:
        if char == ">":
            try:
                if spec_char in unsafe_chars and safety:
                    raise KeyError(f"Disallowed Pokemon text special character '<{spec_char}>'")
                encoded_text.append(special_chars[spec_char])
            except KeyError:
                if force:
                    encoded_text.append(char_map[" "])
                else:
                    raise KeyError(f"Invalid Pokemon text special character '<{spec_char}>'")
            spec_char = ""
            special = False
        elif char == "<":
            spec_char = ""
            special = True
        elif special is True:
            spec_char += char
        else:
            try:
                encoded_text.append(char_map[char])
                if char in unsafe_chars and safety:
                    raise KeyError(f"Disallowed Pokemon text character '{char}'")
            except KeyError:
                if force:
                    encoded_text.append(char_map[" "])
                else:
                    raise KeyError(f"Invalid Pokemon text character '{char}'")
    if length > 0:
        encoded_text = encoded_text[:length]
    while whitespace and len(encoded_text) < length:
        encoded_text.append(char_map[" " if whitespace is True else whitespace])
    return encoded_text
