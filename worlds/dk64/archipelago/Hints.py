"""Hints for DK64R Archipelago."""

# from worlds.dk64 import DK64World
from randomizer.CompileHints import UpdateSpoilerHintList, getRandomHintLocation, replaceKongNameWithKrusha
from randomizer.Enums.Maps import Maps
from randomizer.Lists.WrinklyHints import ClearHintMessages
from randomizer.Patching.UpdateHints import UpdateHint

boss_names = {
    Maps.JapesBoss: "Army Dillo 1",
    Maps.AztecBoss: "Dogadon 1",
    Maps.FactoryBoss: "Mad Jack",
    Maps.GalleonBoss: "Pufftoss",
    Maps.FungiBoss: "Dogadon 2",
    Maps.CavesBoss: "Army Dillo 2",
    Maps.CastleBoss: "King Kut Out",
    Maps.KroolDonkeyPhase: "DK Phase",
    Maps.KroolDiddyPhase: "Diddy Phase",
    Maps.KroolLankyPhase: "Lanky Phase",
    Maps.KroolTinyPhase: "Tiny Phase",
    Maps.KroolChunkyPhase: "Chunky Phase",
}
boss_colors = {
    Maps.JapesBoss: "\x08",
    Maps.AztecBoss: "\x04",
    Maps.FactoryBoss: "\x0c",
    Maps.GalleonBoss: "\x06",
    Maps.FungiBoss: "\x07",
    Maps.CavesBoss: "\x0a",
    Maps.CastleBoss: "\x09",
    Maps.KroolDonkeyPhase: "\x04",
    Maps.KroolDiddyPhase: "\x05",
    Maps.KroolLankyPhase: "\x06",
    Maps.KroolTinyPhase: "\x07",
    Maps.KroolChunkyPhase: "\x08",
}


def CompileArchipelagoHints(world, hint_data: list):
    """Insert Archipelago hints."""
    replaceKongNameWithKrusha(world.spoiler)
    ClearHintMessages()
    # All input lists are in the form of [loc]
    # Settings
    woth_count = 10
    major_count = 7
    deep_count = 8

    # Variables
    hints_remaining = 35  # Keep count how many hints we placed
    hints = []  # The hints we compile
    woth_duplicates = []
    kong_locations = hint_data["kong"]
    key_locations = hint_data["key"]
    woth_locations = hint_data["woth"]
    major_locations = hint_data["major"]
    deep_locations = hint_data["deep"]
    already_hinted = kong_locations + key_locations

    # Creating the hints

    # K. Rool order hint
    hints.append(parseKRoolHint(world))
    hints_remaining -= 1

    # Kong hints
    for kong_loc in kong_locations:
        hints.append(parseKongHint(world, kong_loc))
        hints_remaining -= 1

    # Key hints
    for key_loc in key_locations:
        hints.append(parseKeyHint(world, key_loc))
        hints_remaining -= 1

    # Woth hints
    woth_locations = [x for x in woth_locations if x not in already_hinted]
    woth_count = min(min(len(woth_locations), woth_count), hints_remaining)
    woth_locations = world.spoiler.settings.random.sample(woth_locations, woth_count)
    for woth_loc in woth_locations:
        already_hinted.append(woth_loc)
        this_hint = parseWothHint(world, woth_loc)
        hints.append(this_hint)
        woth_duplicates.append(this_hint)
        hints_remaining -= 1

    # Major item hints
    major_locations = [x for x in major_locations if x not in already_hinted]
    major_count = min(min(len(major_locations), major_count), hints_remaining)
    major_locations = world.spoiler.settings.random.sample(major_locations, major_count)
    for major_loc in major_locations:
        hints.append(parseMajorItemHint(world, major_loc))
        hints_remaining -= 1

    # Deep check hints
    deep_count = min(min(len(deep_locations), deep_count), hints_remaining)
    deep_locations = world.spoiler.settings.random.sample(deep_locations, deep_count)
    for deep_loc in deep_locations:
        hints.append(parseDeepHint(world, deep_loc))
        hints_remaining -= 1

    # Woth hint duplicates as needed
    while hints_remaining > 0 and len(woth_duplicates) > 0:
        hints.append(woth_duplicates.pop())
        hints_remaining -= 1

    # Sanity check that 35 hints were placed
    if hints_remaining > 0:
        # This part of the code should not be reached.
        print("Not enough hints. Please wait. stage_generate_output might be crashing.")
        while hints_remaining > 0:
            hints.append("no hint, sorry...".upper())
            hints_remaining -= 1

    for hint in hints:
        hint_location = getRandomHintLocation(random=world.spoiler.settings.random)
        UpdateHint(hint_location, hint)
    UpdateSpoilerHintList(world.spoiler)


def parseKeyHint(world, location):
    """Write a key hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"\x07{location.item.name[:40]}\x07 is hidden away for \x05{world.multiworld.get_player_name(location.player)}\x05 to find in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"\x07{location.item.name[:40]}\x07 is hidden away in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseKongHint(world, location):
    """Write a kong hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"\x07{location.item.name[:40]}\x07 is to be found by \x05{world.multiworld.get_player_name(location.player)}\x05 in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"\x07{location.item.name[:40]}\x07 is held by your local villain in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseWothHint(world, location):
    """Write a woth item hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"\x05{world.multiworld.get_player_name(location.player)}\x05 \x0d{location.name[:80]}\x0d is on the \x04Way of the Hoard\x04.".upper()
    else:
        text = f"Your \x0d{location.name}\x0d is on the \x04Way of the Hoard\x04.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseMajorItemHint(world, location):
    """Write a major item hint for the given location."""
    text = ""
    if location.player != world.player:
        text = f"Looking for \x07{location.item.name[:40]}\x07? Ask \x05{world.multiworld.get_player_name(location.player)}\x05 to try looking in \x0d{location.name[:80]}\x0d.".upper()
    else:
        text = f"Looking for \x07{location.item.name[:40]}\x07? Try looking in \x0d{location.name}\x0d.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseDeepHint(world, location):
    """Write a deep item hint for the given location."""
    text = ""
    if location.item.player != world.player:
        text = f"\x0d{location.name}\x0d has \x05{world.multiworld.get_player_name(location.item.player)}'s\x05 \x07{location.item.name[:40]}\x07.".upper()
    else:
        text = f"\x0d{location.name}\x0d has your \x07{location.item.name}\x07".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseKRoolHint(world):
    """Write the K. Rool order hint for the given location."""
    text = ""
    kong_krool_order = [boss_colors[map_id] + boss_names[map_id] + boss_colors[map_id] for map_id in world.spoiler.settings.krool_order]
    kong_krool_text = ", then ".join(kong_krool_order)
    text = f"\x08The final battle\x08 will be against {kong_krool_text}.".upper()
    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text
