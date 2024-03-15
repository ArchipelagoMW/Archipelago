
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
