"""Update wrinkly hints compressed file."""

from randomizer.Enums.Kongs import Kongs
from randomizer.Lists.WrinklyHints import HintLocation, hints
from randomizer.Patching.Library.Assets import getPointerLocation, TableNames, grabText, writeText
from randomizer.Patching.Patcher import LocalROM


def writeWrinklyHints(ROM_COPY: LocalROM, file_start_offset, text):
    """Write the text to ROM."""
    ROM_COPY.seek(file_start_offset)
    ROM_COPY.writeMultipleBytes(len(text), 1)
    position = 0
    offset = 1
    for textbox in text:
        ROM_COPY.seek(file_start_offset + offset)
        ROM_COPY.writeMultipleBytes(1, 1)
        ROM_COPY.seek(file_start_offset + offset + 1)
        ROM_COPY.writeMultipleBytes(1, 1)
        ROM_COPY.seek(file_start_offset + offset + 2)
        ROM_COPY.writeMultipleBytes(len(textbox), 1)
        offset += 3
        for string in textbox:
            ROM_COPY.seek(file_start_offset + offset)
            ROM_COPY.writeMultipleBytes(position, 4)
            ROM_COPY.seek(file_start_offset + offset + 4)
            ROM_COPY.writeMultipleBytes(len(string), 2)
            ROM_COPY.seek(file_start_offset + offset + 6)
            ROM_COPY.writeMultipleBytes(0, 2)
            offset += 8
            position += len(string)
        ROM_COPY.seek(file_start_offset + offset)
        ROM_COPY.writeMultipleBytes(0, 4)
        offset += 4
    ROM_COPY.seek(file_start_offset + offset)
    ROM_COPY.writeMultipleBytes(position, 2)
    offset += 2
    for textbox in text:
        for string in textbox:
            for x in range(len(string)):
                ROM_COPY.seek(file_start_offset + offset + x)
                ROM_COPY.writeMultipleBytes(int.from_bytes(string[x].encode("ascii"), "big"), 1)
            offset += len(string)


def UpdateHint(WrinklyHint: HintLocation, message: str):
    """Update the wrinkly hint with the new string.

    Args:
        WrinklyHint (Hint): Wrinkly hint object.
        message (str): Hint message to write.
    """
    # Seek to the wrinkly data
    if len(message) <= 914:
        # We're safely below the character limit
        WrinklyHint.hint = message
        return True
    else:
        raise Exception("Hint message is longer than allowed.")
    return False


def updateRandomHint(random, message: str, kongs_req=[], keywords=[], levels=[]):
    """Update a random hint with the string specifed.

    Args:
        message (str): Hint message to write.
    """
    hint_pool = []
    for x in range(len(hints)):
        if hints[x].hint == "" and hints[x].kong in kongs_req and hints[x].level in levels:
            is_banned = False
            for banned in hints[x].banned_keywords:
                if banned in keywords:
                    is_banned = True
            if not is_banned:
                hint_pool.append(x)
    if len(hint_pool) > 0:
        selected = random.choice(hint_pool)
        return UpdateHint(hints[selected], message)
    return False


def PushHints(spoiler, ROM_COPY: LocalROM):
    """Update the ROM with all hints."""
    hint_arr = []
    short_hint_arr = []
    for replacement_hint in spoiler.hint_list.values():
        if replacement_hint == "":
            replacement_hint = "error: missing hint - report this error to the discord"
        hint_arr.append([replacement_hint.upper()])
    for short_hint in spoiler.short_hint_list.values():
        if short_hint == "":
            short_hint = "error: missing hint - report this error to the discord"
        short_hint_arr.append([short_hint.upper()])
    writeWrinklyHints(ROM_COPY, getPointerLocation(TableNames.Text, 41), hint_arr)
    writeWrinklyHints(ROM_COPY, getPointerLocation(TableNames.Text, 45), short_hint_arr)
    spoiler.hint_list.pop("First Time Talk")  # The FTT needs to be written to the ROM but should not be found in the spoiler log


def wipeHints():
    """Wipe the hint block."""
    for x in range(len(hints)):
        if hints[x].kong != Kongs.any:
            hints[x].hint = ""


def PushItemLocations(spoiler, ROM_COPY: LocalROM):
    """Push item hints to ROM."""
    text_arr = []
    for loc in spoiler.location_references:
        text_arr.append([loc.item_name.upper()])
        for subloc in loc.locations:
            text_arr.append([subloc.upper()])
    writeWrinklyHints(ROM_COPY, getPointerLocation(TableNames.Text, 44), text_arr)


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
