from docutils.io import InputError

from BaseClasses import ItemClassification
from .items import zodiac_stone_names


class TextData:
    character: str
    id: int
    width: int

    def __init__(self, character: str, id: int, width: int = 6):
        self.character = character
        self.id = id
        self.width = width


all_characters: list[TextData] = [
    TextData("0", 0x00),
    TextData("1", 0x01),
    TextData("2", 0x02),
    TextData("3", 0x03),
    TextData("4", 0x04),
    TextData("5", 0x05),
    TextData("6", 0x06),
    TextData("7", 0x07),
    TextData("8", 0x08),
    TextData("9", 0x09),

    TextData("A", 0x0A),
    TextData("B", 0x0B),
    TextData("C", 0x0C),
    TextData("D", 0x0D),
    TextData("E", 0x0E),
    TextData("F", 0x0F),
    TextData("G", 0x10),
    TextData("H", 0x11),
    TextData("I", 0x12, 4),
    TextData("J", 0x13),
    TextData("K", 0x14),
    TextData("L", 0x15),
    TextData("M", 0x16),
    TextData("N", 0x17),
    TextData("O", 0x18),
    TextData("P", 0x19),
    TextData("Q", 0x1A),
    TextData("R", 0x1B),
    TextData("S", 0x1C),
    TextData("T", 0x1D),
    TextData("U", 0x1E),
    TextData("V", 0x1F),
    TextData("W", 0x20),
    TextData("X", 0x21),
    TextData("Y", 0x22),
    TextData("Z", 0x23),

    TextData("a", 0x24, 4),
    TextData("b", 0x25, 4),
    TextData("c", 0x26, 4),
    TextData("d", 0x27, 4),
    TextData("e", 0x28, 4),
    TextData("f", 0x29, 4),
    TextData("g", 0x2A, 4),
    TextData("h", 0x2B, 4),
    TextData("i", 0x2C, 2),
    TextData("j", 0x2D, 4),
    TextData("k", 0x2E, 4),
    TextData("l", 0x2F, 2),
    TextData("m", 0x30, 6),
    TextData("n", 0x31, 4),
    TextData("o", 0x32, 4),
    TextData("p", 0x33, 4),
    TextData("q", 0x34, 4),
    TextData("r", 0x35, 4),
    TextData("s", 0x36, 4),
    TextData("t", 0x37, 4),
    TextData("u", 0x38, 4),
    TextData("v", 0x39, 4),
    TextData("w", 0x3A, 6),
    TextData("x", 0x3B, 4),
    TextData("y", 0x3C, 4),
    TextData("z", 0x3D, 4),

    TextData("!", 0x3E, 4),
    TextData("?", 0x40),
    #TextData("+", 0x42),
    TextData("/", 0x44),
    TextData(":", 0x46, 4),
    TextData(".", 0x5F, 4),
    TextData("(", 0x8D, 4),
    TextData(")", 0x8E, 4),
    TextData("\"", 0x91, 4),
    TextData("'", 0x93, 4),
    TextData("♪", 0xB2, 10),
    TextData("*", 0xB5, 10),
    TextData(",", 0xDA74, 4),
    #TextData(".", 0xD11C, 2),

    TextData("-", 0xD11D, 2),
    TextData("+", 0xD11E, 2),
    TextData("×", 0xD11F, 2),
    TextData("÷", 0xD120, 2),

    TextData("&", 0xD9B7),
    TextData("%", 0xD9B8),

    TextData("{Aries}", 0xDA00, 10),
    TextData("{Taurus}", 0xDA01, 10),
    TextData("{Gemini}", 0xDA02, 10),
    TextData("{Cancer}", 0xDA03, 10),
    TextData("{Leo}", 0xDA04, 10),
    TextData("{Virgo}", 0xDA05, 10),
    TextData("{Libra}", 0xDA06, 10),
    TextData("{Scorpio}", 0xDA07, 10),
    TextData("{Sagittarius}", 0xDA08, 10),
    TextData("{Capricorn}", 0xDA09, 10),
    TextData("{Aquarius}", 0xDA0A, 10),
    TextData("{Pisces}", 0xDA0B, 10),
    TextData("{Serpentarius}", 0xDA0C, 10),

    TextData("=", 0xDA0C, 6),
    TextData("$", 0xDA0C, 6),
    TextData("¥", 0xDA0C, 6),

    TextData(" ", 0xDA73, 2),
    TextData("{unitname}", 0xE1),
    TextData("{Newline}", 0xF8),
    TextData("{End}", 0xFE),
    TextData("{ColorNormal}", 0xE300, 0),
    TextData("{ColorSpecial1}", 0xE304, 0),
    TextData("{ColorSpecial2}", 0xE308, 0),
    TextData("{ColorSpecial3}", 0xE3FF, 0)
]

text_data_lookup = {
    text_data.character: text_data for text_data in all_characters
}

max_text_width = 180

def create_text_for_offworld_item(player_name: str, item_name: str, classification: ItemClassification, is_fft_item: bool):
    if is_fft_item and item_name in zodiac_stone_names:
        item_string = f"{{{item_name}}}" + f"{item_name}"
    else:
        item_string = f"{item_name}"
    if classification == ItemClassification.progression:
        item_string = "{ColorSpecial2}" + f"{item_string}" + "{ColorNormal}"
    elif classification == ItemClassification.useful:
        item_string = f"{item_string}"
    elif classification == ItemClassification.trap:
        item_string = "{ColorSpecial1}" + f"{item_string}" + "{ColorNormal}"
    else:
        item_string = "{ColorSpecial1}" + f"{item_string}" + "{ColorNormal}"
    return f"{player_name}'s {item_string}"

def create_text_for_own_item(item_name: str, classification: ItemClassification):
    if item_name in zodiac_stone_names:
        item_string = f"{{{item_name}}}" + f"{item_name}"
    else:
        item_string = f"{item_name}"
    if classification == ItemClassification.progression:
        item_string = "{ColorSpecial2}" + f"{item_string}" + "{ColorNormal}"
    elif classification == ItemClassification.useful:
        item_string = f"{item_string}"
    elif classification == ItemClassification.trap:
        item_string = "{ColorSpecial1}" + f"{item_string}" + "{ColorNormal}"
    else:
        item_string = "{ColorSpecial1}" + f"{item_string}" + "{ColorNormal}"
    return f"their own {item_string}"

def split_text_into_lines(location_text: str) -> tuple[list[str], list[list[int]]]:
    lines: list[str] = []
    byte_lines: list[list[int]] = []
    current_line_width = 0
    index = 0
    current_line = ""
    current_bytes = []
    last_space_index = 0
    while index < len(location_text):
        character = location_text[index]
        if character not in ["{", "}"]:
            data_key = character
            index += 1
        elif character == "{":
            start = index
            end = location_text.index("}", start)
            data_key = location_text[start:end + 1]
            index = end + 1
        else:
            print(character)
            print(index)
            raise InputError("We shouldn't be processing this.")
        if data_key not in text_data_lookup.keys():
            data_key = "?"
        data = text_data_lookup[data_key]
        if current_line_width + data.width > max_text_width:
            last_space = current_line.rfind(" ")
            last_space_byte = -1
            for byte_index, value in enumerate(current_bytes):
                if value == 0x73:
                    last_space_byte = byte_index
            if last_space == -1:
                lines.append(current_line)
                byte_lines.append(current_bytes)
                current_line = data_key
                current_bytes = [data.id]
                current_line_width = 0
            else:
                lines.append(current_line[:last_space])
                byte_lines.append(current_bytes[:last_space_byte - 1])
                current_line = current_line[last_space + 1:] + data_key
                current_bytes = current_bytes[last_space_byte + 1:]
                if data.id > 0xFF:
                    current_bytes.append((data.id & 0xFF00) >> 8)
                    current_bytes.append(data.id & 0xFF)
                else:
                    current_bytes.append(data.id)
                current_line_width = 0
                sub_index = 0
                while sub_index < len(current_line):
                    sub_character = current_line[sub_index]
                    if sub_character not in ["{", "}"]:
                        sub_data_key = character
                        sub_index += 1
                    elif sub_character == "{":
                        sub_start = sub_index
                        sub_end = current_line.index("}", sub_start)
                        sub_data_key = current_line[sub_start:sub_end + 1]
                        sub_index = sub_end + 1
                    else:
                        print(character)
                        print(index)
                        raise InputError("We shouldn't be processing this.")
                    if sub_data_key not in text_data_lookup.keys():
                        sub_data_key = "?"
                    sub_data = text_data_lookup[sub_data_key]
                    current_line_width += sub_data.width
        else:
            current_line_width += data.width
            current_line += data_key
            if data.id > 0xFF:
                current_bytes.append((data.id & 0xFF00) >> 8)
                current_bytes.append(data.id & 0xFF)
            else:
                current_bytes.append(data.id)
    if len(current_line) > 0:
        lines.append(current_line)
        byte_lines.append(current_bytes)
    for line in byte_lines[:-1]:
        line.append(text_data_lookup["{Newline}"].id)
    byte_lines[-1].append(text_data_lookup["{End}"].id)
    return lines, byte_lines