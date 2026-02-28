"""Hints for DK64R Archipelago."""

# from worlds.dk64 import DK64World
from randomizer.CompileHints import HintSet, replaceKongNameWithKrusha
from randomizer.Enums.Maps import Maps
from randomizer.Enums.Kongs import Kongs
from randomizer.Enums.Levels import Levels
from randomizer.Enums.Transitions import Transitions
from randomizer.Enums.Types import BarrierItems
from randomizer.Lists.ShufflableExit import ShufflableExits
from randomizer.Lists.WrinklyHints import UpdateHint

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


def hint_location_to_kong_level(hint_location):
    """Convert a hint location to a (kong, level) tuple based on the wrinkly door system."""
    if hint_location is None:
        return None, None

    try:
        kong_index = hint_location.kong
        level_index = hint_location.level
        if not isinstance(kong_index, int):
            kong_index = getattr(kong_index, "value", kong_index)
        if not isinstance(level_index, int):
            level_index = getattr(level_index, "value", level_index)
        if not isinstance(kong_index, int):
            kong_names = {
                Kongs.donkey: 0,
                Kongs.diddy: 1,
                Kongs.lanky: 2,
                Kongs.tiny: 3,
                Kongs.chunky: 4,
            }
            kong_index = kong_names.get(hint_location.kong, None)

        # Map levels to 0-6 range
        if not isinstance(level_index, int) or level_index > 6:
            level_names = {
                Levels.JungleJapes: 0,
                Levels.AngryAztec: 1,
                Levels.FranticFactory: 2,
                Levels.GloomyGalleon: 3,
                Levels.FungiForest: 4,
                Levels.CrystalCaves: 5,
                Levels.CreepyCastle: 6,
            }
            level_index = level_names.get(hint_location.level, None)
        if kong_index is not None and level_index is not None and 0 <= kong_index <= 4 and 0 <= level_index <= 6:
            return kong_index, level_index

    except Exception:
        pass

    return None, None


def convert_hint_door_name_to_full_name(hint_door_name):
    """Convert a short hint door name to the full location name used in ap_check_ids."""
    if not hint_door_name:
        return None
    # Map short kong names to full names
    kong_name_mapping = {"DK": "Donkey", "Donkey": "Donkey", "Diddy": "Diddy", "Lanky": "Lanky", "Tiny": "Tiny", "Chunky": "Chunky"}

    # Map hint system level names to client expected level names
    level_name_mapping = {"Fungi": "Forest"}

    parts = hint_door_name.split()
    if len(parts) >= 2:
        level_name = parts[0]  # e.g., "Japes", "Aztec", "Castle"
        kong_name = parts[1]  # e.g., "DK", "Chunky", "Tiny"

        # Convert short kong name to full name
        full_kong_name = kong_name_mapping.get(kong_name, kong_name)

        # Convert Forest name
        level_name = level_name_mapping.get(level_name, level_name)

        # Construct the full hint door name
        full_name = f"{level_name} {full_kong_name} Hint Door"
        return full_name

    return None


def CompileArchipelagoHints(world, hint_data: list):
    """Insert Archipelago hints."""
    replaceKongNameWithKrusha(world.spoiler)
    hintset = HintSet()
    hint_location_mapping = {}
    if world.options.hint_style == 1:
        woth_count = 0  # disabled
        major_count = 15
        deep_count = 35  # overly high to cover the bases
    if world.options.hint_style == 2:
        woth_count = 10
        major_count = 7
        deep_count = 8

    # Variables
    hints_remaining = 35  # Keep count how many hints we placed
    compiled_hints = []  # The hints we compile
    hint_locations_used = []  # Track which hint locations are used for mapping
    woth_duplicates = []
    kong_locations = hint_data["kong"]
    key_locations = hint_data["key"]
    woth_locations = hint_data["woth"]
    major_locations = hint_data["major"]
    deep_locations = hint_data["deep"]
    already_hinted = kong_locations + key_locations
    hint_location_pairs = []
    krool_hint = parseKRoolHint(world)
    compiled_hints.append(krool_hint)
    hint_location_pairs.append((krool_hint, None))  # K. Rool hints don't have a specific location
    hints_remaining -= 1

    # Isles to Helm transition hint (only if loading zone rando is enabled and Helm is shuffled)
    if world.options.loading_zone_rando != 0 and world.options.shuffle_helm_level_order:
        isles_to_helm_hint = parseIslesToHelmHint(world)
        compiled_hints.append(isles_to_helm_hint)
        hint_location_pairs.append((isles_to_helm_hint, None))  # Transition hints don't have a specific location
        hints_remaining -= 1

    # Helm Door hints (only if one or both doors were set to random)
    if world.options.crown_door_item.value in [13, 2, 14] or world.options.coin_door_item.value in [13, 2, 14]:
        helm_door_hints = parseHelmDoorHint(world)
        for helm_door_hint in helm_door_hints:
            compiled_hints.append(helm_door_hint)
            hint_location_pairs.append((helm_door_hint, None))  # Helm door hints don't have a specific location
            hints_remaining -= 1

    # Kong hints
    for kong_loc in kong_locations:
        kong_hint = parseKongHint(world, kong_loc)
        compiled_hints.append(kong_hint)
        hint_location_pairs.append((kong_hint, kong_loc))
        hints_remaining -= 1

    # Key hints
    for key_loc in key_locations:
        key_hint = parseKeyHint(world, key_loc)
        compiled_hints.append(key_hint)
        hint_location_pairs.append((key_hint, key_loc))
        hints_remaining -= 1

    # Woth hints
    woth_locations = [x for x in woth_locations if x not in already_hinted]
    woth_count = min(min(len(woth_locations), woth_count), hints_remaining)
    woth_locations = world.spoiler.settings.random.sample(woth_locations, woth_count)
    for woth_loc in woth_locations:
        already_hinted.append(woth_loc)
        this_hint = parseWothHint(world, woth_loc)
        compiled_hints.append(this_hint)
        hint_location_pairs.append((this_hint, None))
        woth_duplicates.append(this_hint)
        hints_remaining -= 1

    # Major item hints
    major_locations = [x for x in major_locations if x not in already_hinted]
    major_count = min(min(len(major_locations), major_count), hints_remaining)
    major_locations = world.spoiler.settings.random.sample(major_locations, major_count)
    for major_loc in major_locations:
        major_hint = parseMajorItemHint(world, major_loc)
        compiled_hints.append(major_hint)
        hint_location_pairs.append((major_hint, major_loc))
        hints_remaining -= 1

    # Deep check hints
    deep_count = min(min(len(deep_locations), deep_count), hints_remaining)
    deep_locations = world.spoiler.settings.random.sample(deep_locations, deep_count)
    for deep_loc in deep_locations:
        deep_hint = parseDeepHint(world, deep_loc)
        compiled_hints.append(deep_hint)
        hint_location_pairs.append((deep_hint, deep_loc))
        hints_remaining -= 1

    # Woth hint duplicates as needed
    while hints_remaining > 0 and len(woth_duplicates) > 0:
        duplicate_hint = woth_duplicates.pop()
        compiled_hints.append(duplicate_hint)
        hint_location_pairs.append((duplicate_hint, None))  # Duplicates don't need location mapping
        hints_remaining -= 1

    # Sanity check that 35 hints were placed
    if hints_remaining > 0:
        # This part of the code should not be reached.
        while hints_remaining > 0:
            filler_hint = "no hint, sorry...".upper()
            compiled_hints.append(filler_hint)
            hint_location_pairs.append((filler_hint, None))  # Filler hints don't have locations
            hints_remaining -= 1

    # Place hints and create mapping
    for i, (hint, location_obj) in enumerate(hint_location_pairs):
        hint_location = hintset.getRandomHintLocation(random=world.spoiler.settings.random)

        if hint_location is None:
            continue

        UpdateHint(hint_location, hint)
        hint_locations_used.append(hint_location)

        # Create mapping if we have a corresponding location for this hint
        if location_obj is not None:
            # Convert hint_location to a (kong, level) tuple
            kong, level = hint_location_to_kong_level(hint_location)

            if kong is not None and level is not None:
                # We need to find the hint door location ID from the hint door name
                hint_door_name = getattr(hint_location, "name", None)

                # Convert short hint door name to full name
                full_hint_door_name = convert_hint_door_name_to_full_name(hint_door_name)

                # Import the hint door location mappings
                try:
                    from archipelago.client.ap_check_ids import check_names_to_id

                    hint_door_location_id = check_names_to_id.get(full_hint_door_name, None)

                    if hint_door_location_id:
                        hint_location_mapping[f"{kong},{level}"] = hint_door_location_id
                        # Use the hint door location ID as the key
                        target_location_id = location_obj.address if hasattr(location_obj, "address") else location_obj.id
                        world.dynamic_hints[hint_door_location_id] = {"should_add_hint": True, "location_id": target_location_id, "location_player_id": location_obj.player}
                except ImportError:
                    # Fallback if import fails - hints will not work but generation can continue
                    pass

    world.spoiler.hintset = hintset

    # Store the hint location mapping in the world for use in slot_data
    world.hint_location_mapping = hint_location_mapping


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
        text = f"\x05{world.multiworld.get_player_name(location.player)}'s\x05 \x0d{location.name[:80]}\x0d is on the \x04Way of the Hoard\x04.".upper()
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


def parseIslesToHelmHint(world):
    """Write a hint for finding the transition that leads to Hideout Helm."""
    text = ""
    # Check if entrance randomization is enabled
    if hasattr(world.spoiler, "shuffled_exit_data") and world.spoiler.shuffled_exit_data:
        # Find which transition leads to Hideout Helm
        source_transition = None
        for transition, shuffled_back in world.spoiler.shuffled_exit_data.items():
            # Check if this transition's destination is Hideout Helm
            if shuffled_back.reverse == Transitions.HelmToIsles:
                source_transition = transition
                break

        if source_transition and source_transition in ShufflableExits:
            pathToHint = source_transition
            # Don't hint entrances from connector rooms, follow the reverse pathway back until finding a non-connector
            while ShufflableExits[pathToHint].category is None:
                originPaths = [x for x, back in world.spoiler.shuffled_exit_data.items() if back.reverse == pathToHint]
                # In a few cases, there is no reverse loading zone. In this case we must keep the original path to hint
                if len(originPaths) == 0:
                    break
                pathToHint = originPaths[0]

            source_name = ShufflableExits[pathToHint].name
            text = f"Looking for \x04Hideout Helm\x04? Try going from \x08{source_name}\x08.".upper()

    for letter in text:
        if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
            text = text.replace(letter, " ")
    return text


def parseHelmDoorHint(world):
    """Write hints for the Helm door requirements if they're randomized."""
    # Map BarrierItems to display names (singular)
    item_names_singular = {
        BarrierItems.GoldenBanana: "Golden Banana",
        BarrierItems.Blueprint: "Blueprint",
        BarrierItems.CompanyCoin: "Special Coin",
        BarrierItems.Key: "Key",
        BarrierItems.Medal: "Medal",
        BarrierItems.Crown: "Crown",
        BarrierItems.Fairy: "Fairy",
        BarrierItems.RainbowCoin: "Rainbow Coin",
        BarrierItems.Bean: "Bean",
        BarrierItems.Pearl: "Pearl",
    }

    crown_door_item = world.spoiler.settings.crown_door_item
    crown_door_count = world.spoiler.settings.crown_door_item_count
    coin_door_item = world.spoiler.settings.coin_door_item
    coin_door_count = world.spoiler.settings.coin_door_item_count

    crown_door_randomized = world.options.crown_door_item.value in [13, 2, 14]  # easy, medium, hard random
    coin_door_randomized = world.options.coin_door_item.value in [13, 2, 14]

    hints = []

    if crown_door_randomized:
        crown_name = item_names_singular.get(crown_door_item, "item")
        if crown_door_count > 1:
            if crown_door_item == BarrierItems.Fairy:
                crown_name = "Fairies"
            else:
                crown_name = crown_name + "s"
        text = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{crown_door_count} {crown_name}\x04.".upper()
        for letter in text:
            if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
                text = text.replace(letter, " ")
        hints.append(text)

    if coin_door_randomized:
        coin_name = item_names_singular.get(coin_door_item, "item")
        if coin_door_count > 1:
            if coin_door_item == BarrierItems.Fairy:
                coin_name = "Fairies"
            else:
                coin_name = coin_name + "s"
        coin_text = f"There lies a \x05gate in Hideout Helm\x05 that requires \x04{coin_door_count} {coin_name}\x04.".upper()
        for letter in coin_text:
            if letter not in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.,!?:;'S-()% \x04\x05\x06\x07\x08\x09\x0a\x0b\x0c\x0d":
                coin_text = coin_text.replace(letter, " ")
        hints.append(coin_text)

    return hints
