"""Update wrinkly hints compressed file."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, grabText, writeText, CompTextFiles, writeRawFile
from randomizer.Patching.Patcher import LocalROM
from randomizer.Patching.ASMPatcher import writeItemReferenceFlags
from randomizer.Enums.Settings import WinConditionComplex

MAX_LINES = 3
MAX_LINE_LENGTH = 400
CHAR_KERNING = 0
SPACE_KERNING = 5
DEBUG = False
HINT_CHARACTER_LIMIT = 125
TERMINATING_EFFECTS = False
CHAR_WIDTH = {
    "A": 10,
    "B": 9,
    "C": 9,
    "D": 9,
    "E": 8,
    "F": 8,
    "G": 11,
    "H": 9,
    "I": 4,
    "J": 9,
    "K": 9,
    "L": 8,
    "M": 11,
    "N": 9,
    "O": 10,
    "P": 8,
    "Q": 11,
    "R": 9,
    "S": 10,
    "T": 9,
    "U": 9,
    "V": 9,
    "W": 12,
    "X": 8,
    "Y": 9,
    "Z": 8,
    ".": 5,
    ",": 5,
    "!": 4,
    "?": 7,
    ":": 5,
    ";": 5,
    "'": 5,
    "-": 9,
    "&": 11,
    "1": 6,
    "2": 9,
    "3": 9,
    "4": 10,
    "5": 10,
    "6": 9,
    "7": 9,
    "8": 10,
    "9": 10,
    "0": 10,
    "(": 5,
    ")": 5,
    "%": 12,
}
CONTROL_CHARACTERS = [
    "\x04",
    "\x05",
    "\x06",
    "\x07",
    "\x08",
    "\x09",
    "\x0a",
    "\x0b",
    "\x0c",
    "\x0d",
]


def getActiveEffectStr(active_effects: list[str], ending: bool) -> str:
    """Get the start or end of a string to properly account for the active effect list."""
    if not TERMINATING_EFFECTS:
        return ""
    effects_copy = active_effects[:]
    if ending:
        effects_copy.reverse()  # If ending a string, remove the effects in reverse order to how they were applied
    return "".join(effects_copy)


def splitText(text: str, truncate_split: bool) -> str:
    """Split a text entry into lines."""
    lines = []
    line_index = 0
    line_length = 0
    line_text = ""
    text = text.strip(" ")  # Filter out any trailing whitespaces
    most_recent_word = ""
    word_length = 0
    displayed_characters = 0
    active_effects = []
    if DEBUG:
        print("----------")
        print(text)
    while line_index < MAX_LINES:
        if len(text) == 0:
            if len(most_recent_word) > 0:
                line_text += most_recent_word
                line_text = line_text.strip(" ")
                line_text += getActiveEffectStr(active_effects, True)
                lines.append(line_text)
            break
        elif line_length == 0:
            # Start of a string
            line_text += getActiveEffectStr(active_effects, False)
        if line_length == 0 and DEBUG:
            print("Starting new line")
        char = text[0]
        add_word = False
        width = 0
        if char == " ":
            width = SPACE_KERNING
            add_word = True
        elif char in CONTROL_CHARACTERS:
            width = CHAR_KERNING
            if char in active_effects:
                active_effects.remove(char)
            else:
                active_effects.append(char)
        else:
            char_width = CHAR_WIDTH.get(char, 0)
            if char_width:
                displayed_characters += 1
            width = CHAR_KERNING + char_width
        if displayed_characters > HINT_CHARACTER_LIMIT and len(text) > 1 and truncate_split:
            line_text += most_recent_word
            line_text = line_text.strip(" ")
            if len(line_text) < 3:
                line_text = "..."
            else:
                line_text = line_text[:3].strip(" ") + "..."
            line_text += getActiveEffectStr(active_effects, True)
            lines.append(line_text)
            break
        word_length += width
        line_length += width
        most_recent_word += text[0]
        if add_word:
            line_text += most_recent_word
            if DEBUG:
                print("Parsed new world", most_recent_word, "|", line_text)
            # Reset
            word_length = 0
            most_recent_word = ""
        text = text[1:]
        if line_length > MAX_LINE_LENGTH and truncate_split:
            line_index += 1
            line_length = 0
            if line_index == MAX_LINES:
                line_text = line_text.strip(" ") + "..."
            line_text = line_text.strip(" ")
            line_text += getActiveEffectStr(active_effects, True)
            lines.append(line_text)
            if DEBUG:
                print("Next line: ", line_text, "|", most_recent_word)
            line_text = ""
    base_text = "\x0f".join(lines)
    return f"{base_text}\x00"


def writeFastHints(ROM_COPY: LocalROM, table_index: int, file_index: int, input_text: list, compressed: bool, truncate_split: bool = True, elmer_fudd: bool = False):
    """Write a fast lookup version of text to ROM."""
    bad_chars = ["\x00, \x0f"]
    entries = []
    for textbox in input_text:
        text = ""
        for line in textbox:
            filtered_line = "".join(c for c in line if c not in bad_chars)
            if elmer_fudd:
                filtered_line = filtered_line.replace("r", "w")
                filtered_line = filtered_line.replace("R", "W")
            text += f"{filtered_line} "
        entries.append(splitText(text, truncate_split))
    raw_text = "".join(entries)
    data = raw_text.encode("ascii")
    unc_size = len(data)
    if compressed:
        unc_table = getPointerLocation(TableNames.UncompressedFileSizes, table_index)
        ROM_COPY.seek(unc_table + (file_index * 4))
        ROM_COPY.writeMultipleBytes(unc_size, 4)
    writeRawFile(table_index, file_index, compressed, bytearray(data), ROM_COPY)


def writeWrinklyHints(ROM_COPY: LocalROM, table_index: int, file_index: int, text: list, compressed: bool, elmer_fudd: bool = False):
    """Write the text to ROM."""
    data = [len(text)]
    position = 0
    for textbox in text:
        data.extend([1, 1, len(textbox)])
        for string in textbox:
            str_len = len(string)
            data.extend(
                [
                    (position >> 24) & 0xFF,
                    (position >> 16) & 0xFF,
                    (position >> 8) & 0xFF,
                    position & 0xFF,
                    (str_len >> 8) & 0xFF,
                    str_len & 0xFF,
                    0,
                    0,
                ]
            )
            position += str_len
        data.extend([0, 0, 0, 0])
    data.extend(
        [
            (position >> 8) & 0xFF,
            position & 0xFF,
        ]
    )
    for textbox in text:
        for string in textbox:
            for x in range(len(string)):
                written_string = string[x]
                if elmer_fudd:
                    written_string = written_string.replace("r", "w")
                    written_string = written_string.replace("R", "W")
                data.append(int.from_bytes(written_string.encode("ascii"), "big"))
    unc_size = len(data)
    if compressed:
        unc_table = getPointerLocation(TableNames.UncompressedFileSizes, table_index)
        ROM_COPY.seek(unc_table + (file_index * 4))
        ROM_COPY.writeMultipleBytes(unc_size, 4)
    writeRawFile(table_index, file_index, compressed, bytearray(data), ROM_COPY)


def PushHints(spoiler, ROM_COPY: LocalROM):
    """Update the ROM with all hints."""
    hint_arr = []
    short_hint_arr = []
    for hint_info in spoiler.hintset.hints:
        if hint_info.hint == "":
            hint_info.hint = "error: missing hint - report this error to the discord"
        hint_arr.append([hint_info.hint.upper()])
        if hint_info.short_hint is None:
            hint_info.short_hint = hint_info.hint
        short_hint_arr.append([hint_info.short_hint.upper()])
    elmer_fudd = spoiler.settings.win_condition_item == WinConditionComplex.kill_the_rabbit
    writeWrinklyHints(ROM_COPY, TableNames.Unknown6, CompTextFiles.Wrinkly & 0x3F, hint_arr, True, elmer_fudd)
    writeFastHints(ROM_COPY, TableNames.Unknown6, CompTextFiles.WrinklyShort & 0x3F, short_hint_arr[1:], True, True, elmer_fudd)
    spoiler.hintset.RemoveFTT()  # The FTT needs to be written to the ROM but should not be found in the spoiler log


def PushItemLocations(spoiler, ROM_COPY: LocalROM):
    """Push item hints to ROM."""
    text_arr = []
    flag_arr = []
    for loc in spoiler.location_references:
        text_arr.append([loc.item_name.upper()])
        for subloc in loc.locations:
            text_arr.append([subloc.upper()])
        flag_arr.extend(loc.flags)
    writeFastHints(ROM_COPY, TableNames.Unknown6, CompTextFiles.ItemLocations & 0x3F, text_arr, True, False)
    writeItemReferenceFlags(ROM_COPY, flag_arr)


def replaceIngameText(spoiler, ROM_COPY: LocalROM):
    """Replace text in-game with defined modifications."""
    for file_index in spoiler.text_changes:
        old_text = grabText(ROM_COPY, file_index)
        modification_data = spoiler.text_changes[file_index]
        for mod in modification_data:
            if mod["mode"] == "replace":
                old_textbox = old_text[mod["textbox_index"]]
                new_textbox = []
                for seg in old_textbox:
                    text = []
                    for line in seg["text"]:
                        new_line = line.replace(mod["search"], mod["target"])
                        text.append(new_line)
                    new_textbox.append({"text": text.copy()})
                old_text[mod["textbox_index"]] = new_textbox.copy()
            elif mod["mode"] == "replace_whole":
                # print(mod["target"])
                old_text[mod["textbox_index"]] = ({"text": [mod["target"]]},)
        writeText(ROM_COPY, file_index, old_text)


def PushHelpfulHints(spoiler, ROM_COPY: LocalROM):
    """Push the flags to ROM which control the dim_solved_hints setting."""
    for index, flag in enumerate(spoiler.tied_hint_flags.values()):
        ROM_COPY.seek(0x1FFE000 + (2 * index))
        ROM_COPY.writeMultipleBytes(flag, 2)


def PushHintTiedRegions(spoiler, ROM_COPY: LocalROM):
    """Push the flags to ROM which control the dim_solved_hints setting."""
    for index, flag in enumerate(spoiler.tied_hint_regions):
        ROM_COPY.seek(0x1FFE080 + (2 * index))
        ROM_COPY.writeMultipleBytes(flag, 2)
