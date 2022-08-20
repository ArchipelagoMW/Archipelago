
from BaseClasses import MultiWorld

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
}


def string_to_bytes(input_string):
    out_array = bytearray()
    for letter in input_string:
        out_array.append(text_mapping[letter])

    return out_array


def generate_goal_text(world: MultiWorld, player: int):
    out_array = bytearray()
    if world.goal[player] == "yoshi_egg_hunt":
        required_yoshi_eggs = max(math.floor(
                world.number_of_yoshi_eggs[player].value * (world.percentage_of_yoshi_eggs[player].value / 100.0)), 1)
        out_array += bytearray([0x9F, 0x9F])
        out_array += string_to_bytes(" You must acquire")
        out_array[-1] += 0x80
        out_array += string_to_bytes(f'  {required_yoshi_eggs:02} Yoshi Eggs,')
        out_array[-1] += 0x80
        out_array += string_to_bytes("then return here.")
        out_array[-1] += 0x80
        out_array += bytearray([0x9F, 0x9F, 0x9F])
    else:
        bosses_required = world.bosses_required[player].value
        out_array += bytearray([0x9F, 0x9F])
        out_array += string_to_bytes(" You must defeat")
        out_array[-1] += 0x80
        out_array += string_to_bytes(f'    {bosses_required:02} Bosses,')
        out_array[-1] += 0x80
        out_array += string_to_bytes("then defeat Bowser")
        out_array[-1] += 0x80
        out_array += bytearray([0x9F, 0x9F, 0x9F])

    return out_array

