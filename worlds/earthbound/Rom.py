import hashlib
import os
import Utils
import typing
import struct
import settings
from worlds.Files import APProcedurePatch, APTokenMixin, APTokenTypes, APPatchExtension
from .game_data import local_data
from .game_data.battle_bg_data import battle_bg_bpp
from .modules.psi_shuffle import write_psi
from .game_data.text_data import barf_text, text_encoder
from .modules.flavor_data import flavor_data, vanilla_flavor_pointers
from .modules.hint_data import parse_hint_data
from .modules.enemy_data import scale_enemies
from .modules.area_scaling import calculate_scaling
from .modules.boss_shuffle import write_bosses
from .modules.equipamizer import randomize_armor, randomize_weapons
from .modules.music_rando import music_randomizer
from .modules.palette_shuffle import randomize_psi_palettes, map_palette_shuffle
from .modules.shopsanity import write_shop_checks
from .modules.enemy_shuffler import apply_enemy_shuffle
from .modules.dungeon_er import write_dungeon_entrances
# from .modules.foodamizer import randomize_food
from .modules.enemizer.randomize_enemy_attributes import randomize_enemy_attributes
from .modules.enemizer.randomize_enemy_stats import randomize_enemy_stats
from .modules.enemizer.randomize_enemy_attacks import randomize_enemy_attacks
from .game_data.static_location_data import location_groups
from BaseClasses import ItemClassification
from typing import TYPE_CHECKING, Sequence
from logging import warning
# from .local_data import local_locations

if TYPE_CHECKING:
    from . import EarthBoundWorld

item_id_table = local_data.item_id_table
location_dialogue = local_data.location_dialogue
present_locations = local_data.present_locations
psi_locations = local_data.psi_locations
npc_locations = local_data.npc_locations
character_locations = local_data.character_locations
special_name_table = local_data.special_name_table
item_space_checks = local_data.item_space_checks
local_present_types = local_data.local_present_types
present_text_pointers = local_data.present_text_pointers
psi_item_table = local_data.psi_item_table
character_item_table = local_data.character_item_table
party_id_nums = local_data.party_id_nums
starting_psi_table = local_data.starting_psi_table
badge_names = local_data.badge_names
world_version = local_data.world_version
protection_checks = local_data.protection_checks
protection_text = local_data.protection_text
nonlocal_present_types = local_data.nonlocal_present_types
ap_text_pntrs = local_data.ap_text_pntrs
money_item_table = local_data.money_item_table

valid_hashes = ["a864b2e5c141d2dec1c4cbed75a42a85",  # Cartridge
                "6d71ccc8e2afda15d011348291afdf4f"]  # VC


class LocalRom(object):

    def __init__(self, file: bytes, name: str | None = None) -> None:
        self.file = bytearray(file)
        self.name = name

    def read_byte(self, offset: int) -> int:
        return self.file[offset]

    def read_bytes(self, offset: int, length: int) -> bytes:
        return self.file[offset:offset + length]

    def write_bytes(self, offset: int, values: Sequence[int]) -> None:
        self.file[offset:offset + len(values)] = values

    def get_bytes(self) -> bytes:
        return bytes(self.file)


def patch_rom(world: "EarthBoundWorld", rom: LocalRom, player: int) -> None:
    rom.copy_bytes(0x1578DD, 0x3E, 0x34A060)  # Threed/Saturn teleport move
    rom.copy_bytes(0x15791B, 0xF8, 0x157959)

    rom.copy_bytes(0x34A000, 0x1F, 0x1578DD)
    rom.copy_bytes(0x34A020, 0x1F, 0x15793A)
    rom.copy_bytes(0x34A040, 0x1F, 0x157A51)
    rom.copy_bytes(0x34A060, 0x3E, 0x1578FC)
    rom.copy_bytes(0x15ED4B, 0x06, 0x15F1FB)
    rom.copy_bytes(0x1A7FA7, 0xBF, 0x389900)

    starting_area_coordinates = {
                    0: [0x50, 0x04, 0xB5, 0x1F],  # North Onett
                    1: [0x52, 0x06, 0x4C, 0x1F],  # Onett
                    2: [0xEF, 0x22, 0x41, 0x1F],  # Twoson
                    3: [0x53, 0x06, 0x85, 0x1D],  # Happy Happy
                    4: [0x55, 0x24, 0x69, 0x1D],  # Threed
                    5: [0x60, 0x1D, 0x30, 0x01],  # Saturn Valley
                    6: [0xAB, 0x10, 0xF3, 0x09],  # Fourside
                    7: [0xE3, 0x09, 0xA3, 0x1D],  # Winters
                    8: [0xCB, 0x24, 0x7B, 0x1E],  # Summers
                    9: [0xD0, 0x1E, 0x31, 0x1D],  # Dalaam
                    10: [0xC7, 0x1F, 0x37, 0x19],  # Scaraba
                    11: [0xDD, 0x1B, 0xB7, 0x17],  # Deep Darkness
                    12: [0xD0, 0x25, 0x47, 0x18],  # Tenda Village
                    13: [0x9C, 0x00, 0x84, 0x17],  # Lost Underworld
                    14: [0x4B, 0x11, 0xAD, 0x18]  # Magicant
    }

    starting_levels = {
        "Ness": 0x15F5FB,
        "Paula": 0x15F60F,
        "Jeff": 0x15F623,
        "Poo": 0x15F637
    }

    atm_card_slots = {
        "Ness": 0x15F5FF,
        "Paula": 0x15F613,
        "Jeff": 0x15F629,
        "Poo": 0x15F63B
    }

    starting_weapon = {
        "Ness": [0x15F600, 0x12],
        "Paula": [0x15F615, 0x1C],
        "Jeff": [0x15F62A, 0x24]
    }

    teleport_learnlevel = {
        "Ness": [0x158D53, 0x158D62],
        "Paula": [0x158D54, 0x158D63],
        "Poo": [0x158D55, 0x158D64]
    }
    world.start_items = []
    world.handled_locations = []
    
    for item in world.multiworld.precollected_items[world.player]:
        world.start_items.append(item.name)

    if world.options.random_start_location:
        rom.write_bytes(0x0F96C2, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9618, bytearray([0x69, 0x00]))
        rom.write_bytes(0x0F9629, bytearray([0x69, 0x00]))  # Block Northern Onett
    else:
        rom.write_bytes(0x00B66A, bytearray([0x06]))  # Fix starting direction
    
    rom.write_bytes(0x01FE9B, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE9E, bytearray(starting_area_coordinates[world.start_location][2:4]))  # Start position

    rom.write_bytes(0x01FE91, bytearray(starting_area_coordinates[world.start_location][0:2]))
    rom.write_bytes(0x01FE8B, bytearray(starting_area_coordinates[world.start_location][2:4]))  # Respawn position

    if world.options.skip_epilogue:
        rom.write_bytes(0x09C4D4, struct.pack("I", 0xEEA437))

    if world.starting_character == "Poo":
        rom.write_bytes(starting_levels[world.starting_character], bytearray([0x06]))
    else:
        rom.write_bytes(starting_levels[world.starting_character], bytearray([0x03]))
    rom.write_bytes(atm_card_slots[world.starting_character], bytearray([0xB1]))
    if world.starting_character != "Ness":
        rom.write_bytes(atm_card_slots["Ness"], bytearray([0x58]))
    if world.starting_character != "Poo":
        rom.write_bytes(starting_weapon[world.starting_character][0], bytearray([starting_weapon[world.starting_character][1]]))

    if world.starting_character != "Jeff":
        for i in range(2):
            rom.write_bytes(teleport_learnlevel[world.starting_character][i - 1], bytearray([0x01]))
    else:
        rom.write_bytes(0x15F62B, bytearray([0xB5]))

    if world.options.alternate_sanctuary_goal:
        rom.write_bytes(0x04FD72, bytearray([world.options.sanctuaries_required.value + 2]))
    else:
        rom.write_bytes(0x04FD72, bytearray([0xFF]))

    if not world.options.giygas_required:
        rom.write_bytes(0x2E9C29, bytearray([0x10, 0xA5]))

    if world.options.magicant_mode == 2:
        rom.write_bytes(0x04FD71, bytearray([world.options.sanctuaries_required.value + 1]))
        rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE]))  # Alt goal magicant sets the credits
    elif world.options.magicant_mode == 1:
        rom.write_bytes(0x2E9C29, bytearray([0x00, 0xA5]))
        if world.options.giygas_required:
            rom.write_bytes(0x2EA26A, bytearray([0x08, 0xD9, 0x9B, 0xEE]))  # Give stat boost if magicant + giygas required
        else:
            rom.write_bytes(0x2EA26A, bytearray([0x0A, 0x10, 0xA5, 0xEE]))  # If no giygas, set credits
    elif world.options.magicant_mode == 3:
        rom.write_bytes(0x2EA26A, bytearray([0x08, 0x0F, 0x9C, 0xEE]))  # Give only stat boost if set to boost

    rom.write_bytes(0x04FD74, bytearray([world.options.death_link.value]))
    rom.write_bytes(0x04FD75, bytearray([world.options.death_link_mode.value]))
    rom.write_bytes(0x04FD76, bytearray([world.options.remote_items.value]))
    rom.write_bytes(0x04FD78, bytearray([world.options.energy_link.value]))

    if world.options.death_link_mode != 1:
        rom.write_bytes(0x2FFDFE, bytearray([0x80]))  # Mercy healing
        rom.write_bytes(0x2FFE30, bytearray([0x80]))  # Mercy text
        rom.write_bytes(0x2FFE59, bytearray([0x80]))  # Mercy revive
        # IF YOU ADD ASM, CHANGE THESE OR THE GAME WILL CRASH

    if world.options.monkey_caves_mode == 2:
        rom.write_bytes(0x062B87, bytearray([0x0A, 0x28, 0xCA, 0xEE]))
    elif world.options.monkey_caves_mode == 3:
        rom.write_bytes(0x0F1388, bytearray([0x03, 0xCA, 0xEE]))

    if world.options.no_free_sanctuaries:
        rom.write_bytes(0x0F09F2, bytearray([0x15, 0x84]))  # Lock Lilliput steps with flag $0415
        rom.write_bytes(0x0F09EE, struct.pack("I", 0xEEF790))  # Lilliput door script

        rom.write_bytes(0x0F23D2, bytearray([0x16, 0x84]))  # Lock Fire Spring with flag $0146
        rom.write_bytes(0x0F23CE, struct.pack("I", 0xEEF946))  # Fire Spring door script

    rom.write_bytes(0x04FD70, bytearray([world.options.sanctuaries_required.value]))
    shop_checks = []
    
    for location in world.multiworld.get_locations(player):
        if location.address:
            receiver_name = world.multiworld.get_player_name(location.item.player)
            name = location.name
            if world.options.remote_items:
                item = "Remote Item"
            else:
                item = location.item.name
            item_name_loc = (((location.address - 0xEB0000) * 128) + 0x3F0000)
            # todo; replace with the encoder function
            item_text = text_encoder(location.item.name, 128)
            item_text.extend([0x00])
            player_name_loc = (((location.address - 0xEB0000) * 48) + 0x3F8000)
            player_text = text_encoder(receiver_name, 48)
            # Locations over this address are Shopsanity locations and handled in the shopsanity module
            if location.address < 0xEB1000:
                rom.write_bytes(item_name_loc, bytearray(item_text))
                rom.write_bytes(player_name_loc, bytearray(player_text))

            if item not in item_id_table or location.item.player != location.player:
                item_id = 0xAD
            else:
                item_id = item_id_table[item]

            if name in location_dialogue:
                for i in range(len(location_dialogue[name])):
                    if location.item.player != location.player or item == "Remote Item":
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x17, location.address - 0xEB0000]))
                    elif item in item_id_table:
                        rom.write_bytes(location_dialogue[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x16, special_name_table[item][0]]))
                    elif item in money_item_table:
                        rom.write_bytes(location_dialogue[name][i] - 1, bytearray([0x16, (0x16 + list(money_item_table).index(item))]))

            if name in present_locations:
                world.handled_locations.append(name)
                if item == "Nothing":  # I can change this to "In nothing_table" later todo: make it so nonlocal items do not follow this table
                    rom.write_bytes(present_locations[name], bytearray([0x00, 0x00, 0x01]))
                elif location.item.player != location.player or item == "Remote Item":
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00, 0x00, (location.address - 0xEB0000)]))
                elif item in item_id_table:
                    rom.write_bytes(present_locations[name], bytearray([item_id, 0x00]))
                elif item in psi_item_table:
                    rom.write_bytes(present_locations[name], bytearray([psi_item_table[item], 0x00, 0x02]))
                elif item in character_item_table:
                    rom.write_bytes(present_locations[name], bytearray([character_item_table[item][0], 0x00, 0x03]))
                elif item in money_item_table:
                    rom.write_bytes(present_locations[name], struct.pack("H", money_item_table[item]))
                    rom.write_bytes(present_locations[name] + 2, bytearray([0x01]))

            if name in npc_locations:
                world.handled_locations.append(name)
                for i in range(len(npc_locations[name])):
                    if item in item_id_table or location.item.player != location.player or item == "Remote Item":
                        rom.write_bytes(npc_locations[name][i], bytearray([item_id]))
                    elif item in psi_item_table or item in character_item_table:
                        rom.write_bytes(npc_locations[name][i] - 3, bytearray([0x0E, 0x00, 0x0E, (special_name_table[item][0] + 1)]))
                        rom.write_bytes(npc_locations[name][i] + 2, bytearray([0xA5, 0xAA, 0xEE]))
                    elif item in money_item_table:
                        rom.write_bytes(npc_locations[name][i] - 3, bytearray([0x1D, 0x25]))
                        rom.write_bytes(npc_locations[name][i] - 1, struct.pack("H", money_item_table[item]))
                        rom.write_bytes(npc_locations[name][i] + 2, bytearray([0x00, 0xF0, 0xF3]))

            if name in psi_locations:
                world.handled_locations.append(name)
                if item in special_name_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(psi_locations[name][0], special_name_table[item][1].to_bytes(3, byteorder="little"))
                    rom.write_bytes(psi_locations[name][0] + 4, bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
                elif item in money_item_table and location.item.player == location.player:
                    rom.write_bytes(psi_locations[name][0] - 1, bytearray([0x1D, 0x25]))
                    rom.write_bytes(psi_locations[name][0] + 1, struct.pack("H", money_item_table[item]))
                    rom.write_bytes(psi_locations[name][0] + 3, bytearray([0x08, 0x26, 0xF0, 0xF3, 0x00, 0x03, 0x00]))
                else:
                    rom.write_bytes(psi_locations[name][0], bytearray(psi_locations[name][1:4]))
                    rom.write_bytes(psi_locations[name][4], bytearray([item_id]))

            if name in character_locations:
                world.handled_locations.append(name)
                if item in character_item_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(character_locations[name][0], special_name_table[item][1].to_bytes(3, byteorder="little"))
                    if name == "Snow Wood - Bedroom":  # Use lying down sprites for the bedroom check
                        rom.write_bytes(character_locations[name][1], struct.pack("H", character_item_table[item][2]))
                        rom.write_bytes(0x0FB0D8, bytearray([0x06]))
                    else:
                        rom.write_bytes(character_locations[name][1], struct.pack("H", character_item_table[item][1]))
                elif item in psi_item_table and location.item.player == location.player:
                    rom.write_bytes(character_locations[name][0], (special_name_table[item][1] + 1).to_bytes(3, byteorder="little"))
                    rom.write_bytes(character_locations[name][1], bytearray([0x62]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x70, 0xF9, 0xD5]))
                elif item in money_item_table and location.item.player == location.player:
                    rom.write_bytes(character_locations[name][2] - 1, bytearray([0x1D, 0x25]))
                    rom.write_bytes(character_locations[name][2] + 1, struct.pack("H", money_item_table[item]))
                    rom.write_bytes(character_locations[name][0] - 2, bytearray([0x01]))
                    rom.write_bytes(character_locations[name][0], bytearray([0x4B, 0xF0, 0xF3]))
                    rom.write_bytes(character_locations[name][1], bytearray([0x97]))
                else:
                    rom.write_bytes(character_locations[name][0], bytearray(character_locations[name][4:7]))
                    if location.item.name in ["Ness", "Paula", "Jeff", "Poo"]:
                        rom.write_bytes(character_locations[name][1], bytearray([character_item_table[location.item.name][1]]))
                    else:
                        rom.write_bytes(character_locations[name][1], bytearray([0x97]))
                    rom.write_bytes(character_locations[name][2], bytearray([0x18, 0xF9, 0xD5]))
                    rom.write_bytes(character_locations[name][3], bytearray([item_id]))
                if name == "Deep Darkness - Barf Character":
                    if item in character_item_table:
                        rom.write_bytes(0x2EA0E2, bytearray(barf_text[item][0:3]))
                        rom.write_bytes(0x2EA0E8, bytearray(barf_text[item][3:6]))
                    elif item in psi_item_table and location.item.player == location.player:
                        rom.write_bytes(0x2EA0E2, bytearray([0x98, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xF7, 0xC4, 0xEE]))
                    else:
                        rom.write_bytes(0x2EA0E2, bytearray([0x6A, 0xC3, 0xEE]))
                        rom.write_bytes(0x2EA0E8, bytearray([0xB4, 0xC4, 0xEE]))

            if name == "Poo - Starting Item":
                world.handled_locations.append(name)
                if item in item_id_table and location.item.player == location.player and item != "Remote Item":
                    rom.write_bytes(0x15F63C, bytearray([item_id]))
                else:
                    rom.write_bytes(0x15F63C, bytearray([0x00]))  # Don't give anything if the item doesn't have a tangible ID

                if item in special_name_table and location.item.player == location.player:  # Apply a special script if teleport or character
                    rom.write_bytes(0x15F765, special_name_table[item][1].to_bytes(3, byteorder="little"))  # This might be offset, check if it is
                    rom.write_bytes(0x2EC618, bytearray([(special_name_table[item][0] + 1)]))
                    rom.write_bytes(0x2EC61A, bytearray([0xA5, 0xAA, 0xEE]))
                    rom.write_bytes(0x2EC613, bytearray([0x03, 0x01]))
                
                if item in money_item_table and location.item.player == location.player:
                    rom.write_bytes(0x15F764, bytearray([0x1D, 0x08]))
                    rom.write_bytes(0x15F766, struct.pack("H", money_item_table[item]))
                    rom.write_bytes(0x15F768, bytearray([0x01]))

            if location.address >= 0xEB1000:
                world.handled_locations.append(name)
                shop_checks.append(location)

            if name not in world.handled_locations:
                warning(f"{name} not placed in {world.multiworld.get_player_name(world.player)}'s EarthBound world. Something went wrong here.")
            
            if name in item_space_checks:
                if item not in item_id_table or location.item.player != location.player:
                    if len(item_space_checks[name]) == 4:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                    else:
                        rom.write_bytes(item_space_checks[name][0], bytearray(item_space_checks[name][1:4]))
                        rom.write_bytes(item_space_checks[name][4], bytearray(item_space_checks[name][5:8]))

            if name in present_locations and "Lost Underworld" not in name and world.options.presents_match_contents:
                if ItemClassification.trap in location.item.classification:
                    world.present_type = "trap"
                elif ItemClassification.progression in location.item.classification:
                    world.present_type = "progression"
                elif ItemClassification.useful in location.item.classification:
                    world.present_type = "useful"
                else:
                    world.present_type = "filler"

                if location.item.player == world.player or world.options.nonlocal_items_use_local_presents:
                    rom.write_bytes(present_locations[name] - 12, bytearray(local_present_types[world.present_type]))
                    if name != "Threed - Boogey Tent Trashcan":
                        rom.write_bytes(present_locations[name] - 4, bytearray(present_text_pointers[world.present_type]))
                else:
                    rom.write_bytes(present_locations[name] - 12, bytearray(nonlocal_present_types[world.present_type]))
                    if name != "Threed - Boogey Tent Trashcan":
                        if world.present_type == "progression":
                            rom.write_bytes(present_locations[name] - 4, struct.pack("I", world.random.choice(ap_text_pntrs)))
                        elif world.present_type == "trap":
                            rom.write_bytes(present_locations[name] - 4, bytearray([0x8D, 0xce, 0xee]))
                        else:
                            rom.write_bytes(present_locations[name] - 4, bytearray([0xc1, 0xcd, 0xee]))

    location = world.multiworld.get_location("Twoson - Bike Shop Rental", world.player)
    if location.item.name in item_id_table:
        item_id = item_id_table[location.item.name]
    else:
        item_id = 0xAD

    rom.write_bytes(0x0800C4, bytearray([item_id]))  # Bike shop
    rom.write_bytes(0x0802EA, bytearray([item_id]))

    rom.write_bytes(0x2EA05C, bytearray([item_id_table[world.slime_pile_wanted_item]]))
    rom.write_bytes(0x2F61F6, bytearray([item_id_table[world.slime_pile_wanted_item]]))
    
    hintable_locations = [
        location for location in world.multiworld.get_locations()
        if location.player == world.player or location.item.player == world.player
    ]
    world.hint_pointer = 0x0000
    world.hint_number = 0
    for index, hint in enumerate(world.in_game_hint_types):
        if hint == "item_at_location":
            for location in hintable_locations:
                if location.name == world.hinted_locations[index] and location.player == world.player:
                    parse_hint_data(world, location, rom, hint, index)
                    
        elif hint == "region_progression_check":
            world.progression_count = 0
            for location in hintable_locations:
                if location.name in location_groups[world.hinted_regions[index]] and location.player == world.player:
                    if ItemClassification.progression in location.item.classification:
                        world.progression_count += 1
            world.hinted_area = world.hinted_regions[index]  # im doing a little sneaky
            parse_hint_data(world, location, rom, hint, index)

        elif hint == "hint_for_good_item" or hint == "prog_item_at_region":
            hintable_locations_2 = []
            for location in hintable_locations:
                if location.item.name == world.hinted_items[index] and location.item.player == world.player:
                    hintable_locations_2.append(location)
            if hintable_locations_2 == []:
                # This is just failsafe behavior
                warning(f"Warning: Unable to create local hint for {world.hinted_items[index]} for "
                        + f"{world.multiworld.get_player_name(world.player)}'s EarthBound world."
                        + " Please report this.")
                location = world.random.choice(hintable_locations)
            else:
                location = world.random.choice(hintable_locations_2)
            parse_hint_data(world, location, rom, hint, index)

        elif hint == "item_in_local_region":
            for location in hintable_locations:
                if location.name == world.hinted_locations[index] and location.player == world.player:
                    parse_hint_data(world, location, rom, hint, index)
        else:
            location = "null"
            parse_hint_data(world, location, rom, hint, index)
    
    for location in hintable_locations:
        if location.item.name == "Paula":
            world.paula_region = location.parent_region
        
        if location.item.name == "Jeff":
            world.jeff_region = location.parent_region

        if location.item.name == "Poo":
            world.poo_region = location.parent_region

    if world.options.skip_prayer_sequences:
        rom.write_bytes(0x07BC96, bytearray([0x02]))
        rom.write_bytes(0x07BA2C, bytearray([0x02]))
        rom.write_bytes(0x07BAC7, bytearray([0x02]))
        rom.write_bytes(0x07BB38, bytearray([0x02]))
        rom.write_bytes(0x07BBF3, bytearray([0x02])) 
        rom.write_bytes(0x07BC56, bytearray([0x02])) 
        rom.write_bytes(0x07B9A1, bytearray([0x1f, 0xeb, 0xff, 0x02, 0x1f, 0x1f, 0xca, 0x01, 0x06, 0x1f, 0x1f, 0x72, 0x01, 0x06, 0x02]))  # Clean up overworld stuff

    if world.options.easy_deaths:
        rom.write_bytes(0x2EBFF9, bytearray([0x0A]))
        rom.write_bytes(0x04C7CE, bytearray([0x5C, 0x8A, 0xFB, 0xEF]))  # Jump to code that restores the party
        rom.write_bytes(0x04C7D4, bytearray([0xEA, 0xEA, 0xEA]))
        # rom.write_bytes(0x04C7DA, bytearray([0xEA, 0xEA]))#Stop the game from zeroing stuff
        rom.write_bytes(0x0912F2, bytearray([0x0A, 0xFE, 0xBF, 0xEE]))
        rom.write_bytes(0x2EBFFE, bytearray([0x00, 0x1B, 0x04, 0x15, 0x38, 0x1F, 0x81, 0xFF, 0xFF, 0x1B, 0x04, 0x0A, 0xF7, 0x12, 0xC9]))  # Hospitals = 0$
        rom.write_bytes(0x04C822, bytearray([0xEA, 0xEA, 0xEA, 0xEA]))
        rom.write_bytes(0x04C7F7, bytearray([0x00, 0x00])) # Stop "rounding up" the money

    if world.options.magicant_mode >= 2:
        rom.write_bytes(0x077629, bytearray([item_id_table[world.magicant_junk[0]]]))
        rom.write_bytes(0x077614, bytearray([item_id_table[world.magicant_junk[0]]]))
        rom.write_bytes(0x0FF25C, bytearray([item_id_table[world.magicant_junk[1]]]))
        rom.write_bytes(0x0FF27E, bytearray([item_id_table[world.magicant_junk[2]]]))
        rom.write_bytes(0x0FF28F, bytearray([item_id_table[world.magicant_junk[3]]]))
        rom.write_bytes(0x0FF2A0, bytearray([item_id_table[world.magicant_junk[4]]]))
        rom.write_bytes(0x0FF26D, bytearray([item_id_table[world.magicant_junk[5]]]))

    rom.write_bytes(0x02EC1AA, bytearray([world.options.sanctuaries_required.value]))
    if world.options.alternate_sanctuary_goal and world.options.giygas_required:
        rom.write_bytes(0x02EC1E2, bytearray([0xFD, 0xC1, 0xEE]))

    if world.options.magicant_mode == 1 and world.options.giygas_required:  # Apple kid text
        rom.write_bytes(0x2EC1D8, bytearray([0x33, 0xC2, 0xEE]))
    elif world.options.magicant_mode == 2:
        rom.write_bytes(0x2EC1D8, bytearray([0x6A, 0xC2, 0xEE]))

    if not world.options.giygas_required:
        rom.write_bytes(0x2EC164, bytearray([0xE8, 0xF0, 0xEE]))
        rom.write_bytes(0x02EC1E2, bytearray([0x40, 0xC1, 0xEE]))
        rom.write_bytes(0x02EC1E2, bytearray([0x40, 0xC1, 0xEE]))
    
    flavor_address = 0x3FAF10
    for i in range(4):
        rom.copy_bytes(world.flavor_pointer[i], 2, 0x34B110 + (2 * i))

    rom.copy_bytes(0x202008, 0x100, 0x34B000)
    for i in range(4):
        if world.available_flavors[i] not in ["Mint flavor", "Strawberry flavor", "Banana flavor", "Peanut flavor"]:
            rom.write_bytes(flavor_address, bytearray(world.flavor_text[i]))
            flavor_addr = flavor_address - 0x3F0000
            flavor_addr = struct.pack("H", flavor_addr)
            rom.write_bytes(world.flavor_pointer[i], flavor_addr)
            rom.write_bytes(world.flavor_pointer[i] + 5, bytearray([0xFF]))
            flavor_address += len(world.flavor_text[i])
            rom.write_bytes(0x202008 + (0x40 * i), bytearray(flavor_data[world.available_flavors[i]]))
        else:
            rom.copy_bytes(vanilla_flavor_pointers[world.available_flavors[i]][1], 0x40, 0x202008 + (0x40 * i))
            rom.copy_bytes(vanilla_flavor_pointers[world.available_flavors[i]][2], 2, world.flavor_pointer[i])

    rom.write_bytes(0x048037, bytearray(world.lumine_text))
    starting_item_address = 0
    starting_psi = 0
    starting_char = 0
    starting_psi_types = []
    starting_character_count = []
    starting_inventory_pointers = {
        "Ness": 0x99F3,
        "Paula": 0x9A53,
        "Jeff": 0x9AB4,
        "Poo": 0x9B0F
    }

    starting_inv_amounts = {
        "Ness": 0x0B,
        "Paula": 0x0A,
        "Jeff": 0x08,
        "Poo": 0x0C
    }

    location = world.multiworld.get_location("Poo - Starting Item", world.player)
    if world.starting_character == "Poo" and location.item.name in item_id_table and location.item.player == world.player:
        starting_inventory_pointers["Poo"] = 0x9B10
        starting_inv_amounts["Poo"] = 0x0B
    rom.write_bytes(0x16FB66, struct.pack("H", starting_inventory_pointers[world.starting_character]))
    rom.write_bytes(0x16FB68, struct.pack("H", starting_inv_amounts[world.starting_character]))
    
    for item in world.multiworld.precollected_items[player]:
        if item.name == world.starting_character:  # Write the starting character
            rom.write_bytes(0x00B672, bytearray([world.options.starting_character.value + 1]))

        if world.options.remote_items:
            continue

        if item.name == "Photograph":
            rom.write_bytes(0x17FEA8, bytearray([0x01]))

        if item.name == "Poo" and world.multiworld.get_location("Poo - Starting Item", world.player).item.name in special_name_table and item.player == world.player:
            world.multiworld.push_precollected(world.multiworld.get_location("Poo - Starting Item", world.player).item)
        elif item.name == "Poo" and world.multiworld.get_location("Poo - Starting Item", world.player).item.name in money_item_table:
            world.starting_money += money_item_table[world.multiworld.get_location("Poo - Starting Item", world.player).item.name]

        # if item.name == "Poo" and world.multiworld.get_location("Poo - Starting Item", world.player).item.name == "Photograph":
            # rom.write_bytes(0x17FEA9, bytearray([0x01]))

        if item.name in ["Progressive Bat", "Progressive Fry Pan", "Progressive Gun", "Progressive Bracelet",
                         "Progressive Other"]:
            old_item_name = item.name
            item.name = world.progressive_item_groups[item.name][world.start_prog_counts[item.name]]
            if world.start_prog_counts[old_item_name] != len(world.progressive_item_groups[old_item_name]) - 1:
                world.start_prog_counts[old_item_name] += 1

        if item.name in item_id_table:
            rom.write_bytes(0x375000 + starting_item_address, bytearray([item_id_table[item.name]]))
            starting_item_address += 1
        elif item.name in psi_item_table:
            if item.name != "Progressive Poo PSI":
                if item.name not in starting_psi_types:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
            else:
                if starting_psi_types.count(item.name) < 2:
                    rom.write_bytes(0x17FC7C + starting_psi, bytearray([starting_psi_table[item.name]]))
                    starting_psi_types.append(item.name)
                    starting_psi += 1
        elif item.name in character_item_table and item.name != "Photograph":
            if item.name not in starting_character_count:
                rom.write_bytes(0x17FC8D + starting_char, bytearray([party_id_nums[item.name]]))
                starting_character_count.append(item.name)
                starting_char += 1
        elif item.name in money_item_table:
            world.starting_money += money_item_table[item]

    if world.options.random_battle_backgrounds:
        bpp2_bgs = [bg_id for bg_id, bpp in battle_bg_bpp.items() if bpp == 2]
        bpp4_bgs = [bg_id for bg_id, bpp in battle_bg_bpp.items() if bpp == 4]
        for i in range(483):
            world.flipped_bg = world.random.randint(0, 100)
            if i == 480:
                drawn_background = struct.pack("H", 0x00E3)
            else:
                drawn_background = struct.pack("H", world.random.randint(0x01, 0x0146))

            if battle_bg_bpp[struct.unpack("H", drawn_background)[0]] == 4:
                drawn_background_2 = struct.pack("H",  0x0000)
            else:
                drawn_background_2 = struct.pack("H", world.random.choice(bpp2_bgs))
            #print(f"ello mate we are doing background {i} at {hex(0xCBD89A + (i * 4))}, the background is {drawn_background[0]}.")
            if world.flipped_bg > 33 or drawn_background not in bpp2_bgs:
                rom.write_bytes(0x0BD89A + (i * 4), drawn_background)
                rom.write_bytes(0x0BD89C + (i * 4), drawn_background_2)
            else:
                rom.write_bytes(0x0BD89A + (i * 4), drawn_background_2)
                rom.write_bytes(0x0BD89C + (i * 4), drawn_background)

            rom.write_bytes(0x00B5F1, struct.pack("H", world.random.choice(bpp4_bgs)))

    if world.options.random_swirl_colors:
        if world.random.random() < 0.5:
            rom.write_bytes(0x02E98A, bytearray([0x7F]))  # Color math mode
            rom.write_bytes(0x02E996, bytearray([0x3F]))

        rom.write_bytes(0x300240, bytearray([world.random.randint(0x00, 0x1F)]))  # Normal swirls
        rom.write_bytes(0x300245, bytearray([world.random.randint(0x00, 0x1F)]))
        rom.write_bytes(0x30024A, bytearray([world.random.randint(0x00, 0x1F)]))

        rom.write_bytes(0x300253, bytearray([world.random.randint(0x00, 0x1F)]))  # Green swirls
        rom.write_bytes(0x300258, bytearray([world.random.randint(0x00, 0x1F)]))
        rom.write_bytes(0x30025D, bytearray([world.random.randint(0x00, 0x1F)]))

        rom.write_bytes(0x300269, bytearray([world.random.randint(0x00, 0x1F)]))  # Red swirls
        rom.write_bytes(0x30026E, bytearray([world.random.randint(0x00, 0x1F)]))
        rom.write_bytes(0x300273, bytearray([world.random.randint(0x00, 0x1F)]))

    if not world.options.prefixed_items:
        rom.write_bytes(0x15F9DC, bytearray([0x06]))
        rom.write_bytes(0x15F9DE, bytearray([0x08]))
        rom.write_bytes(0x15F9E0, bytearray([0x05]))
        rom.write_bytes(0x15F9E2, bytearray([0x0B]))
        rom.write_bytes(0x15F9E4, bytearray([0x0F]))
        rom.write_bytes(0x15F9E6, bytearray([0x10]))
        # change if necessary

    if world.options.psi_shuffle:
        write_psi(world, rom)

    world.description_pointer = 0x1000
    if world.options.armorizer:
        randomize_armor(world, rom)

    if world.options.weaponizer:
        randomize_weapons(world, rom)
    
    music_randomizer(world, rom)
    if world.options.map_palette_shuffle:
        map_palette_shuffle(world, rom)
    if world.options.randomize_psi_palettes:
        randomize_psi_palettes(world, rom)

    if world.options.randomize_enemy_attributes:
        randomize_enemy_attributes(world, rom)

    if world.options.randomize_enemy_stats:
        randomize_enemy_stats(world, rom)

    if world.options.randomize_enemy_attacks:
        randomize_enemy_attacks(world, rom)

    apply_enemy_shuffle(world, rom)
    # randomize_food(world,rom)
    write_bosses(world, rom)
    if world.options.dungeon_shuffle:
        write_dungeon_entrances(world, rom)

    world.get_all_spheres.wait()
    calculate_scaling(world)
    if world.options.shop_randomizer:
        write_shop_checks(world, rom, shop_checks)

    scale_enemies(world, rom)
    world.badge_name = badge_names[world.franklin_protection]
    world.badge_name = text_encoder(world.badge_name, 23)
    world.badge_name.extend([0x00])
    world.starting_money = min(world.starting_money, 99999)
    world.starting_money = struct.pack('<I', world.starting_money)

    rom.write_bytes(0x17FCD0, world.starting_money)
    rom.write_bytes(0x17FCE0, world.prayer_player)
    rom.write_bytes(0x17FD00, world.credits_player)
    rom.write_bytes(0x155027, world.badge_name)
    rom.write_bytes(0x17FD50, struct.pack("H", world.multiworld.players))
    rom.write_bytes(0x3FF0A0, world.world_version.encode("ascii"))
    display_version = text_encoder(world_version, 15)
    display_version.extend([0x02])
    rom.write_bytes(0x3CFFBF, display_version)

    for element in world.franklinbadge_elements:
        for address in protection_checks[element]:
            if element == world.franklin_protection:
                rom.write_bytes(address, [0xF0])
            else:
                rom.write_bytes(address, [0x80])
                # THIS WILL CRASH IF ADDRESS IS WRONG.
    rom.write_bytes(0x2EC909, struct.pack("I", protection_text[world.franklin_protection][0]))  # help text
    rom.write_bytes(0x2EC957, struct.pack("I", protection_text[world.franklin_protection][1]))  # battle text
    from Utils import __version__
    rom.name = bytearray(f'MOM2AP{__version__.replace(".", "")[0:3]}_{player}_{world.multiworld.seed:11}\0', "utf8")[:21]
    rom.name.extend([0] * (21 - len(rom.name)))
    rom.write_bytes(0x00FFC0, rom.name)

    rom.write_file("token_patch.bin", rom.get_token_binary())


class EBProcPatch(APProcedurePatch, APTokenMixin):
    hash = valid_hashes
    game = "EarthBound"
    patch_file_ending = ".apeb"
    result_file_ending = ".sfc"
    name: bytearray
    procedure = [
        ("apply_bsdiff4", ["earthbound_basepatch.bsdiff4"]),
        ("apply_tokens", ["token_patch.bin"]),
        ("repoint_vanilla_tables", [])
    ]

    @classmethod
    def get_source_data(cls) -> bytes:
        return get_base_rom_bytes()

    def write_bytes(self, offset: int, value: typing.Iterable[int]) -> None:
        self.write_token(APTokenTypes.WRITE, offset, bytes(value))
    
    def copy_bytes(self, source: int, amount: int, destination: int) -> None:
        self.write_token(APTokenTypes.COPY, destination, (amount, source))


class EBPatchExtensions(APPatchExtension):
    game = "EarthBound"

    @staticmethod
    def repoint_vanilla_tables(caller: APProcedurePatch, rom: bytes) -> bytes:
        rom = LocalRom(rom)
        version_check = rom.read_bytes(0x3FF0A0, 16)
        version_check = version_check.split(b'\x00', 1)[0]
        version_check_str = version_check.decode("ascii")
        client_version = world_version
        if client_version != version_check_str and version_check_str != "":
            raise Exception(f"Error! Patch generated on EarthBound APWorld version {version_check_str} doesn't match client version {client_version}! " +
                            f"Please use EarthBound APWorld version {version_check_str} for patching.")
        elif version_check_str == "":
            raise Exception(f"Error! Patch generated on old EarthBound APWorld version, doesn't match client version {client_version}! " +
                            f"Please verify you are using the same APWorld as the generator.")

        for action_number in range(0x013F):
            current_action = rom.read_bytes(0x157B68 + (12 * action_number), 12)
            rom.write_bytes(0x3FAFB0 + (12 * action_number), current_action)
        
        for psi_number in range(0x35):
            current_action = rom.read_bytes(0x158A50 + (15 * psi_number), 15)
            rom.write_bytes(0x350000 + (15 * psi_number), current_action)
        
        psi_text_table = rom.read_bytes(0x158D7A, (25 * 17))
        rom.write_bytes(0x3B0500, psi_text_table)

        psi_anim_config = rom.read_bytes(0x0CF04D, 0x0198)
        rom.write_bytes(0x360000, psi_anim_config)
        
        psi_anim_pointers = rom.read_bytes(0x0CF58F, 0x088)
        rom.write_bytes(0x360400, psi_anim_pointers)

        psi_anim_palettes = rom.read_bytes(0x0CF47F, 0x0110)
        rom.write_bytes(0x360600, psi_anim_palettes)

        for psi_number in range(0x32):
            psi_anim = rom.read_bytes(0x2F8583 + (0x04 * psi_number), 4)
            rom.write_bytes(0x3B0003 + (4 * psi_number), psi_anim)
            rom.write_bytes(0x3B0003, bytearray([0x4C]))
            # rom.write_bytes(0x3B0002, bytearray([0x45]))

        main_font_data = rom.read_bytes(0x210C7A, 96)
        main_font_gfx = rom.read_bytes(0x210CDA, 0x0C00)
        saturn_font_data = rom.read_bytes(0x201359, 96)
        saturn_font_gfx = rom.read_bytes(0x2013B9, 0x0C00)
        letter_n = rom.read_bytes(0x21169F, 6)
        letter_a = rom.read_bytes(0x2114FF, 6)
        letter_e = rom.read_bytes(0x21157F, 6)
        saturn_a = rom.read_bytes(0x2017DD, 9)
        saturn_n = rom.read_bytes(0x20197E, 8)
        saturn_e = rom.read_bytes(0x20185C, 24)

        accent_tilde = rom.read_bytes(0x2118A1, 2)
        saturn_tilde = rom.read_bytes(0x201F7F, 2)

        rom.write_bytes(0x3A0000, main_font_data)
        rom.write_bytes(0x3C0000, main_font_gfx)

        rom.write_bytes(0x3A0100, saturn_font_data)
        rom.write_bytes(0x3C1000, saturn_font_gfx)
        rom.write_bytes(0x3C0D25, letter_n)  # Setup n
        rom.write_bytes(0x3C0D45, letter_a)  # Setup a
        rom.write_bytes(0x3C0D65, letter_e)
        rom.write_bytes(0x3C0D22, accent_tilde)

        rom.write_bytes(0x3C1D25, saturn_n)  # Setup n
        rom.write_bytes(0x3C1D45, saturn_a)
        rom.write_bytes(0x3C1D63, saturn_e)
        rom.write_bytes(0x3C1D22, saturn_tilde)

        # ---------------------------------------
        ness_level = rom.read_bytes(0x15F5FB, 1)
        paula_level = rom.read_bytes(0x15f60f, 1)
        jeff_level = rom.read_bytes(0x15f623, 1)
        poo_level = rom.read_bytes(0x15f637, 1)

        ness_start_exp = rom.read_bytes(0x158F49 + (ness_level[0] * 4), 4)
        paula_start_exp = rom.read_bytes(0x1590D9 + (paula_level[0] * 4), 4)
        jeff_start_exp = rom.read_bytes(0x159269 + (jeff_level[0] * 4), 4)
        poo_start_exp = rom.read_bytes(0x1593F9 + (poo_level[0] * 4), 4)

        rom.write_bytes(0x17FD40, ness_start_exp)
        rom.write_bytes(0x17FD44, paula_start_exp)
        rom.write_bytes(0x17FD48, jeff_start_exp)
        rom.write_bytes(0x17FD4C, poo_start_exp)
        return rom.get_bytes()


def get_base_rom_bytes(file_name: str = "") -> bytes:
    base_rom_bytes = getattr(get_base_rom_bytes, "base_rom_bytes", None)
    if not base_rom_bytes:
        file_name = get_base_rom_path(file_name)
        base_rom_bytes = bytes(Utils.read_snes_rom(open(file_name, "rb")))

        basemd5 = hashlib.md5()
        basemd5.update(base_rom_bytes)
        if basemd5.hexdigest() not in valid_hashes:
            raise Exception('Supplied Base Rom does not match known MD5 for US(1.0) release. '
                            'Get the correct game and version, then dump it')
        get_base_rom_bytes.base_rom_bytes = base_rom_bytes
    return base_rom_bytes


def get_base_rom_path(file_name: str = "") -> str:
    options: settings.Settings = settings.get_settings()
    if not file_name:
        file_name = options["earthbound_options"]["rom_file"]
    if not os.path.exists(file_name):
        file_name = Utils.user_path(file_name)
    return file_name


# Fix hint text, I have a special idea where I can give it info on a random region
