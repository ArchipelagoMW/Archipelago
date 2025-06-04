import os
import random
from typing import List
import Utils
from settings import get_settings
from . import RomData
from .Util import *
from .z80asm.Assembler import Z80Assembler
from .Constants import *
from ..data.Constants import *
from .. import LOCATIONS_DATA, OracleOfSeasonsOldMenShuffle, OracleOfSeasonsGoal, OracleOfSeasonsAnimalCompanion, \
    OracleOfSeasonsMasterKeys, OracleOfSeasonsFoolsOre, OracleOfSeasonsShowDungeonsWithEssence
from pathlib import Path


def get_asm_files(patch_data):
    asm_files = ASM_FILES.copy()
    if patch_data["options"]["quick_flute"]:
        asm_files.append("asm/conditional/quick_flute.yaml")
    if patch_data["options"]["shuffle_old_men"] == OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
        asm_files.append("asm/conditional/old_men_as_locations.yaml")
    if patch_data["options"]["remove_d0_alt_entrance"]:
        asm_files.append("asm/conditional/remove_d0_alt_entrance.yaml")
    if patch_data["options"]["remove_d2_alt_entrance"]:
        asm_files.append("asm/conditional/remove_d2_alt_entrance.yaml")
    if patch_data["options"]["goal"] == OracleOfSeasonsGoal.option_beat_ganon:
        asm_files.append("asm/conditional/ganon_goal.yaml")
    if patch_data["options"]["rosa_quick_unlock"]:
        asm_files.append("asm/conditional/instant_rosa.yaml")
    if get_settings()["tloz_oos_options"]["remove_music"]:
        asm_files.append("asm/conditional/mute_music.yaml")
    if patch_data["options"]["secret_locations"]:
        asm_files.append("asm/conditional/secret_locations.yaml")
    return asm_files


def write_chest_contents(rom: RomData, patch_data):
    """
    Chest locations are packed inside several big tables in the ROM, unlike other more specific locations.
    This puts the item described in the patch data inside each chest in the game.
    """
    for location_name, location_data in LOCATIONS_DATA.items():
        if location_data.get('collect', COLLECT_TOUCH) != COLLECT_CHEST and not location_data.get('is_chest', False):
            continue
        chest_addr = rom.get_chest_addr(location_data['room'])
        item = patch_data["locations"][location_name]
        item_id, item_subid = get_item_id_and_subid(item)
        rom.write_byte(chest_addr, item_id)
        rom.write_byte(chest_addr + 1, item_subid)


def define_samasa_combination(assembler: Z80Assembler, patch_data):
    samasa_combination = [int(number) for number in patch_data["samasa_gate_sequence"].split(" ")]

    # 1) Define the combination itself and its length for the gate check
    assembler.add_floating_chunk("samasaCombination", samasa_combination)
    assembler.define_byte("samasaCombinationLengthMinusOne", len(samasa_combination) - 1)

    # 2) Build a cutscene for the Piratian to show the new sequence
    cutscene = [MOVE_UP, 0x15]
    # Add a fake last press on button 1 to make the pirate go back to its original position
    sequence = samasa_combination + [1]
    current_position = 1
    for i, button_to_press in enumerate(sequence):
        # If current button is at a different position than the current one,
        # make the pirate move
        if button_to_press != current_position:
            if button_to_press < current_position:
                distance_to_move = 0x8 * (current_position - button_to_press) + 1
                cutscene.extend([MOVE_LEFT, distance_to_move])
            else:
                distance_to_move = 0x8 * (button_to_press - current_position) + 1
                cutscene.extend([MOVE_RIGHT, distance_to_move])
            current_position = button_to_press

        # Close the cupboard to mimic a button press on the gate by calling
        # the "closeOpenCupboard" subscript. Don't do it if it's the last movement
        # (which was only added to make the pirate go back to its initial position)
        if i < len(sequence) - 1:
            cutscene.extend([CALL_SCRIPT, 0x59, 0x5e])

    # Add some termination to the script
    cutscene.extend([
        MOVE_DOWN, 0x15,
        WRITE_OBJECT_BYTE, 0x7c, 0x00,
        DELAY_6,
        SHOW_TEXT_LOW_INDEX, 0x0d,
        ENABLE_ALL_OBJECTS,
        0x5e, 0x4b  # jump back to script start
    ])

    if len(cutscene) > 0xFE:
        raise Exception("Samasa gate sequence is too long")
    assembler.add_floating_chunk("showSamasaCutscene", cutscene)


def define_compass_rooms_table(assembler: Z80Assembler, patch_data):
    table = []
    for location_name, item in patch_data["locations"].items():
        item_id, item_subid = get_item_id_and_subid(item)
        dungeon = 0xff
        if item_id == 0x30:  # Small Key or Master Key
            dungeon = item_subid
        elif item_id == 0x31:  # Boss Key
            dungeon = item_subid + 1

        if dungeon != 0xff:
            location_data = LOCATIONS_DATA[location_name]
            rooms = location_data["room"]
            if not isinstance(rooms, list):
                rooms = [rooms]
            for room in rooms:
                room_id = room & 0xff
                group_id = room >> 8
                table.extend([group_id, room_id, dungeon])
    table.append(0xff)  # End of table
    assembler.add_floating_chunk("compassRoomsTable", table)


def define_collect_properties_table(assembler: Z80Assembler, patch_data):
    """
    Defines a table of (group, room, collect mode) entries for randomized items
    to determine how they spawn, how they are grabbed and whether they set
    a room flag when obtained.
    """
    table = []
    for location_name, item in patch_data["locations"].items():
        location_data = LOCATIONS_DATA[location_name]
        if "collect" not in location_data:
            continue
        mode = location_data["collect"]

        # Use no pickup animation for falling small keys
        item_id, _ = get_item_id_and_subid(item)
        if mode == COLLECT_DROP and item_id == 0x30:
            mode &= 0xf8  # Set grab mode to TREASURE_GRAB_INSTANT

        rooms = location_data["room"]
        if not isinstance(rooms, list):
            rooms = [rooms]
        for room in rooms:
            room_id = room & 0xff
            group_id = room >> 8
            table.extend([group_id, room_id, mode])

    # Specific case for D6 fake rupee
    table.extend([0x04, 0xc5, TREASURE_SPAWN_POOF | TREASURE_GRAB_INSTANT | TREASURE_SET_ITEM_ROOM_FLAG])
    # Maku Tree gate opening cutscene
    table.extend([0x00, 0xd9, TREASURE_SPAWN_INSTANT | TREASURE_GRAB_SPIN_SLASH])

    table.append(0xff)
    assembler.add_floating_chunk("collectPropertiesTable", table)


def define_additional_tile_replacements(assembler: Z80Assembler, patch_data):
    """
    Define a list of entries following the format of `tileReplacementsTable` (see ASM for more info) which end up
    being tile replacements on various rooms in the game.
    """
    table = []
    # Reveal hidden subrosia digging spots if required
    if get_settings()["tloz_oos_options"]["reveal_hidden_subrosia_digging_spots"]:
        table.extend([
            0x01, 0x06, 0x00, 0x18, 0x2f,  # Bath digging spot
            0x01, 0x57, 0x00, 0x38, 0x2f,  # Market portal digging spot
            0x01, 0x47, 0x00, 0x33, 0x2f,  # Hard-working Subrosian digging spot
            0x01, 0x3a, 0x00, 0x46, 0x2f,  # Temple of Seasons digging spot
            0x01, 0x07, 0x00, 0x13, 0x2f,  # Northern volcanoes digging spot
            0x01, 0x20, 0x00, 0x68, 0x2f,  # D8 portal digging spot
            0x01, 0x42, 0x00, 0x14, 0x2f   # Western volcanoes digging spot
        ])
    # If D0 alternate entrance is removed, put stairs inside D0 to make chest reachable without the alternate entrance
    if patch_data["options"]["remove_d0_alt_entrance"] > 0:
        table.extend([0x04, 0x05, 0x00, 0x5a, 0x53])
    # Remove Gasha spots when harvested once if deterministic Gasha locations are enabled
    if patch_data["options"]["deterministic_gasha_locations"] > 0:
        table.extend([
            0x00, 0xa6, 0x20, 0x54, 0x04,  # North Horon: Gasha Spot Above Impa
            0x00, 0xc8, 0x20, 0x67, 0x04,  # Horon Village: Gasha Spot Near Mayor's House
            0x00, 0xac, 0x20, 0x27, 0x04,  # Eastern Suburbs: Gasha Spot
            0x00, 0x95, 0x20, 0x32, 0x04,  # Holodrum Plain: Gasha Spot Near Mrs. Ruul's House
            0x00, 0x75, 0x20, 0x34, 0x04,  # Holodrum Plain: Gasha Spot on Island Above D1
            0x00, 0x80, 0x20, 0x53, 0x04,  # Spool Swamp: Gasha Spot Near Floodgate Keyhole
            0x00, 0xc0, 0x20, 0x61, 0x04,  # Spool Swamp: Gasha Spot Near Portal
            0x00, 0x3f, 0x20, 0x44, 0x04,  # Sunken City: Gasha Spot
            0x00, 0x1f, 0x20, 0x21, 0x12,  # Mt. Cucco: Gasha Spot
            0x00, 0x38, 0x20, 0x25, 0x04,  # Goron Mountain: Gasha Spot Left of Entrance
            0x00, 0x3b, 0x20, 0x53, 0x12,  # Goron Mountain: Gasha Spot Right of Entrance
            0x00, 0x89, 0x20, 0x24, 0x04,  # Eyeglass Lake: Gasha Spot Near D5
            0x00, 0x22, 0x20, 0x45, 0x04,  # Tarm Ruins: Gasha Spot
            0x00, 0xf0, 0x20, 0x22, 0x12,  # Western Coast: Gasha Spot South of Graveyard
            0x00, 0xef, 0x20, 0x66, 0xaf,  # Samasa Desert: Gasha Spot
            0x00, 0x44, 0x20, 0x44, 0x04,  # Path to Onox Castle: Gasha Spot
        ])
    assembler.add_floating_chunk("additionalTileReplacements", table)


def define_location_constants(assembler: Z80Assembler, patch_data):
    # If "Enforce potion in shop" is enabled, put a Potion in a specific location in Horon Shop that was
    # disabled at generation time to prevent trackers from tracking it
    if patch_data["options"]["enforce_potion_in_shop"]:
        patch_data["locations"]["Horon Village: Shop #3"] = {"item": "Potion"}
    # If golden ore spots are not shuffled, they are still reachable nonetheless, so we need to enforce their
    # vanilla item for systems to work
    if not patch_data["options"]["shuffle_golden_ore_spots"]:
        for location_name in SUBROSIA_HIDDEN_DIGGING_SPOTS_LOCATIONS:
            patch_data["locations"][location_name] = {"item": "Ore Chunks (50)"}

    # Define shop prices as constants
    for symbolic_name, price in patch_data["shop_prices"].items():
        assembler.define_byte(f"shopPrices.{symbolic_name}", RUPEE_VALUES[price])

    for location_name, location_data in LOCATIONS_DATA.items():
        if "symbolic_name" not in location_data:
            continue

        symbolic_name = location_data["symbolic_name"]
        if location_name in patch_data["locations"]:
            item = patch_data["locations"][location_name]
        else:
            # Put a fake item for disabled locations, since they are unreachable anwyway
            item = {"item": "Friendship Ring"}

        item_id, item_subid = get_item_id_and_subid(item)
        assembler.define_byte(f"locations.{symbolic_name}.id", item_id)
        assembler.define_byte(f"locations.{symbolic_name}.subid", item_subid)
        assembler.define_word(f"locations.{symbolic_name}", (item_id << 8) + item_subid)

    # Process deterministic Gasha Nut locations to define a table
    deterministic_gasha_table = []
    for i in range(int(patch_data["options"]["deterministic_gasha_locations"])):
        item = patch_data["locations"][f"Gasha Nut #{i+1}"]
        item_id, item_subid = get_item_id_and_subid(item)
        deterministic_gasha_table.extend([item_id, item_subid])
    assembler.add_floating_chunk("deterministicGashaLootTable", deterministic_gasha_table)


def define_option_constants(assembler: Z80Assembler, patch_data):
    options = patch_data["options"]

    assembler.define_byte("option.startingGroup", 0x00)
    assembler.define_byte("option.startingRoom", 0xb6)
    assembler.define_byte("option.startingPosY", 0x58)
    assembler.define_byte("option.startingPosX", 0x58)
    assembler.define_byte("option.startingPos", 0x55)
    assembler.define_byte("option.startingSeason", patch_data["default_seasons"]["EYEGLASS_LAKE"])
    assembler.define_byte("option.startingMapsCompasses", patch_data["options"]["starting_maps_compasses"])

    assembler.define_byte("option.animalCompanion", 0x0b + patch_data["options"]["animal_companion"])
    assembler.define_byte("option.defaultSeedType", 0x20 + patch_data["options"]["default_seed"])
    assembler.define_byte("option.receivedDamageModifier", options["combat_difficulty"])
    assembler.define_byte("option.openAdvanceShop", options["advance_shop"])
    assembler.define_byte("option.warpToStart", True)

    assembler.define_byte("option.requiredEssences", options["required_essences"])
    assembler.define_byte("option.goldenBeastsRequirement", options["golden_beasts_requirement"])
    assembler.define_byte("option.treehouseOldManRequirement", options["treehouse_old_man_requirement"])
    assembler.define_byte("option.tarmGateRequiredJewels", options["tarm_gate_required_jewels"])
    assembler.define_byte("option.signGuyRequirement", options["sign_guy_requirement"])

    assembler.define_byte("option.removeD0AltEntrance", options["remove_d0_alt_entrance"])
    assembler.define_byte("option.deterministicGashaLootCount", options["deterministic_gasha_locations"])

    fools_ore_damage = 3 if options["fools_ore"] == OracleOfSeasonsFoolsOre.option_balanced else 12
    assembler.define_byte("option.foolsOreDamage", (-1 * fools_ore_damage + 0x100))

    assembler.define_byte("option.keysanity_small_keys", patch_data["options"]["keysanity_small_keys"])
    keysanity = patch_data["options"]["keysanity_small_keys"] or patch_data["options"]["keysanity_boss_keys"]
    assembler.define_byte("option.customCompassChimes", 1 if keysanity else 0)

    master_keys_as_boss_keys = patch_data["options"]["master_keys"] == OracleOfSeasonsMasterKeys.option_all_dungeon_keys
    assembler.define_byte("option.smallKeySprite", 0x43 if master_keys_as_boss_keys else 0x42)

    scrubs_all_refill = not patch_data["options"]["shuffle_business_scrubs"]
    assembler.define_byte("var.spoolSwampScrubSubid", 0x04 if scrubs_all_refill else 0x00)
    assembler.define_byte("var.samasaCaveScrubSubid", 0x04 if scrubs_all_refill else 0x01)
    assembler.define_byte("var.d2ScrubSubid", 0x04 if scrubs_all_refill else 0x02)
    assembler.define_byte("var.d4ScrubSubid", 0x04 if scrubs_all_refill else 0x03)


def define_season_constants(assembler: Z80Assembler, patch_data):
    for region_name, season_byte in patch_data["default_seasons"].items():
        assembler.define_byte(f"defaultSeason.{region_name}", season_byte)


def define_lost_woods_sequences(assembler: Z80Assembler, patch_data):
    pedestal_sequence = patch_data["lost_woods_item_sequence"]
    pedestal_bytes, pedestal_text = process_lost_woods_sequence(pedestal_sequence)
    assembler.add_floating_chunk("lostWoodsPedestalSequence", pedestal_bytes)
    assembler.add_floating_chunk("text.lostWoodsPedestalSequence", pedestal_text)

    main_sequence = patch_data["lost_woods_main_sequence"]
    main_bytes, main_text = process_lost_woods_sequence(main_sequence)
    assembler.add_floating_chunk("lostWoodsMainSequence", main_bytes)
    assembler.add_floating_chunk("text.lostWoodsMainSequence", main_text)


def process_lost_woods_sequence(sequence):
    """
    Process a sequence of directions + seasons, and outputs two byte arrays:
    - one to use as a technical data array to check the sequence being done
    - one to use as text hint
    """
    sequence_bytes = []
    text_bytes = []
    for i in range(4):
        direction = sequence[i][0]
        season = sequence[i][1]
        sequence_bytes.extend(sequence[i])
        text_bytes.extend(DIRECTION_STRINGS[direction])
        text_bytes.extend(SEASON_STRINGS[season])
        if i != 3:
            text_bytes.extend([0x05, 0x56])  # wait for input + newline
    text_bytes.append(0x00)
    return sequence_bytes, text_bytes


def get_treasure_addr(rom: RomData, item_name: str):
    item_id, item_subid = get_item_id_and_subid({"item": item_name})
    addr = 0x55129 + (item_id * 4)
    if rom.read_byte(addr) & 0x80 != 0:
        addr = 0x50000 + rom.read_word(addr + 1)
    return addr + (item_subid * 4)


def set_treasure_data(rom: RomData,
                      item_name: str, text_id: int | None,
                      sprite_id: int | None = None,
                      param_value: int | None = None):
    addr = get_treasure_addr(rom, item_name)
    if text_id is not None:
        rom.write_byte(addr + 0x02, text_id)
    if sprite_id is not None:
        rom.write_byte(addr + 0x03, sprite_id)
    if param_value is not None:
        rom.write_byte(addr + 0x01, param_value)


def alter_treasure_types(rom: RomData):
    # Some treasures don't exist as interactions in base game, we need to add
    # text & sprite references for them to work properly in a randomized context
    set_treasure_data(rom, "Fool's Ore", 0x36, 0x4a)
    set_treasure_data(rom, "Rare Peach Stone", None, 0x3f)
    set_treasure_data(rom, "Ribbon", 0x41, 0x4c)
    set_treasure_data(rom, "Treasure Map", 0x6c, 0x49)
    set_treasure_data(rom, "Member's Card", 0x45, 0x48)
    set_treasure_data(rom, "Potion", 0x6d, 0x4b)

    # Set data for remote Archipelago items
    set_treasure_data(rom, "Archipelago Item", 0x57, 0x53)
    set_treasure_data(rom, "Archipelago Progression Item", 0x57, 0x52)

    # Make bombs increase max carriable quantity when obtained from treasures,
    # not drops (see asm/seasons/bomb_bag_behavior)
    set_treasure_data(rom, "Bombs (10)", None, None, 0x90)

    # Colored Rod of Seasons to make them recognizable
    set_treasure_data(rom, "Rod of Seasons (Spring)", None, 0x4f)
    set_treasure_data(rom, "Rod of Seasons (Autumn)", None, 0x50)
    set_treasure_data(rom, "Rod of Seasons (Winter)", None, 0x51)


def set_old_men_rupee_values(rom: RomData, patch_data):
    if patch_data["options"]["shuffle_old_men"] == OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
        return
    for i, name in enumerate(OLD_MAN_RUPEE_VALUES.keys()):
        if name in patch_data["old_man_rupee_values"]:
            value = patch_data["old_man_rupee_values"][name]
            value_byte = RUPEE_VALUES[abs(value)]
            rom.write_byte(0x56233 + i, value_byte)

            if abs(value) == value:
                rom.write_word(0x2987b + (i * 2), 0x7472)  # Give rupees
            else:
                rom.write_word(0x2987b + (i * 2), 0x7488)  # Take rupees


def apply_miscellaneous_options(rom: RomData, patch_data):
    # If companion is Dimitri, allow calling him using the Flute inside Sunken City
    if patch_data["options"]["animal_companion"] == OracleOfSeasonsAnimalCompanion.option_dimitri:
        rom.write_byte(0x24f39, 0xa7)
        rom.write_byte(0x24f3b, 0xe7)

    # If horon shop 3 is set to be a renewable Potion, manually edit the shop flag for
    # that slot to zero to make it stay after buying
    if patch_data["options"]["enforce_potion_in_shop"]:
        rom.write_byte(0x20cfb, 0x00)

    if patch_data["options"]["master_keys"] != OracleOfSeasonsMasterKeys.option_disabled:
        # Remove small key consumption on keydoor opened
        rom.write_byte(0x18357, 0x00)
        # Change obtention text
        rom.write_bytes(0x7546f, [0x02, 0xe5, 0x20, 0x4b, 0x65, 0x79, 0x05, 0xD8, 0x00])
    if patch_data["options"]["master_keys"] == OracleOfSeasonsMasterKeys.option_all_dungeon_keys:
        # Remove boss key consumption on boss keydoor opened
        rom.write_word(0x1834f, 0x0000)


def set_fixed_subrosia_seaside_location(rom: RomData, patch_data):
    """
    Make the location for Subrosia Seaside fixed among the 4 possible locations from the vanilla game.
    This is done to compensate for the poor in-game randomness and potential unfairness in races.
    """
    spots_data = [rom.read_word(addr) for addr in range(0x222D3, 0x222DB, 0x02)]
    spot = spots_data[patch_data["subrosia_seaside_location"]]
    for addr in range(0x222D3, 0x222DB, 0x02):
        rom.write_word(addr, spot)


def set_file_select_text(assembler: Z80Assembler, slot_name: str):
    def char_to_tile(c: str) -> int:
        if '0' <= c <= '9':
            return ord(c) - 0x20
        if 'A' <= c <= 'Z':
            return ord(c) + 0xa1
        if c == '+':
            return 0xfd
        if c == '-':
            return 0xfe
        if c == '.':
            return 0xff
        else:
            return 0xfc  # All other chars are blank spaces

    row_1 = [char_to_tile(c) for c in f"ARCHIPELAGO {VERSION}".ljust(16, " ")]
    row_2 = [char_to_tile(c) for c in slot_name.replace("-", " ").upper()]
    row_2_left_padding = int((16 - len(row_2)) / 2)
    row_2_right_padding = int(16 - row_2_left_padding - len(row_2))
    row_2 = ([0x00] * row_2_left_padding) + row_2 + ([0x00] * row_2_right_padding)

    text_tiles = [0x74, 0x31]
    text_tiles.extend(row_1)
    text_tiles.extend([0x41, 0x40])
    text_tiles.extend([0x02] * 12)  # Offscreen tiles

    text_tiles.extend([0x40, 0x41])
    text_tiles.extend(row_2)
    text_tiles.extend([0x51, 0x50])
    text_tiles.extend([0x02] * 12)  # Offscreen tiles

    assembler.add_floating_chunk("dma_FileSelectStringTiles", text_tiles)


def process_item_name_for_shop_text(item: Dict) -> List[int]:
    if "player" in item:
        player_name = item['player']
        if len(player_name) > 14:
            player_name = player_name[0:13] + "."
        item_name = f"{player_name}'s {item['item']}"
    else:
        item_name = item["item"]

    words = item_name.split(" ")
    current_line = 0
    lines = [""]
    while len(words) > 0:
        line_with_word = lines[current_line]
        if len(line_with_word) > 0:
            line_with_word += " "
        line_with_word += words[0]
        if len(line_with_word) <= 16:
            lines[current_line] = line_with_word
        else:
            current_line += 1
            lines.append(words[0])
        words = words[1:]

    # If name is more than 2 lines long, discard excess lines and put an ellipsis to suggest content was truncated
    if len(lines) > 2:
        lines = lines[0:2]
        lines[1] = lines[1][0:15] + "."

    result = []
    for line in lines:
        if len(line) > 16:
            line = line[0:15] + "."
        if len(result) > 0:
            result.append(0x01)  # Newline
        result.extend(line.encode())
    return result


def define_text_constants(assembler: Z80Assembler, patch_data):
    # Holodrum shop slots
    OVERWORLD_SHOPS = [
        "Horon Village: Shop",
        "Horon Village: Member's Shop",
        "Sunken City: Syrup Shop",
        "Horon Village: Advance Shop"
    ]

    for shop_name in OVERWORLD_SHOPS:
        for i in range(1, 4):
            location_name = f"{shop_name} #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            item_name_bytes = []
            if location_name in patch_data["locations"]:
                item_name_bytes = process_item_name_for_shop_text(patch_data["locations"][location_name])

            text_bytes = [0x09, 0x01] + item_name_bytes + [0x03, 0xe2]  # Item name
            text_bytes.extend([0x20, 0x0c, 0x08, 0x02, 0x8f, 0x01])  # Price
            text_bytes.extend([0x02, 0x00, 0x00])  # OK / No thanks
            assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)

    # Subrosian market slots
    for market_slot in range(1, 6):
        location_name = f"Subrosia: Market #{market_slot}"
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            continue
        item_name_bytes = process_item_name_for_shop_text(patch_data["locations"][location_name])
        text_bytes = [0x09, 0x01] + item_name_bytes + [0x03, 0xe2]  # (Item name)
        text_bytes.extend([0x02, 0x08])  # "I'll trade for"
        if market_slot == 1:
            text_bytes.extend([0x02, 0x8e, 0x2e, 0x01])  # "Star-Shaped Ore."
        else:
            text_bytes.extend([0x09, 0x01, 0x0c, 0x08, 0x20, 0x02, 0x09, 0x2e, 0x01])  # "(number) Ore Chunks."
        assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)

    BUSINESS_SCRUBS = [
        "Spool Swamp: Business Scrub",
        "Samasa Desert: Business Scrub",
        "Snake's Remains: Business Scrub",
        "Dancing Dragon Dungeon (1F): Business Scrub"
    ]
    for location_name in BUSINESS_SCRUBS:
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            assembler.add_floating_chunk(f"text.{symbolic_name}", [])
            assembler.define(f"text.{symbolic_name}Price", "$0000")
            continue
        # Scrub string asking the player if they want to buy the item
        item_name_bytes = process_item_name_for_shop_text(patch_data["locations"][location_name])
        text_bytes = [0x0e, 0xc6, 0x03, 0x79]  # \sfx(0xc6)Greetings!\n
        text_bytes.extend([0x09, 0x01] + item_name_bytes + [0x03, 0xe2])  # (Item name)
        text_bytes.extend([0x04, 0x91, 0x09, 0x04, 0x0c, 0x08])  # "for \green\num"
        text_bytes.extend([0x02, 0x8f, 0x09, 0x00, 0x21, 0x01])  # " Rupees\white!\n"
        text_bytes.extend([0x02, 0x00, 0x00])  # Yes / No
        assembler.add_floating_chunk(f"text.{symbolic_name}", text_bytes)
        # Price as BCD
        price_as_string = str(patch_data["shop_prices"][symbolic_name])
        assembler.define(f"text.{symbolic_name}Price", f"${price_as_string.zfill(4)}")

    assembler.add_floating_chunk("text.signGuyRequirementDigits",
                                 convert_value_to_digits(patch_data["options"]["sign_guy_requirement"]))
    assembler.add_floating_chunk("text.deterministicGashaCountDigits",
                                 convert_value_to_digits(patch_data["options"]["deterministic_gasha_locations"]))


def set_heart_beep_interval_from_settings(rom: RomData):
    heart_beep_interval = get_settings()["tloz_oos_options"]["heart_beep_interval"]
    if heart_beep_interval == "half":
        rom.write_byte(0x9116, 0x3f * 2)
    elif heart_beep_interval == "quarter":
        rom.write_byte(0x9116, 0x3f * 4)
    elif heart_beep_interval == "disabled":
        rom.write_bytes(0x9116, [0x00, 0xc9])  # Put a return to avoid beeping entirely


def set_character_sprite_from_settings(rom: RomData):
    sprite = get_settings()["tloz_oos_options"]["character_sprite"]
    sprite_dir = Path(Utils.local_path(os.path.join('data', 'sprites', 'oos_ooa')))
    if sprite == "random":
        sprite_weights = {f: 1 for f in os.listdir(sprite_dir) if sprite_dir.joinpath(f).is_file() and f.endswith(".bin")}
    elif isinstance(sprite, str):
        sprite_weights = {sprite: 1}
    else:
        sprite_weights = sprite

    weights = random.randrange(sum(sprite_weights.values()))
    for sprite, weight in sprite_weights.items():
        weights -= weight
        if weights < 0:
            break

    palette_option = get_settings()["tloz_oos_options"]["character_palette"]
    if palette_option == "random":
        palette_weights = {palette: 1 for palette in get_available_random_colors_from_sprite_name(sprite)}
    elif isinstance(palette_option, str):
        palette_weights = {palette_option: 1}
    else:
        valid_palettes = get_available_random_colors_from_sprite_name(sprite)
        palette_weights = {}
        for palette, weight in palette_option.items():
            splitted_palette = palette.split("|")
            if len(splitted_palette) == 2 and splitted_palette[1] != sprite:
                continue
            palette_name = splitted_palette[0]
            if palette_name == "random":
                for valid_palette in valid_palettes:
                    palette_weights[valid_palette] = weight
            elif palette_name in valid_palettes:
                palette_weights[palette_name] = weight
        if len(palette_weights) == 0:
            palette_weights["green"] = 1

    weights = random.randrange(sum(palette_weights.values()))
    for palette, weight in palette_weights.items():
        weights -= weight
        if weights < 0:
            break

    if not sprite.endswith(".bin"):
        sprite += ".bin"
    if sprite != "link.bin":
        sprite_path = sprite_dir.joinpath(sprite)
        if not (sprite_path.exists() and sprite_path.is_file()):
            raise ValueError(f"Path '{sprite_path}' doesn't exist")
        sprite_bytes = list(Path(sprite_path).read_bytes())
        rom.write_bytes(0x68000, sprite_bytes)

    if palette == "green":
        return  # Nothing to change
    if palette not in PALETTE_BYTES:
        raise ValueError(f"Palette color '{palette}' doesn't exist (must be 'green', 'blue', 'red' or 'orange')")
    palette_byte = PALETTE_BYTES[palette]

    # Link in-game
    for addr in range(0x141cc, 0x141df, 2):
        rom.write_byte(addr, 0x08 | palette_byte)
    # Link palette restored after Medusa Head / Ganon stun attacks
    rom.write_byte(0x1516d, 0x08 | palette_byte)
    # Link standing still in file select (fileSelectDrawLink:@sprites0)
    rom.write_byte(0x8d46, palette_byte)
    rom.write_byte(0x8d4a, palette_byte)
    # Link animated in file select (@sprites1 & @sprites2)
    rom.write_byte(0x8d4f, palette_byte)
    rom.write_byte(0x8d53, palette_byte)
    rom.write_byte(0x8d58, 0x20 | palette_byte)
    rom.write_byte(0x8d5c, 0x20 | palette_byte)


def inject_slot_name(rom: RomData, slot_name: str):
    slot_name_as_bytes = list(str.encode(slot_name))
    slot_name_as_bytes += [0x00] * (0x40 - len(slot_name_as_bytes))
    rom.write_bytes(0xfffc0, slot_name_as_bytes)


def set_dungeon_warps(rom: RomData, patch_data):
    warp_matchings = patch_data["dungeon_entrances"]
    enter_values = {name: rom.read_word(dungeon["addr"]) for name, dungeon in DUNGEON_ENTRANCES.items()}
    exit_values = {name: rom.read_word(addr) for name, addr in DUNGEON_EXITS.items()}

    # Apply warp matchings expressed in the patch
    for from_name, to_name in warp_matchings.items():
        entrance_addr = DUNGEON_ENTRANCES[from_name]["addr"]
        exit_addr = DUNGEON_EXITS[to_name]
        rom.write_word(entrance_addr, enter_values[to_name])
        rom.write_word(exit_addr, exit_values[from_name])

    # Build a map dungeon => entrance (useful for essence warps)
    entrance_map = dict((v, k) for k, v in warp_matchings.items())

    # D0 Chest Warp (hardcoded warp using a specific format)
    d0_new_entrance = DUNGEON_ENTRANCES[entrance_map["d0"]]
    rom.write_bytes(0x2bbe4, [
        d0_new_entrance["group"] | 0x80,
        d0_new_entrance["room"],
        0x00,
        d0_new_entrance["position"]
    ])

    # D1-D8 Essence Warps (hardcoded in one array using a unified format)
    for i in range(8):
        entrance = DUNGEON_ENTRANCES[entrance_map[f"d{i + 1}"]]
        rom.write_bytes(0x24b59 + (i * 4), [
            entrance["group"] | 0x80,
            entrance["room"],
            entrance["position"]
        ])

    # Change Minimap popups to indicate the randomized dungeon's name
    for i in range(8):
        entrance_name = f"d{i}"
        dungeon_index = int(warp_matchings[entrance_name][1:])
        map_tile = DUNGEON_ENTRANCES[entrance_name]["map_tile"]
        rom.write_byte(0xaa19 + map_tile, 0x81 | (dungeon_index << 3))
    # Dungeon 8 specific case (since it's in Subrosia)
    dungeon_index = int(warp_matchings["d8"][1:])
    rom.write_byte(0xab19, 0x81 | (dungeon_index << 3))


def set_portal_warps(rom: RomData, patch_data):
    warp_matchings = patch_data["subrosia_portals"]

    values = {}
    for portal_1, portal_2 in PORTAL_CONNECTIONS.items():
        values[portal_1] = rom.read_word(PORTAL_WARPS[portal_2]["addr"])
        values[portal_2] = rom.read_word(PORTAL_WARPS[portal_1]["addr"])

    # Apply warp matchings expressed in the patch
    for name_1, name_2 in warp_matchings.items():
        portal_1 = PORTAL_WARPS[name_1]
        portal_2 = PORTAL_WARPS[name_2]

        # Set warp destinations for both portals
        rom.write_word(portal_1["addr"], values[name_2])
        rom.write_word(portal_2["addr"], values[name_1])

        # Set portal text in map menu for both portals
        portal_text_addr = 0xab19 if portal_1["in_subrosia"] else 0xaa19
        portal_text_addr += portal_1["map_tile"]
        rom.write_byte(portal_text_addr, 0x80 | (portal_2["text_index"] << 3))

        portal_text_addr = 0xab19 if portal_2["in_subrosia"] else 0xaa19
        portal_text_addr += portal_2["map_tile"]
        rom.write_byte(portal_text_addr, 0x80 | (portal_1["text_index"] << 3))


def define_dungeon_items_text_constants(assembler: Z80Assembler, patch_data):
    for i in range(9):
        if i == 0:
            # " for\nHero's Cave"
            dungeon_precision = [0x02, 0xe2, 0x03, 0x78]
        else:
            # " for\nDungeon X"
            dungeon_precision = [0x02, 0xe2, 0x44, 0x05, 0x8a, 0x20, (0x30 + i)]

        # ###### Small keys ##############################################
        # "You found a\n\color(RED)"
        small_key_text = [0x05, 0x9d, 0x02, 0x78, 0x61, 0x01, 0x09, 0x01]
        if patch_data["options"]["master_keys"]:
            # "Master Key"
            small_key_text.extend([0x02, 0xe5, 0x20, 0x4b, 0x65, 0x79])
        else:
            # "Small Key"
            small_key_text.extend([0x53, 0x6d, 0x04, 0x07, 0x4b, 0x65, 0x79])
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text.extend(dungeon_precision)
        small_key_text.extend([0x05, 0xd8, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.smallKeyD{i}", small_key_text)

        # Hero's Cave only has Small Keys, so skip other texts
        if i == 0:
            continue

        # ###### Boss keys ##############################################
        # "You found the\n\color(RED)Boss Key"
        boss_key_text = [
            0x05, 0x9d, 0x02, 0x78, 0x04, 0xa7,
            0x09, 0x01, 0x42, 0x6f, 0x73, 0x73, 0x20, 0x4b, 0x65, 0x79
        ]
        if patch_data["options"]["keysanity_boss_keys"]:
            boss_key_text.extend(dungeon_precision)
        boss_key_text.extend([0x05, 0xd8, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.bossKeyD{i}", boss_key_text)

        # ###### Dungeon maps ##############################################
        # "You found the\n\color(RED)"
        dungeon_map_text = [0x05, 0x9d, 0x02, 0x78, 0x04, 0xa7, 0x09, 0x01]
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text.extend([0x4d, 0x61, 0x70])  # "Map"
            dungeon_map_text.extend(dungeon_precision)
        else:
            dungeon_map_text.extend([0x44, 0x05, 0x8a, 0x20, 0x4d, 0x61, 0x70])  # "Dungeon Map"
        dungeon_map_text.extend([0x05, 0xd8, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.dungeonMapD{i}", dungeon_map_text)

        # ###### Compasses ##############################################
        # "You found the\n\color(RED)Compass"
        compasses_text = [
            0x05, 0x9d, 0x02, 0x78, 0x04, 0xa7,
            0x09, 0x01, 0x43, 0x6f, 0x6d, 0x05, 0x11
        ]
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text.extend(dungeon_precision)
        compasses_text.extend([0x05, 0xd8, 0x00])  # "\color(WHITE)!(end)"
        assembler.add_floating_chunk(f"text.compassD{i}", compasses_text)


def define_essence_sparkle_constants(assembler: Z80Assembler, patch_data):
    byte_array = []
    show_dungeons_with_essence = patch_data["options"]["show_dungeons_with_essence"]

    essence_pedestals = [k for k, v in LOCATIONS_DATA.items() if v.get("essence", False)]
    if show_dungeons_with_essence and not patch_data["options"]["shuffle_essences"]:
        for i, pedestal in enumerate(essence_pedestals):
            if patch_data["locations"][pedestal]["item"] not in ESSENCES:
                byte_array.extend([0xF0, 0x00])  # Nonexistent room, for padding
                continue

            # Find where dungeon entrance is located, and place the sparkle hint there
            dungeon = f"d{i+1}"
            dungeon_entrance = [k for k, v in patch_data["dungeon_entrances"].items() if v == dungeon][0]
            entrance_data = DUNGEON_ENTRANCES[dungeon_entrance]
            byte_array.extend([entrance_data["group"], entrance_data["room"]])
    assembler.add_floating_chunk("essenceLocationsTable", byte_array)

    require_compass = show_dungeons_with_essence == OracleOfSeasonsShowDungeonsWithEssence.option_with_compass
    assembler.define_byte("option.essenceSparklesRequireCompass", 1 if require_compass else 0)


def randomize_ai_for_april_fools(rom: RomData, seed: int):
    code_table = 0x2f16
    enemy_table = [
        # enemy id in (08, 2f)
        {
            0: [
                0x08,  # river zora
                0x09,  # octorok
                0x0c,  # arrow moblin
                0x0d,  # lynel
                0x0f,
                0x11,  # Pokey is too unreliable and laggy
                0x12,  # gibdo
                0x13,  # spark
                0x14,  # spiked beetle
                0x15,  # bubble
                0x16,  # beamos
                0x18,  # buzzblob
                0x19,  # whisp
                0x1a,  # crab
                0x20,  # masked moblin
                0x22,
                0x23,
                0x25,  # goponga flower
                0x27,
                0x29,
                0x2d,
                0x2e,
                0x2f,
            ],
            1: [
                0x0a,  # boomerang moblin
                0x1c,  # iron mask
                0x1e,  # piranha
                0x25,
                0x2c,  # cheep cheep, will probably break
            ],
            2: [
                0x0b,  # leever
                0x17,  # ghini
                0x21,  # arrow darknut
            ],
            3: [
                0x1b,  # spiny beetle
                0x24,  # like like, flagged as unkillable as the spawner, and is logically not required
                0x2a,
            ],
            4: [
                0x10,  # rope
            ],
            5: [
                0x0e,  # blade trap
                0x2b,
            ],
        },
        # enemy id in (08, 2f), killable
        {
            0: [
                0x09,  # octorok
                0x12,  # gibdo
                0x14,  # spiked beetle
                0x18,  # buzzblob
                0x1a,  # crab
                0x22,
                0x23,
                0x0d,  # lynel
                0x0c,  # arrow moblin
                0x20,  # masked moblin
            ],
            1: [
                0x0a,  # boomerang moblin
                0x1c,  # iron mask
                0x1e,  # piranha
                0x25,
            ],
            2: [
                0x0b,  # leever
                0x17,  # ghini
                0x21,  # arrow darknut
            ],
            4: [
                0x10,  # rope
            ],
        },

        # enemy id in (30, 60)
        {
            0: [
                0x30,
                0x31,
                0x33,
                0x36,
                0x37,
                0x38,
                0x3a,  # water tektite
                0x3b,
                0x3c,
                0x3d,
                0x3e,
                0x43,
                0x46,
                0x48,
                0x49,
                0x4a,
                0x4b,
                0x4d,
                0x4e,
                0x5e,
            ],
            1: [
                0x32,
                0x34,
                0x39,
                0x41,
                0x4c,
            ],
            2: [
                0x40,
                0x52,
            ],
            3: [
                0x51,
                0x58,
            ],
            4: [
                0x45,  # pincer
            ]
        },

        # enemy id in (30, 60), killable
        {
            0: [
                0x30,
                0x31,
                0x3a,  # water tektite
                0x3c,
                0x3d,
                0x3e,
                0x43,
                0x46,
                0x48,
                0x49,
                0x4a,
                0x4b,
                0x4d,
                0x4e,
                0x5e,
            ],
            1: [
                0x32,
                0x34,
                0x39,
                0x4c
            ],
            2: [
                0x40
            ],
        }
    ]
    r = random.Random(seed)
    ai_table = {}

    for bank in enemy_table:
        for cat in bank:
            enemies = bank[cat]
            if isinstance(cat, int) and cat != 0:
                ais = list(bank[cat])
                for cat2 in bank:
                    if isinstance(cat2, int):
                        if cat2 == 0:
                            ais.extend(bank[cat2])
                        elif cat2 >= cat:
                            ais.extend(bank[cat2])
                            ais.extend(bank[cat2])
            else:
                ais = list(bank[cat])
            r.shuffle(ais)
            for i in range(len(enemies)):
                enemy = enemies[i]
                ai = ais.pop()
                ai_table[enemy] = ai

    for enemy in ai_table:
        ai = ai_table[enemy]
        rom.write_word(code_table + enemy * 2, rom.read_word(code_table + ai * 2))

    blinkers = {
        0x08,
        0x10,
        0x24,
        0x34,
        0x40,
        0x41
    }

    # Make some enemies hittable without having access to their AI
    if ai_table[0x08] not in blinkers:
        rom.write_byte(0xFDD92, 0x8F)  # river zora
    if ai_table[0x10] not in blinkers:
        rom.write_byte(0xFDDB2, 0x90)  # rope
    if ai_table[0x24] not in blinkers:
        rom.write_byte(0xFDE02, 0xA2)  # like-like
    if ai_table[0x34] not in blinkers:
        rom.write_byte(0xFDE42, 0xAA)  # zol
    if ai_table[0x40] not in blinkers:
        rom.write_byte(0xFDE72, 0xAF)  # wizzrobes
    if ai_table[0x41] not in blinkers:
        rom.write_byte(0xFDE76, 0xB0)  # crow

    if ai_table[0x14] != 0x14:
        rom.write_byte(0xFDDC2, 0xCE)  # make spiked beetles have the flipped collisions

    if ai_table[0x24] != 0x24:
        # make like like deal low knockback instead of softlocking by grabbing him then never releasing him due to the lack of AI
        rom.write_byte(0x1EED0, 0x01)