
from worlds.AutoWorld import World

import math


text_mapping = {
    "A": 0x00, "B": 0x01, "C": 0x02, "D": 0x03, "E": 0x04, "F": 0x05, "G": 0x06, "H": 0x07, "I": 0x08, "J": 0x09,
    "K": 0x0A, "L": 0x0B, "M": 0x0C, "N": 0x0D, "O": 0x0E, "P": 0x0F, "Q": 0x10, "R": 0x11, "S": 0x12, "T": 0x13,
    "U": 0x14, "V": 0x15, "W": 0x16, "X": 0x17, "Y": 0x18, "Z": 0x19,

    "!": 0x1A, ".": 0x1B, "-": 0x1C, ",": 0x1D, "?": 0x1E, " ": 0x1F,

    "0": 0x22, "1": 0x23, "2": 0x24, "3": 0x25, "4": 0x26, "5": 0x27, "6": 0x28, "7": 0x29, "8": 0x2A, "9": 0x2B,

    "a": 0x40, "b": 0x41, "c": 0x42, "d": 0x43, "e": 0x44, "f": 0x45, "g": 0x46, "h": 0x47, "i": 0x48, "j": 0x49,
    "k": 0x4A, "l": 0x4B, "m": 0x4C, "n": 0x4D, "o": 0x4E, "p": 0x4F, "q": 0x50, "r": 0x51, "s": 0x52, "t": 0x53,
    "u": 0x54, "v": 0x55, "w": 0x56, "x": 0x57, "y": 0x58, "z": 0x59,

    "#": 0x5A, "(": 0x5B, ")": 0x5C, "'": 0x5D
}

stage_text_mapping = {
    "A": 0x00, "B": 0x01, "C": 0x02, "D": 0x03, "E": 0x04, "F": 0x05, "G": 0x06, "H": 0x07, "I": 0x08, "J": 0x09,
    "K": 0x0A, "L": 0x0B, "M": 0x0C, "N": 0x0D, "O": 0x0E, "P": 0x0F, "Q": 0x10, "R": 0x11, "S": 0x12, "T": 0x13,
    "U": 0x14, "V": 0x15, "W": 0x16, "X": 0x17, "Y": 0x18, "Z": 0x19,

    "!": 0x1A, ".": 0x1B, "-": 0x1C, ",": 0x1D, "?": 0x1E, " ": 0x1F,

    "0": 0x6B, "1": 0x64, "2": 0x65, "3": 0x66, "4": 0x67, "5": 0x68, "6": 0x69, "7": 0x6A, "8": 0x2A, "9": 0x2B,

    "a": 0x40, "b": 0x41, "c": 0x42, "d": 0x43, "e": 0x44, "f": 0x45, "g": 0x46, "h": 0x47, "i": 0x48, "j": 0x49,
    "k": 0x4A, "l": 0x4B, "m": 0x4C, "n": 0x4D, "o": 0x4E, "p": 0x4F, "q": 0x50, "r": 0x51, "s": 0x52, "t": 0x53,
    "u": 0x54, "v": 0x55, "w": 0x56, "x": 0x57, "y": 0x58, "z": 0x59,

    "#": 0x5A, "(": 0x5B, ")": 0x5C, "'": 0x5D,

    "@32": 0x32, "@33": 0x33, "@34": 0x34, "@35": 0x35, "@36": 0x36, "@37": 0x37, "@38": 0x38, "@39": 0x39, "@3A": 0x3A, "@3B": 0x3B, "@3C": 0x3C,
}

title_text_mapping = {
    "A": [0x0A, 0x38], "B": [0x0B, 0x38], "C": [0x0C, 0x38], "D": [0x0D, 0x38], "E": [0x0E, 0x38],
    "F": [0x0F, 0x38], "G": [0x10, 0x38], "H": [0x11, 0x38], "I": [0x12, 0x38], "J": [0x13, 0x38],
    "K": [0x14, 0x38], "L": [0x15, 0x38], "M": [0x16, 0x38], "N": [0x17, 0x38], "O": [0x18, 0x38],
    "P": [0x19, 0x38], "Q": [0x1A, 0x38], "R": [0x1B, 0x38], "S": [0x1C, 0x38], "T": [0x1D, 0x38],
    "U": [0x1E, 0x38], "V": [0x1F, 0x38], "W": [0x20, 0x38], "X": [0x21, 0x38], "Y": [0x22, 0x38],
    "Z": [0x23, 0x38], " ": [0xFC, 0x38], ".": [0x24, 0x38],
    "0": [0x00, 0x38], "1": [0x01, 0x38], "2": [0x02, 0x38], "3": [0x03, 0x38], "4": [0x04, 0x38],
    "5": [0x05, 0x38], "6": [0x06, 0x38], "7": [0x07, 0x38], "8": [0x08, 0x38], "9": [0x09, 0x38],
}

credits_text_mapping = {
    "A": [0x0A, 0x38], "B": [0x0B, 0x38], "C": [0x0C, 0x38], "D": [0x0D, 0x38], "E": [0x0E, 0x38],
    "F": [0x0F, 0x38], "G": [0x10, 0x38], "H": [0x11, 0x38], "I": [0x12, 0x38], "J": [0x13, 0x38],
    "K": [0x14, 0x38], "L": [0x15, 0x38], "M": [0x16, 0x38], "N": [0x17, 0x38], "O": [0x18, 0x38],
    "P": [0x19, 0x38], "Q": [0x1A, 0x38], "R": [0x1B, 0x38], "S": [0x1C, 0x38], "T": [0x1D, 0x38],
    "U": [0x1E, 0x38], "V": [0x1F, 0x38], "W": [0x20, 0x38], "X": [0x21, 0x38], "Y": [0x22, 0x38],
    "Z": [0x23, 0x38], " ": [0xFC, 0x00], ".": [0x24, 0x38],
    "0": [0x00, 0x38], "1": [0x01, 0x38], "2": [0x02, 0x38], "3": [0x03, 0x38], "4": [0x04, 0x28],
    "5": [0x05, 0x38], "6": [0x06, 0x38], "7": [0x07, 0x38], "8": [0x08, 0x38], "9": [0x09, 0x28],
}

credits_header_mapping = {
    "A": [0x0A, 0x28], "B": [0x0B, 0x28], "C": [0x0C, 0x28], "D": [0x0D, 0x28], "E": [0x0E, 0x28],
    "F": [0x0F, 0x28], "G": [0x10, 0x28], "H": [0x11, 0x28], "I": [0x12, 0x28], "J": [0x13, 0x28],
    "K": [0x14, 0x28], "L": [0x15, 0x28], "M": [0x16, 0x28], "N": [0x17, 0x28], "O": [0x18, 0x28],
    "P": [0x19, 0x28], "Q": [0x1A, 0x28], "R": [0x1B, 0x28], "S": [0x1C, 0x28], "T": [0x1D, 0x28],
    "U": [0x1E, 0x28], "V": [0x1F, 0x28], "W": [0x20, 0x28], "X": [0x21, 0x28], "Y": [0x22, 0x28],
    "Z": [0x23, 0x28], " ": [0xFC, 0x00], ".": [0x24, 0x28],
    "0": [0x00, 0x28], "1": [0x01, 0x28], "2": [0x02, 0x28], "3": [0x03, 0x28], "4": [0x04, 0x28],
    "5": [0x05, 0x28], "6": [0x06, 0x28], "7": [0x07, 0x28], "8": [0x08, 0x28], "9": [0x09, 0x28],
}


def string_to_bytes(input_string):
    out_array = bytearray()
    for letter in input_string:
        out_array.append(text_mapping[letter] if letter in text_mapping else text_mapping["."])

    return out_array


def generate_text_box(input_string):
    out_bytes = bytearray()
    box_line_count = 0
    box_line_chr_count = 0
    for word in input_string.split():
        if box_line_chr_count + len(word) > 18:
            out_bytes[-1] += 0x80
            box_line_count += 1
            box_line_chr_count = 0

        out_bytes.extend(string_to_bytes(word))
        box_line_chr_count += len(word)

        if box_line_chr_count < 18:
            box_line_chr_count += 1
            out_bytes.append(0x1F)

    for i in range(box_line_count, 8):
        out_bytes.append(0x9F)

    return out_bytes


def generate_goal_text(world: World):
    out_array = bytearray()
    if world.options.goal == "yoshi_egg_hunt":
        required_yoshi_eggs = world.required_egg_count
        actual_yoshi_eggs = world.actual_egg_count
        out_array += bytearray([0x9F, 0x9F])
        out_array += string_to_bytes(" You must acquire")
        out_array[-1] += 0x80
        out_array += string_to_bytes(f'    {required_yoshi_eggs:03} of {actual_yoshi_eggs:03}')
        out_array[-1] += 0x80
        out_array += string_to_bytes(f'    Yoshi Eggs,')
        out_array[-1] += 0x80
        out_array += string_to_bytes("then return here.")
        out_array[-1] += 0x80
        out_array += bytearray([0x9F, 0x9F])
    else:
        bosses_required = world.options.bosses_required.value
        out_array += bytearray([0x9F, 0x9F])
        out_array += string_to_bytes(" You must defeat")
        out_array[-1] += 0x80
        out_array += string_to_bytes(f'    {bosses_required:02} Bosses,')
        out_array[-1] += 0x80
        out_array += string_to_bytes("then defeat Bowser")
        out_array[-1] += 0x80
        out_array += bytearray([0x9F, 0x9F, 0x9F])

    return out_array


def generate_received_text(item_name: str, player_name: str):
    out_array = bytearray()

    item_name = item_name[:18]
    player_name = player_name[:18]

    item_buffer = max(0, math.floor((18 - len(item_name)) / 2))
    player_buffer = max(0, math.floor((18 - len(player_name)) / 2))

    out_array += bytearray([0x9F, 0x9F])
    out_array += string_to_bytes("     Received")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * item_buffer)
    out_array += string_to_bytes(item_name)
    out_array[-1] += 0x80
    out_array += string_to_bytes("       from")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * player_buffer)
    out_array += string_to_bytes(player_name)
    out_array[-1] += 0x80
    out_array += bytearray([0x9F, 0x9F])

    return out_array


def generate_received_trap_link_text(item_name: str, player_name: str):
    out_array = bytearray()

    item_name = item_name[:18]
    player_name = player_name[:18]

    item_buffer = max(0, math.floor((18 - len(item_name)) / 2))
    player_buffer = max(0, math.floor((18 - len(player_name)) / 2))

    out_array += bytearray([0x9F, 0x9F])
    out_array += string_to_bytes(" Received linked")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * item_buffer)
    out_array += string_to_bytes(item_name)
    out_array[-1] += 0x80
    out_array += string_to_bytes("       from")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * player_buffer)
    out_array += string_to_bytes(player_name)
    out_array[-1] += 0x80
    out_array += bytearray([0x9F, 0x9F])

    return out_array


def generate_sent_text(item_name: str, player_name: str):
    out_array = bytearray()

    item_name = item_name[:18]
    player_name = player_name[:18]

    item_buffer = max(0, math.floor((18 - len(item_name)) / 2))
    player_buffer = max(0, math.floor((18 - len(player_name)) / 2))

    out_array += bytearray([0x9F, 0x9F])
    out_array += string_to_bytes("       Sent")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * item_buffer)
    out_array += string_to_bytes(item_name)
    out_array[-1] += 0x80
    out_array += string_to_bytes("        to")
    out_array[-1] += 0x80
    out_array += bytearray([0x1F] * player_buffer)
    out_array += string_to_bytes(player_name)
    out_array[-1] += 0x80
    out_array += bytearray([0x9F, 0x9F])

    return out_array


def generate_credits() -> bytearray:
    out_array = bytearray()

    original_names: list[str] = [
        "TAKASHI TEZUKA",
        "HIDEQUI KONNO",
        "KATSUYA EGUCHI",
        "TOSHIHIKO NAKAGO",
        "TOSHIO IWAWAKI",
        "KAZUAKI MORITA",
        "SHIGEHIRO KASAMATSU",
        "TATSUO NISHIYAMA",
        "YOSHIHIRO NOMOMOTO",
        "EIJI NOTO",
        "SATORU TAKAHATA",
        "SHIGEFUMI HINO",
        "KOJI KONDO",
        "YOICHI KOTABE",
        "YASUHIRO SAKAI",
        "MIE YOSHIMURA",
        "HIRONOBU KAKUI",
        "KEIZO KATO",
        "TAKAO SHIMIZU",
        "DAYV BROOKS",
        "SHIGERU MIYAMOTO",
        "HIROSHI YAMAUCHI",
    ]

    ap_devs: list[str] = [
        "PORYGONE",
        "LX5",
    ]

    special_thanks: list[str] = [
        "ANONIMATO",
        "BIG BRAWLER",
        "IVAN SWORD",
        "MENTHOLEUS",
        "M.",
        "SHINY",
        "VASH VARKET",
        "RASPBERRYSPACEJAM",
        "THEBULBLAXEMPIRE",
    ]

    names_byte_length: int = 0x751

    original_offsets: list[int] = [0x00]

    out_array.extend(bytearray([0x07, 0x23]))
    for chr in "ORIGINAL SMW STAFF":
        out_array.extend(bytearray(credits_header_mapping[chr]))

    out_array.append(0xFF)

    for name in original_names:
        original_offsets.append(len(out_array))

        str_len: int = len(name)
        byte_len: int = str_len * 2 - 1

        column_offset: int = (32 - str_len) // 2
        out_array.append(column_offset)
        out_array.append(byte_len)

        for chr in name:
            out_array.extend(bytearray(credits_text_mapping[chr]))

    ap_offsets: list[int] = [len(out_array)]

    out_array.extend(bytearray([0x05, 0x2B]))
    for chr in "ARCHIPELAGO DEVELOPERS":
        out_array.extend(bytearray(credits_header_mapping[chr]))

    for name in ap_devs:
        ap_offsets.append(len(out_array))

        str_len: int = len(name)
        byte_len: int = str_len * 2 - 1

        column_offset: int = (32 - str_len) // 2
        out_array.append(column_offset)
        out_array.append(byte_len)

        for chr in name:
            out_array.extend(bytearray(credits_text_mapping[chr]))

    special_offsets: list[int] = [len(out_array)]

    out_array.extend(bytearray([0x07, 0x21]))
    for chr in "AP SPECIAL THANKS":
        out_array.extend(bytearray(credits_header_mapping[chr]))

    for name in special_thanks:
        special_offsets.append(len(out_array))

        str_len: int = len(name)
        byte_len: int = str_len * 2 - 1

        column_offset: int = (32 - str_len) // 2
        out_array.append(column_offset)
        out_array.append(byte_len)

        for chr in name:
            out_array.extend(bytearray(credits_text_mapping[chr]))

    while len(out_array) < names_byte_length:
        out_array.extend([0xFC, 0x00])

    offsets_byte_length: int = 0x194

    for offset in original_offsets:
        out_array.extend(bytearray([0x26, 0x00, 0x26, 0x00]))
        out_array += offset.to_bytes(2, "little")

    for i in range(8):
        out_array.extend(bytearray([0x26, 0x00]))

    for offset in ap_offsets:
        out_array.extend(bytearray([0x26, 0x00, 0x26, 0x00]))
        out_array += offset.to_bytes(2, "little")

    for i in range(8):
        out_array.extend(bytearray([0x26, 0x00]))

    for offset in special_offsets:
        out_array.extend(bytearray([0x26, 0x00, 0x26, 0x00]))
        out_array += offset.to_bytes(2, "little")

    while len(out_array) < (names_byte_length + offsets_byte_length):
        out_array.extend(bytearray([0x26, 0x00]))

    return out_array
