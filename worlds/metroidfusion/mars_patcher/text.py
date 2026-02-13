import json
import os
import pkgutil
from enum import Enum
from functools import cache

from .constants.game_data import character_widths
from .mf.constants.game_data import file_screen_text_ptrs
from .mf.data import get_data_path
from .rom import Region, Rom

SPACE_CHAR = 0x40
SPACE_TAG = 0x8000
NEXT = 0xFD00
NEWLINE = 0xFE00
END = 0xFF00
VALUE_MARKUP_TAG = {
    "SPACE": (SPACE_TAG, 8),
    "COLOR": (0x8100, 8),
    "SPEED": (0x8200, 8),
    "INDENT": (0x8300, 8),
    "PLAY_SOUND": (0x9000, 12),
    "STOP_SOUND": (0xA000, 12),
    "WAIT": (0xE100, 8),
}
BREAKING_CHARS = {SPACE_CHAR, NEXT, NEWLINE}
NEWLINE_CHARS = {NEXT, NEWLINE}

KANJI_START = 0x4A0
KANJI_WIDTH = 10
MAX_LINE_WIDTH = 224


class Language(Enum):
    JAPANESE_KANJI = 0
    JAPANESE_HIRAGANA = 1
    ENGLISH = 2
    GERMAN = 3
    FRENCH = 4
    ITALIAN = 5
    SPANISH = 6


class MessageType(Enum):
    """Message types for encoding."""

    ONE_LINE = 0
    """Used for text that can only span one line (ex: location banner)."""
    TWO_LINE = 1
    """Used for text that can only span two lines (ex: item/event message,
    pause screen objective)."""
    CONTINUOUS = 2
    """Used for text where the A button can advance text."""


@cache
def get_char_map(region: Region) -> dict[str, int]:
    path = os.path.join("mf", "data", "char_map_mf.json")
    sections = json.loads(pkgutil.get_data(__name__, path).decode())
    char_map: dict[str, int] = {}
    for section in sections:
        if region.name in section["regions"]:
            char_map.update(section["chars"])
    char_map["\n"] = NEWLINE
    return char_map


def parse_value_markup_tag(tag: str) -> int | None:
    """Used to try parsing a markup tag with an assignable value.
    Returns the resulting character value, or None if not a markup tag."""
    items = tag.split("=", 1)
    if len(items) != 2:
        return None
    label, value_str = items
    if label in VALUE_MARKUP_TAG:
        char_val, bits = VALUE_MARKUP_TAG[label]
        value = int(value_str, 16)
        if value < 0 or value >= (1 << bits):
            raise ValueError(f"Value {value} is not valid for {label}")
        return char_val | value
    raise ValueError(f"Invalid value markup tag '{tag}'")


def get_char_width(rom: Rom, char_widths_addr: int, char_val: int) -> int:
    if char_val >= 0x8000:
        return 0
    if char_val < KANJI_START:
        return rom.read_8(char_widths_addr + char_val)
    return KANJI_WIDTH


def center_text(rom: Rom, char_vals: list[int], max_width: int) -> None:
    char_widths_addr = character_widths(rom)
    line_start = 0
    line_width = 0
    index = 0
    while index < len(char_vals):
        char_val = char_vals[index]
        index += 1
        line_width += get_char_width(rom, char_widths_addr, char_val)
        if char_val in NEWLINE_CHARS or index == len(char_vals):
            if line_width > 0:
                assert line_width <= max_width
                space_val = SPACE_TAG + (max_width - line_width) // 2
                char_vals.insert(line_start, space_val)
                index += 1
                line_width = 0
            line_start = index


def encode_text(
    rom: Rom,
    message_type: MessageType,
    string: str,
    max_width: int = MAX_LINE_WIDTH,
    centered: bool = False,
) -> list[int]:
    char_map = get_char_map(rom.region)
    char_widths_addr = character_widths(rom)
    text: list[int] = []
    line_width = 0
    line_number = 0

    prev_break: int | None = None
    width_since_break = 0
    escaped = False
    markup_tag: list[str] | None = None

    for char in string:
        if not escaped:
            # Check for escaped character
            if char == "\\":
                if markup_tag is not None:
                    raise ValueError(f'Escaped character in markup tag:\n"{string}"')
                escaped = True
                continue
            if markup_tag is None:
                # Check for start of markup tag
                if char == "[":
                    markup_tag = []
                    continue
            else:
                # Check for end of markup tag
                if char == "]":
                    tag_str = "".join(markup_tag)
                    # Check if markup tag with assignable value
                    char_val = parse_value_markup_tag(tag_str)
                    if char_val is None:
                        # Check if normal markup tag
                        char_val = char_map.get(f"[{tag_str}]")
                        if char_val is None:
                            char_val = char_map["?"]
                            # raise ValueError(f"Invalid markup tag '{tag_str}'")
                    if char_val in NEWLINE_CHARS:
                        prev_break = len(text)
                        width_since_break = 0
                        line_width = 0
                        if char_val == NEXT:
                            line_number = 0
                        else:
                            line_number += 1

                    text.append(char_val)
                    markup_tag = None
                else:
                    # Still parsing markup tag
                    markup_tag.append(char)
                continue
        else:
            escaped = False

        try:
            char_val = char_map[char]
        except KeyError:
            char_val = char_map["?"]
        char_width = get_char_width(rom, char_widths_addr, char_val)
        line_width += char_width
        width_since_break += char_width

        if char_val in BREAKING_CHARS:
            prev_break = len(text)
            width_since_break = 0
            if char_val in NEWLINE_CHARS:
                line_width = 0
                line_number += 1

        extra_char = None

        if line_width > max_width:
            if message_type == MessageType.ONE_LINE:
                raise ValueError(f'String does not fit on one line:\n"{string}"')
            if width_since_break > max_width:
                break
                #raise ValueError(f'Word does not fit on one line:\n"{string}"')
            line_width = width_since_break
            line_number += 1
            extra_char = NEWLINE

        if line_number > 1:
            match message_type:
                case MessageType.CONTINUOUS:
                    line_number = 0
                    extra_char = NEXT
                case MessageType.TWO_LINE:
                    # Limited to 2 lines, trim any other characters
                    break

        if extra_char is not None:
            if prev_break is not None:
                if len(text) <= prev_break:
                    text.append(extra_char)
                    continue
                else:
                    text[prev_break] = extra_char
                prev_break = None
            else:
                text.append(extra_char)

        text.append(char_val)

    if markup_tag is not None:
        raise ValueError(f'Unclosed markup tag:\n"{string}"')

    if message_type == MessageType.ONE_LINE and (NEXT in text or NEWLINE in text):
        raise ValueError(f'String cannot have newlines:\n"{string}"')

    if centered:
        center_text(rom, text, max_width)

    if message_type == MessageType.TWO_LINE and NEWLINE not in text:
        # Two line messages MUST have two lines, append NEWLINE if none exists
        text.append(NEWLINE)

    text.append(END)
    return text


def write_seed_hash(rom: Rom, seed_hash: str) -> None:
    char_map = get_char_map(rom.region)
    lang_ptrs = file_screen_text_ptrs(rom)
    for lang in Language:
        # Get address of first text entry
        text_ptrs = rom.read_ptr(lang_ptrs + lang.value * 4)
        addr = rom.read_ptr(text_ptrs)
        # Find newline after "SAMUS DATA"
        try:
            line_len = next(i for i in range(20) if rom.read_16(addr + i * 2) == NEWLINE)
        except StopIteration:
            raise ValueError("Invalid file screen text data")
        pad_left = (line_len - 8) // 2
        pad_right = line_len - 8 - pad_left
        # Overwrite with seed hash
        string = (" " * pad_left) + seed_hash + (" " * pad_right)
        for i, c in enumerate(string):
            rom.write_16(addr + i * 2, char_map[c])
