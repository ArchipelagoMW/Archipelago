import logging
import os
import threading
import pkgutil
from typing import NamedTuple, Union, Dict, Any

import bsdiff4

import Utils
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from worlds.AutoWorld import World, WebWorld
from .Items import item_to_index, tier_1_opponents, booster_packs
from .Locations import location_to_id
from .Options import ygo06_options
from .Rom import YGO06DeltaPatch, get_base_rom_path
from worlds.generic.Rules import add_rule
from .RomValues import structure_deck_selection


class Yugioh06Web(WebWorld):
    theme = "stone"
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up Yu-Gi-Oh! - Ultimate Masters Edition - World Championship Tournament 2006"
        "for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rensen"]
    )

    tutorials = [setup]


class Yugioh06World(World):
    """

    """
    game = "Yu-Gi-Oh! 2006"
    data_version = 1
    web = Yugioh06Web()
    option_definitions = ygo06_options

    item_name_to_id = {}
    start_id = 5730000
    for k, v in item_to_index.items():
        item_name_to_id[k] = v + start_id

    location_name_to_id = {}
    start_id = 5730000
    for k, v in location_to_id.items():
        location_name_to_id[k] = v + start_id

    def create_item(self, name: str) -> Item:
        return Item(name, ItemClassification.progression, self.item_name_to_id[name], self.player)

    def create_items(self):
        start_inventory = self.multiworld.start_inventory[self.player].value.copy()
        item_pool = []
        for name in item_to_index:
            if name == "Remote" or name == "Money" or name in start_inventory:
                continue
            item = Yugioh2006Item(
                name,
                ItemClassification.progression,
                self.item_name_to_id[name],
                self.player
            )
            item_pool.append(item)

        while len(item_pool) < len(location_to_id):
            item = Yugioh2006Item(
                "Money",
                ItemClassification.filler,
                self.item_name_to_id["Money"],
                self.player
            )
            item_pool.append(item)
        self.multiworld.itempool += item_pool

    def create_regions(self):
        self.multiworld.regions += [
            create_region(self.multiworld, self.player, 'Menu', None, ['to Campaign']),
            create_region(self.multiworld, self.player, 'Campaign', self.location_name_to_id)
        ]

        self.multiworld.get_entrance('to Campaign', self.player)\
            .connect(self.multiworld.get_region('Campaign', self.player))

    def generate_early(self):
        starting_opponent = self.multiworld.random.choice(tier_1_opponents)
        self.multiworld.start_inventory[self.player].value[starting_opponent] = 1
        starting_pack = self.multiworld.random.choice(booster_packs)
        self.multiworld.start_inventory[self.player].value[starting_pack] = 1
        self.multiworld.start_inventory[self.player].value['Banlist September 2005'] = 1

    def apply_base_path(self, rom):
        base_patch_location = os.path.dirname(__file__) + "/patch.bsdiff4"
        with open(base_patch_location, "rb") as base_patch:
            rom_data = bsdiff4.patch(rom.read(), base_patch.read())
        rom_data = bytearray(rom_data)
        return rom_data

    def apply_randomizer(self):
        with open(get_base_rom_path(), 'rb') as rom:
            rom_data = self.apply_base_path(rom)

        structure_deck = self.multiworld.StructureDeck[self.player]
        structure_deck_data_location = 0x000fd0aa
        rom_data[structure_deck_data_location] = structure_deck_selection.get(structure_deck.value)
        randomizer_data_start = 0x0000f310
        for location in self.multiworld.get_filled_locations(self.player):
            item = location.item.name
            if location.item.player != self.player:
                item = "Remote"
            item_id = item_to_index[item]
            location_id = location_to_id[location.name]
            rom_data[randomizer_data_start + location_id] = item_id
        return rom_data

    def generate_output(self, output_directory: str):
        patched_rom = self.apply_randomizer()
        outfilebase = 'AP_' + self.multiworld.seed_name
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        outputFilename = os.path.join(output_directory, f'{outfilebase}{outfilepname}.gba')
        self.rom_name_text = f'YGO06{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}\0'
        self.romName = bytearray(self.rom_name_text, 'utf8')[:0x20]
        self.romName.extend([0] * (0x20 - len(self.romName)))
        self.rom_name = self.romName
        patched_rom[0x10:0x30] = self.romName
        self.playerName = bytearray(self.multiworld.player_name[self.player], 'utf8')[:0x20]
        self.playerName.extend([0] * (0x20 - len(self.playerName)))
        patched_rom[0x30:0x50] = self.playerName
        patched_filename = os.path.join(output_directory, outputFilename)
        with open(patched_filename, 'wb') as patched_rom_file:
            patched_rom_file.write(patched_rom)
        patch = YGO06DeltaPatch(os.path.splitext(outputFilename)[0] + YGO06DeltaPatch.patch_file_ending,
                                player=self.player,
                                player_name=self.multiworld.player_name[self.player],
                                patched_path=outputFilename)
        patch.write()
        os.unlink(patched_filename)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    region = Region(name, player, world)
    if locations:
        for location_name in locations.keys():
            location = Yugioh2006Location(player, location_name, locations[location_name], region)
            region.locations.append(location)

    if exits:
        for _exit in exits:
            region.exits.append(Entrance(player, _exit, region))

    return region


class Yugioh2006Item(Item):
    game = "Yu-Gi-Oh! 2006"


class Yugioh2006Location(Location):
    game: str = "Yu-Gi-Oh! 2006"
