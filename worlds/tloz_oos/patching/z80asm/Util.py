import collections
import re
from typing import List

from worlds.tloz_oos.patching.z80asm.Errors import ArgumentOverflowError


def strip_line(line: str) -> str:
    """
    Strips indent and comment from line, if present.
    """
    line = line.strip()
    return re.sub(r" *[;#].*\n?", "", line)


def parse_hex_string_to_value(string: str) -> int:
    """
    Parse an hexadecimal string into a numeric value, handling some operators
    """
    string = string.replace("$", "")
    if "+" in string:
        split = string.split("+")
        return int(split[0], 16) + int(split[1], 16)
    elif "-" in string:
        split = string.split("-")
        return int(split[0], 16) - int(split[1], 16)
    elif "*" in string:
        split = string.split("*")
        return int(split[0], 16) * int(split[1], 16)
    elif "|" in string:
        split = string.split("|")
        return int(split[0], 16) | int(split[1], 16)
    else:
        return int(string, 16)


def parse_bin_string_to_value(string: str) -> int:
    """
    Parse a binary string into a numeric value as small endian, no operator is supported
    """
    return int(string[:0:-1], 2)


def value_to_byte_array(value: int, expected_size: int):
    """
    Converts a value into a little endian byte array
    (e.g. "0x4Fa7DEadBEef" => [0xef, 0xbe, 0xad, 0xde, 0xa7, 0x4f])
    """
    output = []
    while value > 0:
        output.append(value & 0xFF)
        value >>= 8
    if len(output) > expected_size:
        raise ArgumentOverflowError(value, expected_size)
    while len(output) < expected_size:
        output.append(0x00)

    return output


def parse_byte(string: str) -> int:
    if string.startswith("$"):
        return parse_hex_byte(string)
    elif string.startswith("%"):
        return parse_bin_string_to_value(string)
    else:
        raise Exception(f"Invalid byte string : {string}")


def parse_hex_byte(string: str) -> int:
    """
    Converts a byte literal hexadecimal string into a byte value
    (e.g. "$4F" => 0x4f)
    """
    value = parse_hex_string_to_value(string)
    return value_to_byte_array(value, 1)[0]


def parse_hex_word(string: str):
    """
    Converts a word literal hexadecimal string into a little endian byte array
    (e.g. "$4Fa7" => [0xa7, 0x4f])
    """
    value = parse_hex_string_to_value(string)
    return value_to_byte_array(value, 2)


def parse_argument(arg: str, mnemonic_subtree: collections.abc.Mapping) -> (str, List[int]):
    """
    Parse an argument to extract a generic form and potential extra bytes
        "$1a"     => ("$8",     [0x1a])
        "($c43f)" => ("($16)",  [0x3f,0xc4])
        "bc"      => ("bc",     [])
        "$04+$29" => ("$8",     [0x2d])
    """
    arg = arg.strip()
    enclosed_in_parentheses = arg.startswith("(") and arg.endswith(")")
    if enclosed_in_parentheses:
        arg = arg[1:-1]

    # If argument is a literal, determine the expected size of that literal using the
    # mnemonic subtree that was passed as parameter
    if arg.startswith("$") or arg.startswith("%"):
        value = 0
        try:
            if arg.startswith("$"):
                value = parse_hex_string_to_value(arg)
            else:
                value = parse_bin_string_to_value(arg)
        except ValueError:
            pass

        for size in [8, 16]:
            generic_arg = f"${size}"
            if enclosed_in_parentheses:
                generic_arg = f"({generic_arg})"
            if generic_arg in mnemonic_subtree:
                return generic_arg, value_to_byte_array(value, int(size / 8))

    # If we reached that point, this means we need to keep the symbol as it is: it can be a register name,
    # or an invalid name which will get rejected at a later point
    if enclosed_in_parentheses:
        return f"({arg})", []
    else:
        return arg, []
