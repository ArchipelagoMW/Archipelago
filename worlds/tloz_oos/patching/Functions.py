import os
import random
from collections import defaultdict
from pathlib import Path

import Utils
from settings import get_settings
from .RomData import RomData
from .Util import *
from .asm import asm_files
from .text import normalize_text
from .z80asm.Assembler import Z80Assembler, GameboyAddress
from .z80asm.Util import parse_hex_string_to_value
from ..Hints import make_hint_texts
from ..Options import OracleOfSeasonsOldMenShuffle, OracleOfSeasonsGoal, OracleOfSeasonsAnimalCompanion, \
    OracleOfSeasonsMasterKeys, OracleOfSeasonsFoolsOre, OracleOfSeasonsShowDungeonsWithEssence
from ..data.Locations import LOCATIONS_DATA
from ..data.Constants import *


def get_asm_files(patch_data):
    files = list(asm_files["base"])
    if patch_data["options"]["quick_flute"]:
        files += asm_files["quick_flute"]
    if patch_data["options"]["shuffle_old_men"] == OracleOfSeasonsOldMenShuffle.option_turn_into_locations:
        files += asm_files["old_men_as_locations"]
    if patch_data["options"]["remove_d0_alt_entrance"]:
        files += asm_files["remove_d0_alt_entrance"]
    if patch_data["options"]["remove_d2_alt_entrance"]:
        files += asm_files["remove_d2_alt_entrance"]
    if patch_data["options"]["goal"] == OracleOfSeasonsGoal.option_beat_ganon:
        files += asm_files["ganon_goal"]
    if patch_data["options"]["rosa_quick_unlock"]:
        files += asm_files["instant_rosa"]
    if get_settings()["tloz_oos_options"]["remove_music"]:
        files += asm_files["mute_music"]
    if patch_data["options"]["cross_items"]:
        files += asm_files["cross_items"]
    if patch_data["options"]["secret_locations"]:
        files += asm_files["secret_locations"]
    return files


def write_chest_contents(rom: RomData, patch_data):
    """
    Chest locations are packed inside several big tables in the ROM, unlike other more specific locations.
    This puts the item described in the patch data inside each chest in the game.
    """
    for location_name, location_data in LOCATIONS_DATA.items():
        if location_data.get("collect", COLLECT_TOUCH) != COLLECT_CHEST and not location_data.get("is_chest", False):
            continue
        chest_addr = rom.get_chest_addr(location_data["room"])
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

        # Use no pickup animation for drop or diving small keys
        item_id, _ = get_item_id_and_subid(item)
        if item_id == 0x30 and (mode == COLLECT_DROP or mode == COLLECT_DIVE):
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
            0x01, 0x42, 0x00, 0x14, 0x2f  # Western volcanoes digging spot
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
        item = patch_data["locations"][f"Gasha Nut #{i + 1}"]
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

    assembler.define_byte("option.animalCompanion", 0x0b + patch_data["options"]["animal_companion"])
    assembler.define_byte("option.defaultSeedType", 0x20 + patch_data["options"]["default_seed"])
    assembler.define_byte("option.receivedDamageModifier", options["combat_difficulty"])
    assembler.define_byte("option.openAdvanceShop", options["advance_shop"])

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


def define_lost_woods_sequences(assembler: Z80Assembler, texts: dict[str, str], patch_data):
    pedestal_sequence = patch_data["lost_woods_item_sequence"]
    pedestal_bytes, pedestal_text = process_lost_woods_sequence(pedestal_sequence)
    assembler.add_floating_chunk("lostWoodsPedestalSequence", pedestal_bytes)
    travel_index = texts["TX_0b50"].index("If temperatures")
    texts["TX_0b50"] = texts["TX_0b50"][:travel_index] + pedestal_text

    main_sequence = patch_data["lost_woods_main_sequence"]
    main_bytes, main_text = process_lost_woods_sequence(main_sequence)
    assembler.add_floating_chunk("lostWoodsMainSequence", main_bytes)
    texts["TX_3604"] = ""  # Unused
    travel_index = texts["TX_4500"].index("\ntravel west")
    texts["TX_4500"] = texts["TX_4500"][:travel_index] + "\\stop\n" + main_text


def process_lost_woods_sequence(sequence):
    """
    Process a sequence of directions + seasons, and outputs two byte arrays:
    - one to use as a technical data array to check the sequence being done
    - one to use as text hint
    """
    sequence_bytes = []
    text = ""
    for i in range(4):
        direction = sequence[i][0]
        season = sequence[i][1]
        sequence_bytes.extend(sequence[i])
        text += DIRECTION_STRINGS[direction]
        text += SEASON_STRINGS[season]
        if i == 1:
            text += "\\stop"
        if i != 3:
            text += "\n"
    return sequence_bytes, text


def define_tree_sprites(assembler: Z80Assembler, patch_data):
    tree_data = {  # Name: (map, position)
        "Horon Village: Seed Tree": (0xf8, 0x48),
        "Woods of Winter: Seed Tree": (0x9e, 0x88),
        "Holodrum Plain: Seed Tree": (0x67, 0x88),
        "Spool Swamp: Seed Tree": (0x72, 0x88),
        "Sunken City: Seed Tree": (0x5f, 0x86),
        "Tarm Ruins: Seed Tree": (0x10, 0x48),
    }
    i = 1
    for tree_name in tree_data:
        seed = patch_data["locations"][tree_name]
        if seed["item"] == "Ember Seeds":
            continue
        seed_id, _ = get_item_id_and_subid(seed)
        assembler.define_byte(f"seedTree{i}.map", tree_data[tree_name][0])
        assembler.define_byte(f"seedTree{i}.position", tree_data[tree_name][1])
        assembler.define_byte(f"seedTree{i}.gfx", seed_id - 26)
        assembler.define(f"seedTree{i}.rectangle", f"treeRect{seed_id}")
        i += 1
    if i == 5:
        # Duplicate ember, we have to blank some data
        assembler.define_byte("seedTree5.enabled", 0x0e)
        assembler.define_byte("seedTree5.map", 0xff)
        assembler.define_byte("seedTree5.position", 0)
        assembler.define_byte("seedTree5.gfx", 0)
        assembler.define_word("seedTree5.rectangle", 0)
    else:
        assembler.define_byte("seedTree5.enabled", 0x0d)


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


def set_player_start_inventory(assembler: Z80Assembler, patch_data):
    obtained_treasures_address = parse_hex_string_to_value(DEFINES["wObtainedTreasureFlags"])
    start_inventory_changes = defaultdict(int)

    # ###### Base changes ##############################################
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wIsLinkedGame"])] = 0x00  # No linked gaming
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wAnimalTutorialFlags"])] = 0xff  # Animal vars
    # Remove the requirement to go in the screen under Sunken City tree to make Dimitri bullies appear
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wDimitriState"])] = 0x20
    # Give L-3 ring box
    start_inventory_changes[0xc697] = 0x10
    start_inventory_changes[parse_hex_string_to_value(DEFINES["wRingBoxLevel"])] = 0x03

    # Starting map/compass
    if patch_data["options"]["starting_maps_compasses"]:
        dungeon_compass = parse_hex_string_to_value(DEFINES["wDungeonCompasses"])
        for i in range(dungeon_compass, dungeon_compass + 4):
            start_inventory_changes[i] = 0xff

    start_inventory_data: dict[str, int] = patch_data["start_inventory"]
    # Handle leveled items
    if "Progressive Shield" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wShieldLevel"])] \
            = start_inventory_data["Progressive Shield"]
    bombs = 0
    if "Bombs (10)" in start_inventory_data:
        bombs += start_inventory_data["Bombs (10)"] * 0x10
    if "Bombs (20)" in start_inventory_data:
        bombs += start_inventory_data["Bombs (20)"] * 0x20
    if bombs > 0:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wCurrentBombs"])] \
            = start_inventory_changes[parse_hex_string_to_value(DEFINES["wMaxBombs"])] \
            = min(bombs, 0x99)
        # The bomb amounts are stored in decimal
    if "Progressive Sword" in start_inventory_data:
        start_inventory_changes[0xc6ac] = start_inventory_data["Progressive Sword"]
    if "Progressive Boomerang" in start_inventory_data:
        start_inventory_changes[0xc6b1] = start_inventory_data["Progressive Boomerang"]  # Boomerang level
    if "Ricky's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x01  # Flute icon
        start_inventory_changes[0xc643] |= 0x80  # Ricky State
    if "Dimitri's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x02  # Flute icon
        start_inventory_changes[0xc644] |= 0x80  # Dimitri State
    if "Moosh's Flute" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFluteIcon"])] = 0x03  # Flute icon
        start_inventory_changes[0xc645] |= 0x20  # Moosh State
    if "Progressive Feather" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wFeatherLevel"])] \
            = start_inventory_data["Progressive Feather"]
    if "Switch Hook" in start_inventory_data:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wSwitchHookLevel"])] \
            = start_inventory_data["Switch Hook"]
    bombchus = 0
    if "Bombchus (10)" in start_inventory_data:
        bombchus += start_inventory_data["Bombchus (10)"] * 0x10
    if "Bombchus (20)" in start_inventory_data:
        bombchus += start_inventory_data["Bombchus (20)"] * 0x20
    if bombchus > 0:
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wNumBombchus"])] \
            = start_inventory_changes[parse_hex_string_to_value(DEFINES["wMaxBombchus"])] \
            = min(bombchus, 0x99)
        # The bombchus amounts are stored in decimal

    seed_amount = 0
    if "Progressive Slingshot" in start_inventory_data:
        start_inventory_changes[0xc6b3] = start_inventory_data["Progressive Slingshot"]  # Slingshot level
        seed_amount = 0x20
    if "Seed Shooter" in start_inventory_data:
        seed_amount = 0x20
    if "Seed Satchel" in start_inventory_data:
        satchel_level = start_inventory_data["Seed Satchel"]
        start_inventory_changes[parse_hex_string_to_value(DEFINES["wSeedSatchelLevel"])] = satchel_level
        if satchel_level == 1:
            seed_amount = 0x20
        elif satchel_level == 2:
            seed_amount = 0x50
        else:
            seed_amount = 0x99
    if seed_amount:
        start_inventory_data[SEED_ITEMS[patch_data["options"]["default_seed"]]] = 1  # Add seeds to the start inventory

    # Inventory obtained flags
    current_inventory_index = parse_hex_string_to_value(DEFINES["wInventoryB"])
    for item in start_inventory_data:
        item_id = ITEMS_DATA[item]["id"]
        item_address = obtained_treasures_address + item_id // 8
        item_mask = 0x01 << (item_id % 8)

        start_inventory_changes[item_address] |= item_mask
        if item_id < 0x20:  # items prior to 0x20 are all usable
            if item == "Biggoron's Sword":
                # Biggoron needs special care since it occupies both hands
                if current_inventory_index == parse_hex_string_to_value(DEFINES["wInventoryB"]):
                    start_inventory_changes[current_inventory_index] \
                        = start_inventory_changes[current_inventory_index + 1] \
                        = item_id
                    current_inventory_index += 2
                elif current_inventory_index == parse_hex_string_to_value(DEFINES["wInventoryB"]) + 1:
                    current_inventory_index += 1
                    start_inventory_changes[current_inventory_index] = item_id
                    current_inventory_index += 1
            else:
                start_inventory_changes[current_inventory_index] = item_id  # Place the item in the inventory
                current_inventory_index += 1

        if item_id == 0x07:  # Rod of Seasons
            season = ITEMS_DATA[item]["subid"] - 2
            start_inventory_changes[0xc6b0] |= 0x01 << season
        elif item_id == 0x28:  # Rupees
            amount = int(item.split("(")[1][:-1])  # Find the value in the item name
            start_inventory_changes[0xc6a5] += amount * start_inventory_data[item]
        elif item_id == 0x37:  # Ore Chunks
            amount = int(item.split("(")[1][:-1])  # Find the value in the item name
            start_inventory_changes[0xc6a7] += amount * start_inventory_data[item]
        elif item_id == 0x30:  # Small keys
            subid = ITEMS_DATA[item]["subid"] % 0x80
            start_inventory_changes[0xc66e + subid] += start_inventory_data[item]
        elif item_id == 0x31:  # Boss keys
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xc67a + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x32:  # Compasses
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xc67c + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x33:  # Maps
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[0xc67e + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x2d:  # Rings
            subid = ITEMS_DATA[item]["subid"] - 4
            start_inventory_changes[parse_hex_string_to_value(DEFINES["wRingsObtained"]) + subid // 8] |= 0x01 << subid % 8
        elif item_id == 0x40:  # Essences
            subid = ITEMS_DATA[item]["subid"]
            start_inventory_changes[parse_hex_string_to_value(DEFINES["wEssencesObtained"])] |= 0x01 << subid % 8
        elif 0x20 <= item_id <= 0x24:  # Seeds
            seed_address = parse_hex_string_to_value(DEFINES["wNumEmberSeeds"]) + item_id - 0x20
            start_inventory_changes[seed_address] = seed_amount

    if 0xc6a5 in start_inventory_changes:
        hex_rupee_count = parse_hex_string_to_value(f"${start_inventory_changes[0xc6a5]}")
        start_inventory_changes[0xc6a5] = hex_rupee_count % 0x100
        start_inventory_changes[0xc6a6] = hex_rupee_count // 0x100
    if 0xc6a7 in start_inventory_changes:
        hex_ore_count = parse_hex_string_to_value(f"${start_inventory_changes[0xc6a7]}")
        start_inventory_changes[0xc6a7] = hex_ore_count % 0x100
        start_inventory_changes[0xc6a8] = hex_ore_count // 0x100
    if obtained_treasures_address in start_inventory_changes:
        start_inventory_changes[obtained_treasures_address] |= 1 << 2  # Add treasure punch flag

    heart_pieces = (start_inventory_data.get("Piece of Heart", 0) + start_inventory_data.get("Rare Peach Stone", 0))
    additional_hearts = (start_inventory_data.get("Heart Container", 0) + heart_pieces // 4)
    if additional_hearts:
        start_inventory_changes[0xc6a2] = start_inventory_changes[0xc6a3] = 12 + additional_hearts * 4
    if heart_pieces % 4:
        start_inventory_changes[0xc6a4] = heart_pieces % 4
    if "Gasha Seed" in start_inventory_data:
        start_inventory_changes[0xc6ba] = start_inventory_data["Gasha Seed"]

    # Make the list used in asm
    start_inventory = []
    for address in start_inventory_changes:
        start_inventory.append(address // 0x100)
        start_inventory.append(address % 0x100)
        start_inventory.append(start_inventory_changes[address])

    start_inventory.append(0x00)  # End of the list
    assembler.add_floating_chunk("startingInventory", start_inventory)


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
    set_treasure_data(rom, "Bombs (20)", 0x94, None, 0xa0)
    set_treasure_data(rom, "Bombchus (10)", None, None, 0x90)
    set_treasure_data(rom, "Bombchus (20)", None, None, 0xa0)

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
    rom.write_byte(GameboyAddress(0x0a, 0x46ed).address_in_rom(),
                   patch_data["options"]["gasha_nut_kill_requirement"])
    rom.write_byte(GameboyAddress(0x04, 0x6a31).address_in_rom(),
                   patch_data["options"]["gasha_nut_kill_requirement"] // 2)


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
    from .. import OracleOfSeasonsWorld
    def char_to_tile(c: str) -> int:
        if "0" <= c <= "9":
            return ord(c) - 0x20
        if "A" <= c <= "Z":
            return ord(c) + 0xa1
        if c == "+":
            return 0xfd
        if c == "-":
            return 0xfe
        if c == ".":
            return 0xff
        else:
            return 0xfc  # All other chars are blank spaces

    row_1 = [char_to_tile(c) for c in
             f"ARCHIPELAGO {OracleOfSeasonsWorld.version()}"
             .ljust(16, " ")]
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


def process_item_name_for_shop_text(item: Dict) -> str:
    if "player" in item:
        player_name = item["player"]
        if len(player_name) > 14:
            player_name = player_name[:13] + "."
        item_name = f"🟦{player_name}⬜'s 🟥"
    else:
        item_name = "🟥"
    item_name += item["item"]
    item_name = normalize_text(item_name)
    item_name += "⬜\\stop\n"
    return item_name


def make_text_data(assembler: Z80Assembler, text: dict[str, str], patch_data):
    # Process shops
    OVERWORLD_SHOPS = [
        "Horon Village: Shop",
        "Horon Village: Member's Shop",
        "Sunken City: Syrup Shop",
        "Horon Village: Advance Shop"
    ]
    tx_indices = {
        "horonShop1": "TX_0e04",
        "horonShop2": "TX_0e03",
        "horonShop3": "TX_0e02",
        "memberShop1": "TX_0e1c",
        "memberShop2": "TX_0e1d",
        "memberShop3": "TX_0e1e",
        "syrupShop1": "TX_0d0a",
        "syrupShop2": "TX_0d01",
        "syrupShop3": "TX_0d05",
        "advanceShop1": "TX_0e22",
        "advanceShop2": "TX_0e23",
        "advanceShop3": "TX_0e25",
        "subrosianMarket1": "TX_2b00",
        "subrosianMarket2": "TX_2b01",
        "subrosianMarket3": "TX_2b05",
        "subrosianMarket4": "TX_2b06",
        "subrosianMarket5": "TX_2b10",
        "spoolSwampScrub": "TX_4509",
        "samasaCaveScrub": "TX_450b",
        "d4Scrub": "TX_450c",
        "d2Scrub": "TX_450d",
    }

    for shop_name in OVERWORLD_SHOPS:
        for i in range(1, 4):
            location_name = f"{shop_name} #{i}"
            symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
            if location_name not in patch_data["locations"]:
                continue
            item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
            item_text += (" \\num1 Rupees\n"
                          "  \\optOK \\optNo thanks\\cmd(0f)")
            text[tx_indices[symbolic_name]] = item_text

    for market_slot in range(1, 6):
        location_name = f"Subrosia: Market #{market_slot}"
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            continue
        item_text = process_item_name_for_shop_text(patch_data["locations"][location_name])
        if market_slot == 1:
            item_text += ("I'll trade for\n"
                          "🟥Star-Shaped Ore⬜.\n"
                          "\\jump(0b)")
        else:
            item_text += ("I'll trade for\n"
                          "🟥\\num1 Ore Chunks⬜.\n"
                          "\\jump(0b)")
        text[tx_indices[symbolic_name]] = item_text

    BUSINESS_SCRUBS = [
        "Spool Swamp: Business Scrub",
        "Samasa Desert: Business Scrub",
        "Snake's Remains: Business Scrub",
        "Dancing Dragon Dungeon (1F): Business Scrub"
    ]
    for location_name in BUSINESS_SCRUBS:
        symbolic_name = LOCATIONS_DATA[location_name]["symbolic_name"]
        if location_name not in patch_data["locations"]:
            continue
        # Scrub string asking the player if they want to buy the item
        item_text = ("\\sfx(c6)Greetings!\n"
                     + process_item_name_for_shop_text(patch_data["locations"][location_name])
                     + f"for 🟩{patch_data['shop_prices'][symbolic_name]} Rupees⬜\n"
                       "  \\optOK \\optNo thanks")
        text[tx_indices[symbolic_name]] = item_text

    # Cross items
    assembler.define_byte("text.hook1.treasure", 0x3b)
    assembler.define_byte("text.hook2.treasure", 0x51)
    assembler.define_byte("text.cane.treasure", 0x53)
    assembler.define_byte("text.shooter.treasure", 0x54)

    assembler.define_byte("text.hook1.inventory", 0x1e)
    assembler.define_byte("text.hook2.inventory", 0x1e)
    assembler.define_byte("text.cane.inventory", 0x1d)
    assembler.define_byte("text.shooter.inventory", 0x2e)

    # Default satchel seed
    seed_name = SEED_ITEMS[patch_data["options"]["default_seed"]].replace(" ", "\n")
    text["TX_002d"] = text["TX_002d"].replace("Ember\nSeeds", seed_name)

    # Misc
    if patch_data["options"]["rosa_quick_unlock"]:
        text["TX_2904"] = ("Since you're so\n"
                           "nice, I unlocked\n"
                           "all the doors\n"
                           "here for you.")

    text["TX_3e1b"] = ("You've broken\n🟩\\num1 signs⬜!\n"
                       "You'd better not\n"
                       "break more than\n"
                       f"🟩{patch_data['options']['sign_guy_requirement']}⬜"
                       ", or else...")

    # Inform the player of how many gashas are good
    wife_text_index = text["TX_3101"].index("The place")
    num_seeds = patch_data["options"]["deterministic_gasha_locations"]
    if num_seeds == 0:
        seed_text = ("nuts will not\n"
                     "contain anything\n"
                     "useful.")
    elif num_seeds == 16:
        seed_text = ("every nut can\n"
                     "hold something\n"
                     "useful.")
    else:
        seed_text = ("only your first\n"
                     f"🟩{num_seeds}⬜ nuts can\n"
                     "contain anything\n"
                     "useful.")
    text["TX_3101"] = (text["TX_3101"][:wife_text_index]
                       + "\\stop\n"
                         "You should know\n"
                       + seed_text)

    # Golden beasts
    golden_beasts_requirement = patch_data["options"]["golden_beasts_requirement"]
    if golden_beasts_requirement == 0:
        # Just a funny text for killing no golden beasts
        golden_beast_reward_text = text["TX_1f05"]
        post_congratulation_index = golden_beast_reward_text.index("Sir")
        text["TX_1f04"] = ""
        text["TX_1f05"] = ("You did nothing!\n"
                           "Truly, " + golden_beast_reward_text[post_congratulation_index:])
    elif golden_beasts_requirement < 4:
        number = ["one", "two", "three"][golden_beasts_requirement - 1]
        text["TX_1f04"] = text["TX_1f04"].replace("the four", number)
        text["TX_1f05"] = text["TX_1f05"].replace("all four", number)
        if golden_beasts_requirement == 1:
            text["TX_1f04"] = text["TX_1f04"].replace("beasts", "beast")
            text["TX_1f05"] = text["TX_1f05"].replace("beasts", "beast")

    # Maku tree sign
    essence_count = patch_data["options"]["required_essences"]
    text["TX_2e00"] = (f"Find 🟥{essence_count} essence{'s' if essence_count != 1 else ''}⬜\n"
                       "to get the seed!")

    # Tarm ruins sign
    jewel_count = patch_data["options"]["tarm_gate_required_jewels"]
    text["TX_2e12"] = (f"Bring 🟩{jewel_count}⬜ jewel{'s' if jewel_count != 1 else ''}\n"
                       "for the door\n"
                       "to open.")

    # Tree house old man
    essence_count = patch_data["options"]["treehouse_old_man_requirement"]
    text["TX_3601"] = text["TX_3601"].replace("knows many\n🟥essences⬜...", f"has 🟥{essence_count} essence{'s' if essence_count != 1 else ''}⬜!")

    # With quick rosa, the escort code is disabled
    if patch_data["options"]["rosa_quick_unlock"]:
        text["TX_2906"] = normalize_text("Not me. Maybe ask someone else?")

    make_hint_texts(text, patch_data)


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
    sprite_dir = Path(Utils.local_path(os.path.join("data", "sprites", "oos_ooa")))
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


def define_dungeon_items_text_constants(texts: dict[str, str], patch_data):
    base_id = 0x73
    for i in range(9):
        if i == 0:
            # " for\nHero's Cave"
            dungeon_precision = " for\nHero's Cave"
        else:
            # " for\nDungeon X"
            dungeon_precision = f" for\nDungeon {i}"

        # ###### Small keys ##############################################
        # "You found a\n\color(RED)"
        small_key_text = "You found a\n🟥"
        if patch_data["options"]["master_keys"]:
            # "Master Key"
            small_key_text += "Master Key"
        else:
            # "Small Key"
            small_key_text += "Small Key"
        if patch_data["options"]["keysanity_small_keys"]:
            small_key_text += dungeon_precision
        small_key_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i)}"] = small_key_text

        # Hero's Cave only has Small Keys, so skip other texts
        if i == 0:
            continue

        # ###### Boss keys ##############################################
        # "You found the\n\color(RED)Boss Key"
        boss_key_text = "You found the\n🟥Boss Key"
        if patch_data["options"]["keysanity_boss_keys"]:
            boss_key_text += dungeon_precision
        boss_key_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 8)}"] = boss_key_text

        # ###### Dungeon maps ##############################################
        # "You found the\n\color(RED)"
        dungeon_map_text = "You found the\n🟥"
        if patch_data["options"]["keysanity_maps_compasses"]:
            dungeon_map_text += "Map"
            dungeon_map_text += dungeon_precision
        else:
            dungeon_map_text += "Dungeon Map"
        dungeon_map_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 16)}"] = dungeon_map_text

        # ###### Compasses ##############################################
        # "You found the\n\color(RED)Compass"
        compasses_text = "You found the\n🟥Compass"
        if patch_data["options"]["keysanity_maps_compasses"]:
            compasses_text += dungeon_precision
        compasses_text += "⬜!"
        texts[f"TX_00{simple_hex(base_id + i + 24)}"] = compasses_text


def define_essence_sparkle_constants(assembler: Z80Assembler, patch_data):
    byte_array = []
    show_dungeons_with_essence = patch_data["options"]["show_dungeons_with_essence"]

    essence_pedestals = [k for k, v in LOCATIONS_DATA.items() if v.get("essence", False)]
    if show_dungeons_with_essence and not patch_data["options"]["shuffle_essences"]:
        for i, pedestal in enumerate(essence_pedestals):
            if patch_data["locations"][pedestal]["item"] not in ITEM_GROUPS["Essences"]:
                byte_array.extend([0xF0, 0x00])  # Nonexistent room, for padding
                continue

            # Find where dungeon entrance is located, and place the sparkle hint there
            dungeon = f"d{i + 1}"
            dungeon_entrance = [k for k, v in patch_data["dungeon_entrances"].items() if v == dungeon][0]
            entrance_data = DUNGEON_ENTRANCES[dungeon_entrance]
            byte_array.extend([entrance_data["group"], entrance_data["room"]])
    assembler.add_floating_chunk("essenceLocationsTable", byte_array)

    require_compass = show_dungeons_with_essence == OracleOfSeasonsShowDungeonsWithEssence.option_with_compass
    assembler.define_byte("option.essenceSparklesRequireCompass", 1 if require_compass else 0)


def randomize_ai_for_april_fools(rom: RomData, seed: int):
    code_table = 0x2f16
    # TODO : properly implement that ?
    enemy_table = [
        # enemy id in (08, 2f), specially for the blade traps since they can't take the beamos AI, or they'd block d6
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
                0x18,  # buzzblob
                0x19,  # whisp
                0x1a,  # crab
                0x20,  # masked moblin
                0x22,
                0x23,  # pol's voice
                0x25,  # goponga flower
                0x29,
                0x2d,
                0x2e,
                0x2f
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
                0x23,  # pol's voice
                0x25,  # goponga flower
                0x29,
                0x2d,
                0x2e,
                0x2f
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
                0x23,  # pol's voice
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
                0x4f,
            ],
            2: [
                # 0x40,
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
                0x3c,
                0x3d,
                0x3e,
                0x43,
                0x48,
                0x49,
                0x4a,
                0x4b,
                0x4d,
                0x4e,
            ],
            1: [
                0x32,
                0x34,
                0x39,
                0x4c,
                0x4f,
            ],
            2: [
                # 0x40
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

    ai_table[0x2f] = 0x2f  # Thwomps have to stay vanilla for platforming
    for enemy in ai_table:
        ai = ai_table[enemy]
        rom.write_word(code_table + enemy * 2, rom.read_word(code_table + ai * 2))

    blinkers = {
        0x08,
        0x0b,
        0x10,
        0x24,
        0x34,
        0x40,
        0x41
    }

    # Make some enemies hittable without having access to their AI
    if ai_table[0x08] not in blinkers:
        rom.write_byte(0xFDD92, 0x8F)  # river zora
    if ai_table[0x0b] not in blinkers:
        rom.write_byte(0xFDD9E, 0x90)  # leever
    if ai_table[0x10] not in blinkers:
        rom.write_byte(0xFDDB2, 0x90)  # rope
    if ai_table[0x24] not in blinkers:
        rom.write_byte(0xFDE02, 0xA2)  # like-like
    if ai_table[0x34] not in blinkers:
        rom.write_byte(0xFDE42, 0xAA)  # zol
    # if ai_table[0x40] not in blinkers:
    #     rom.write_byte(0xFDE72, 0xAF)  # wizzrobes
    if ai_table[0x41] not in blinkers:
        rom.write_byte(0xFDE76, 0xB0)  # crow

    if ai_table[0x14] != 0x14:
        rom.write_byte(0xFDDC2, 0xCE)  # Make spiked beetles have the flipped collisions
    if ai_table[0x1C] != 0x1C:
        rom.write_byte(0xFDDE2, 0xD0)  # Make iron mask have the unmasked collisions
    if ai_table[0x3e] != 0x3e:
        rom.write_byte(0xFDE6A, 0xAE)  # Make peahats have vulnerable collisions

    if ai_table[0x24] != 0x24:
        # make like like deal low knockback instead of softlocking by grabbing him then never releasing him due to the lack of AI
        rom.write_byte(0x1EED0, 0x01)
