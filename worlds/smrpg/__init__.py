import logging
import os
import random
import threading
import typing
from copy import deepcopy
from typing import NamedTuple, Union, Dict, Any

import bsdiff4

import Utils
import settings
from BaseClasses import Item, Location, Region, Entrance, MultiWorld, ItemClassification, Tutorial
from .Items import item_table
from .Locations import location_table, SMRPGRegions
from .Client import SMRPGClient
from .Options import SMRPGOptions, build_flag_string
from worlds.AutoWorld import World, WebWorld
from worlds.generic.Rules import add_rule, add_item_rule
from .Rom import get_base_rom_path, SMRPGDeltaPatch

from .smrpg_web_randomizer.randomizer.management.commands import make_seed

class SMRPGSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SMRPG US rom"""
        description = "Super Mario RPG (USA) ROM File"
        copy_to = "Super Mario RPG - Legend of the Seven Stars (USA).sfc"
        md5s = [SMRPGDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)

class SMRPGWeb(WebWorld):
    theme = "ice"
    setup = Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up Super Mario RPG for Archipelago on your computer.",
        "English",
        "multiworld_en.md",
        "multiworld/en",
        ["Rosalie"]
    )

    tutorials = [setup]


class SMRPGWorld(World):
    """
    Croakacola
    """
    options_dataclass = SMRPGOptions
    options: SMRPGOptions
    game = "Super Mario RPG Legend of the Seven Stars"
    is_experimental = True
    topology_present = False
    settings: typing.ClassVar[SMRPGSettings]
    data_version = 1
    base_id = 850000
    web = SMRPGWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: location.id for name, location in location_table.items()}

    item_name_groups = {
        "bosses": {"Defeated!", "Star Piece"}
    }

    for k, v in item_name_to_id.items():
        item_name_to_id[k] = v + base_id

    for k, v in location_name_to_id.items():
        if v != None:
            location_name_to_id[k] = v + base_id

    def __init__(self, world: MultiWorld, player: int):
        super().__init__(world, player)
        self.rom_name = None
        self.generator_in_use = threading.Event()
        self.rom_name_text = ""
        self.rom_name_available_event = threading.Event()
        self.levels = None

    def create_item(self, name: str):
        return SMRPGItem(name, item_table[name].classification, self.item_name_to_id[name], self.player)

    def create_event(self, event: str):
        return SMRPGItem(event, ItemClassification.progression, None, self.player)

    def create_location(self, name, id, parent, event=False):
        return_location = SMRPGLocation(self.player, name, id, parent)
        return_location.event = event
        return return_location

    @classmethod
    def stage_assert_generate(cls, _: "MultiWorld") -> None:
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def create_regions(self):
        menu = Region("Menu", self.player, self.multiworld)
        overworld = Region("Overworld", self.player, self.multiworld)
        for key, location in location_table.items():
            try:
                region = self.multiworld.get_region(location.region.name, self.player)
            except KeyError:
                region = Region(location.region.name, self.player, self.multiworld)
                new_entrance = Entrance(self.player, location.region.name, overworld)
                new_entrance.connect(region)
                overworld.exits.append(new_entrance)
                self.multiworld.regions.append(region)
            location = self.create_location(location.name, self.location_name_to_id[location.name], region)
            region.locations.append(location)
        begin_game = Entrance(self.player, "Begin Game", menu)
        menu.exits.append(begin_game)
        begin_game.connect(overworld)
        self.multiworld.regions.append(menu)
        self.multiworld.regions.append(overworld)

    def set_rules(self):
        for key, location in location_table.items():
            if location.region == SMRPGRegions.moleville_mines_back:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has("Bambino Bomb", self.player))
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name != "Bambino Bomb")

            if location.region == SMRPGRegions.nimbus_castle_middle:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has("Castle Key 1", self.player))
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name != "Castle Key 1")

            if location.region == SMRPGRegions.nimbus_castle_back:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has("Castle Key 1", self.player)
                                       and state.has("Castle Key 2", self.player))
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name not in {"Castle Key 1", "Castle Key 2"})

            if location.region in Locations.world_two_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 2))
            if location.region in Locations.world_three_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 4))
            if location.region in Locations.world_four_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 6))
            if location.region in Locations.world_five_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 9))
            if location.region in Locations.world_six_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 12))
            if location.region in Locations.world_seven_regions:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has_group("bosses", self.player, 15))

            if key in Locations.additional_bambino_locks:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has("Bambino Bomb", self.player))
            star_pieces = 6
            if self.options.StarPieceGoal == Options.StarPieceGoal.option_seven:
                star_pieces = 7
            if location.region == SMRPGRegions.factory:
                add_rule(self.multiworld.get_location(key, self.player),
                         lambda state: state.has("Star Piece", self.player, star_pieces))
            if location.region == SMRPGRegions.bowsers_keep:
                if self.options.StarPiecesInBowsersKeep == Options.StarPiecesInBowsersKeep.option_false:
                    add_rule(self.multiworld.get_location(key, self.player),
                             lambda state: state.has("Star Piece", self.player, star_pieces))

            if key in Locations.no_key_locations:
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name not in Items.key_items)

            if key in Locations.no_coin_locations:
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name not in Items.coin_rewards)

            if key in Locations.no_reward_locations:
                print(key)
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.name not in Items.chest_rewards)

            if key in Locations.missable_locations:
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.classification != ItemClassification.progression)

            if key in Locations.culex_locations \
                    and self.options.IncludeCulex == Options.IncludeCulex.option_false:
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.classification != ItemClassification.progression)

            if key in Locations.super_jump_locations \
                    and self.options.SuperJumpsInLogic == Options.SuperJumpsInLogic.option_false:
                add_item_rule(self.multiworld.get_location(key, self.player),
                              lambda item: item.classification != ItemClassification.progression)

            add_item_rule(self.multiworld.get_location(key, self.player),
                          lambda item: item.name not in Items.boss_items)
        for key, locations in Locations.key_item_locations.items():
            for location in locations:
                add_rule(self.multiworld.get_location(location, self.player),
                         lambda state: state.has(key, self.player))
        for index, location2 in enumerate(Locations.bowsers_keep_doors):
            if index < self.options.BowsersKeepDoors:
                add_item_rule(self.multiworld.get_location(location2, self.player),
                              lambda item: item.classification != ItemClassification.progression)

    def generate_basic(self):
        boss_locations = set(deepcopy(Locations.star_piece_locations))
        boss_locations = [x[0] for x in boss_locations]
        bad_boss_locations = set(deepcopy(Locations.force_defeated_locations))
        bad_boss_locations = [x[0] for x in bad_boss_locations]

        exclude_keep = False
        exclude_factory = True
        if self.options.StarPiecesInBowsersKeep == Options.StarPiecesInBowsersKeep.option_false:
            exclude_keep = True

        star_pieces = 6
        if self.options.StarPieceGoal == Options.StarPieceGoal.option_seven:
            star_pieces = 7

        if exclude_factory:
            boss_locations = [x for x in boss_locations if x not in Locations.factory_bosses]
        if exclude_keep:
            boss_locations = [x for x in boss_locations if x not in Locations.keep_bosses]
        if self.options.IncludeCulex == Options.IncludeCulex.option_false:
            boss_locations = [x for x in boss_locations if x not in Locations.culex_locations]

        star_piece_targets = self.multiworld.random.sample(
            [x for x in boss_locations if x not in bad_boss_locations],
            star_pieces
        )
        for location in boss_locations:
            if location in star_piece_targets:
                self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item("Star Piece"))
            else:
                self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item("Defeated!")
                )
        boss_locations = deepcopy(Locations.star_piece_locations)
        boss_locations = [x[0] for x in boss_locations]

        if exclude_keep:
            for location in boss_locations:
                if Locations.location_table[location].region == Locations.SMRPGRegions.bowsers_keep:
                    self.multiworld.get_location(location, self.player).place_locked_item(
                        self.create_item("Defeated!")
                    )
        if exclude_factory:
            for location in boss_locations:
                if Locations.location_table[location].region == Locations.SMRPGRegions.factory:
                    self.multiworld.get_location(location, self.player).place_locked_item(
                        self.create_item("Defeated!")
                    )
        if self.options.IncludeCulex == Options.IncludeCulex.option_false:
            for location in boss_locations:
                if location in Locations.culex_locations:
                    self.multiworld.get_location(location, self.player).place_locked_item(
                        self.create_item("Defeated!")
                    )

        star_locations = deepcopy(Locations.star_allowed_locations)
        stars = self.multiworld.random.sample(star_locations, 9)
        for location in star_locations:
            if location in stars:
                self.multiworld.get_location(location, self.player).place_locked_item(
                    self.create_item("Invincibility Star")
                )

        smithy = self.multiworld.get_location("Boss - Smithy Spot", self.player)
        smithy.place_locked_item(self.create_item("Star Road Restored!"))
        self.multiworld.completion_condition[self.player] = lambda state: state.has("Star Road Restored!", self.player)

        unfilled_boxes = [
            x for x in self.multiworld.get_unfilled_locations(self.player)
            if x.name not in Locations.no_reward_locations
        ]
        self.multiworld.random.choice(unfilled_boxes).place_locked_item(self.create_item("You Missed!"))

    def create_items(self):
        if self.options.ItemPool == Options.ItemPool.option_vanilla:
            for item, amount in Items.original_item_list.items():
                for i in range(amount):
                    self.multiworld.itempool.append(self.create_item(item))
        if self.options.ItemPool == Options.ItemPool.option_shuffled_types:
            for item, amount in Items.original_item_list.items():
                for i in range(amount):
                    self.multiworld.itempool.append(self.create_item(self.randomize_item_in_type(item)))
        if self.options.ItemPool == Options.ItemPool.option_shuffled_inventories:
            for item, amount in Items.original_item_list.items():
                for i in range(amount):
                    self.multiworld.itempool.append(self.create_item(self.randomize_item_in_inventory(item)))
        if self.options.ItemPool == Options.ItemPool.option_chaotic:
            for item, amount in Items.original_item_list.items():
                if item not in Items.singleton_items:
                    for i in range(amount):
                        self.multiworld.itempool.append(
                            self.create_item(self.multiworld.random.choice(Items.all_mundane_items)))
                else:
                    for i in range(amount):
                        self.multiworld.itempool.append(self.create_item(item))

    def randomize_item_in_type(self, item: str):
        item_type = None
        if item in Items.consumables:
            item_type = Items.consumables
        if item in Items.chest_rewards:
            item_type = Items.chest_rewards
        if item in Items.weapons:
            item_type = Items.weapons
        if item in Items.armor:
            item_type = Items.armor
        if item in Items.accessories:
            item_type = Items.accessories
        if item in Items.key_items:
            item_type = Items.key_items
        if item_type == None:
            if item in Items.singleton_items:
                return item
            else:
                print(item)
                raise ValueError(f"{item} is a problem. Fix this.")
        if item_type == Items.key_items:
            return item # We're not randomizing key items
        return random.choice(item_type)

    def randomize_item_in_inventory(self, item: str):
        item_type = None
        if item in Items.filler:
            item_type = Items.filler
        if item in Items.equipment:
            item_type = Items.equipment
        if item in Items.key_items:
            item_type = Items.key_items
        if item_type == None:
            if item in Items.singleton_items:
                return item
            else:
                print(item)
                raise ValueError(f"{item} is a problem. Fix this.")
        if item_type == Items.key_items:
            return item # We're not randomizing key items
        return random.choice(item_type)


    def generate_output(self, output_directory: str):
        self.rom_name_text = f'MRPG{Utils.__version__.replace(".", "")[0:3]}_{self.player}_{self.multiworld.seed:11}'
        self.rom_name_text = self.rom_name_text[:20]
        self.rom_name = bytearray(self.rom_name_text, 'utf-8')
        self.rom_name.extend([0] * (20 - len(self.rom_name)))
        output = dict()
        outfilebase = 'AP_' + self.multiworld.seed_name
        outfilepname = f'_P{self.player}'
        outfilepname += f"_{self.multiworld.get_file_safe_player_name(self.player).replace(' ', '_')}"
        output_file = os.path.join(output_directory, f'{outfilebase}{outfilepname}.sfc')
        for key, location in location_table.items():
            item = self.multiworld.get_location(location.name, self.player).item
            rando_name = item_table[item.name].rando_name if item.player == self.player else "ArchipelagoItem"
            output[location.rando_name] = rando_name
        make_seed.Command().handle(
            mode="open",
            flags = build_flag_string(self.options.as_dict(*list(SMRPGOptions.__annotations__.keys()))),
            seed=((self.multiworld.seed % 2 ** 32) + self.player),
            rom=SMRPGWorld.settings.rom_file,
            output_file=output_file,
            ap_data=output,
            rom_name=self.rom_name
        )
        patch = SMRPGDeltaPatch(os.path.splitext(output_file)[0] + SMRPGDeltaPatch.patch_file_ending,
                                player=self.player,
                                player_name=self.multiworld.player_name[self.player],
                                patched_path=output_file)
        patch.write()
        os.unlink(output_file)
        os.unlink(output_file + ".spoiler")

    def modify_multidata(self, multidata: dict):
        import base64
        rom_name = getattr(self, "rom_name", None)
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def get_filler_item_name(self) -> str:
        filler_items = [item for item in item_table if item_table[item].classification == ItemClassification.filler]
        return self.multiworld.random.choice(filler_items)


class SMRPGItem(Item):
    game = 'Super Mario RPG'


class SMRPGLocation(Location):
    game = 'Super Mario RPG'
