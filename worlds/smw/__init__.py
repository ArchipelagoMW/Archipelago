import dataclasses
import os
import typing
import math
import settings
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SMWItem, ItemData, item_table, junk_table
from .Locations import SMWLocation, all_locations, setup_locations, special_zone_level_names, special_zone_dragon_coin_names, special_zone_hidden_1up_names, special_zone_blocksanity_names
from .Options import SMWOptions
from .Regions import create_regions, connect_regions
from .Levels import full_level_list, generate_level_list, location_id_to_level_id
from .Rules import set_rules
from worlds.generic.Rules import add_rule, exclusion_rules
from .Names import ItemName, LocationName
from .Client import SMWSNIClient
from worlds.AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, SMWDeltaPatch


class SMWSettings(settings.Group):
    class RomFile(settings.SNESRomPath):
        """File name of the SMW US rom"""
        description = "Super Mario World (USA) ROM File"
        copy_to = "Super Mario World (USA).sfc"
        md5s = [SMWDeltaPatch.hash]

    rom_file: RomFile = RomFile(RomFile.copy_to)


class SMWWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Super Mario World randomizer connected to an Archipelago Multiworld.",
        "English",
        "setup_en.md",
        "setup/en",
        ["PoryGone"]
    )
    
    tutorials = [setup_en]


class SMWWorld(World):
    """
    Super Mario World is an action platforming game.
    The Princess has been kidnapped by Bowser again, but Mario has somehow
    lost all of his abilities. Can he get them back in time to save the Princess?
    """
    game: str = "Super Mario World"

    settings: typing.ClassVar[SMWSettings]

    options_dataclass = SMWOptions
    options: SMWOptions

    topology_present = False
    required_client_version = (0, 4, 5)

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_dict: typing.Dict[int,int]
    web = SMWWeb()
    
    def __init__(self, multiworld: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(multiworld, player)

    @classmethod
    def stage_assert_generate(cls, multiworld: MultiWorld):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def fill_slot_data(self) -> dict:
        slot_data = self.options.as_dict(
            "dragon_coin_checks",
            "moon_checks",
            "hidden_1up_checks",
            "bonus_block_checks",
            "blocksanity",
        )
        slot_data["active_levels"] = self.active_level_dict

        return slot_data

    def generate_early(self):
        if self.options.early_climb:
            self.multiworld.local_early_items[self.player][ItemName.mario_climb] = 1

    def create_regions(self):
        location_table = setup_locations(self)
        create_regions(self, location_table)

        # Not generate basic
        itempool: typing.List[SMWItem] = []

        self.active_level_dict = dict(zip(generate_level_list(self), full_level_list))
        self.topology_present = self.options.level_shuffle

        connect_regions(self, self.active_level_dict)

        # Add Boss Token amount requirements for Worlds
        add_rule(self.multiworld.get_region(LocationName.donut_plains_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 1))
        add_rule(self.multiworld.get_region(LocationName.vanilla_dome_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 2))
        add_rule(self.multiworld.get_region(LocationName.forest_of_illusion_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 4))
        add_rule(self.multiworld.get_region(LocationName.chocolate_island_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 5))
        add_rule(self.multiworld.get_region(LocationName.valley_of_bowser_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 6))

        exclusion_pool = set()
        if self.options.exclude_special_zone:
            exclusion_pool.update(special_zone_level_names)
            if self.options.dragon_coin_checks:
                exclusion_pool.update(special_zone_dragon_coin_names)
            if self.options.hidden_1up_checks:
                exclusion_pool.update(special_zone_hidden_1up_names)
            if self.options.blocksanity:
                exclusion_pool.update(special_zone_blocksanity_names)

            exclusion_rules(self.multiworld, self.player, exclusion_pool)

        total_required_locations = 96
        if self.options.dragon_coin_checks:
            total_required_locations += 49
        if self.options.moon_checks:
            total_required_locations += 7
        if self.options.hidden_1up_checks:
            total_required_locations += 14
        if self.options.bonus_block_checks:
            total_required_locations += 4
        if self.options.blocksanity:
            total_required_locations += 582

        itempool += [self.create_item(ItemName.mario_run)]
        itempool += [self.create_item(ItemName.mario_carry)]
        itempool += [self.create_item(ItemName.mario_swim)]
        itempool += [self.create_item(ItemName.mario_spin_jump)]
        itempool += [self.create_item(ItemName.mario_climb)]
        itempool += [self.create_item(ItemName.yoshi_activate)]
        itempool += [self.create_item(ItemName.p_switch)]
        itempool += [self.create_item(ItemName.p_balloon)]
        itempool += [self.create_item(ItemName.super_star_active)]
        itempool += [self.create_item(ItemName.progressive_powerup) for _ in range(3)]
        itempool += [self.create_item(ItemName.yellow_switch_palace)]
        itempool += [self.create_item(ItemName.green_switch_palace)]
        itempool += [self.create_item(ItemName.red_switch_palace)]
        itempool += [self.create_item(ItemName.blue_switch_palace)]
        itempool += [self.create_item(ItemName.special_world_clear)]
        
        if self.options.goal == "yoshi_egg_hunt":
            raw_egg_count = total_required_locations - len(itempool) - len(exclusion_pool)
            total_egg_count = min(raw_egg_count, self.options.max_yoshi_egg_cap.value)
            self.required_egg_count = max(math.floor(total_egg_count * (self.options.percentage_of_yoshi_eggs.value / 100.0)), 1)
            extra_egg_count = total_egg_count - self.required_egg_count
            removed_egg_count = math.floor(extra_egg_count * (self.options.junk_fill_percentage.value / 100.0))
            self.actual_egg_count = total_egg_count - removed_egg_count

            itempool += [self.create_item(ItemName.yoshi_egg) for _ in range(self.actual_egg_count)]

            self.multiworld.get_location(LocationName.yoshis_house, self.player).place_locked_item(self.create_item(ItemName.victory))
        else:
            self.actual_egg_count = 0
            self.required_egg_count = 0

            self.multiworld.get_location(LocationName.bowser, self.player).place_locked_item(self.create_item(ItemName.victory))

        junk_count = total_required_locations - len(itempool)
        trap_weights = []
        trap_weights += ([ItemName.ice_trap] * self.options.ice_trap_weight.value)
        trap_weights += ([ItemName.stun_trap] * self.options.stun_trap_weight.value)
        trap_weights += ([ItemName.literature_trap] * self.options.literature_trap_weight.value)
        trap_weights += ([ItemName.timer_trap] * self.options.timer_trap_weight.value)
        trap_weights += ([ItemName.reverse_controls_trap] * self.options.reverse_trap_weight.value)
        trap_weights += ([ItemName.thwimp_trap] * self.options.thwimp_trap_weight.value)
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.options.trap_fill_percentage.value / 100.0))
        junk_count -= trap_count

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.random.choice(trap_weights)
            trap_pool.append(self.create_item(trap_item))

        itempool += trap_pool

        junk_weights = []
        junk_weights += ([ItemName.one_coin] * 15)
        junk_weights += ([ItemName.five_coins] * 15)
        junk_weights += ([ItemName.ten_coins] * 25)
        junk_weights += ([ItemName.fifty_coins] * 25)
        junk_weights += ([ItemName.one_up_mushroom] * 20)

        junk_pool = [self.create_item(self.random.choice(junk_weights)) for _ in range(junk_count)]
        
        itempool += junk_pool

        boss_location_names = [LocationName.yoshis_island_koopaling, LocationName.donut_plains_koopaling, LocationName.vanilla_dome_koopaling,
                               LocationName.twin_bridges_koopaling, LocationName.forest_koopaling, LocationName.chocolate_koopaling,
                               LocationName.valley_koopaling, LocationName.vanilla_reznor, LocationName.forest_reznor, LocationName.chocolate_reznor, LocationName.valley_reznor]

        for location_name in boss_location_names:
            self.multiworld.get_location(location_name, self.player).place_locked_item(self.create_item(ItemName.koopaling))

        self.multiworld.itempool += itempool


    def generate_output(self, output_directory: str):
        rompath = ""  # if variable is not declared finally clause may fail
        try:
            multiworld = self.multiworld
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(self, rom, self.player, self.active_level_dict)

            rompath = os.path.join(output_directory, f"{self.multiworld.get_out_file_name_base(self.player)}.sfc")
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = SMWDeltaPatch(os.path.splitext(rompath)[0]+SMWDeltaPatch.patch_file_ending, player=player,
                                  player_name=multiworld.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            self.rom_name_available_event.set()  # make sure threading continues and errors are collected
            if os.path.exists(rompath):
                os.unlink(rompath)

    def modify_multidata(self, multidata: dict):
        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.multiworld.player_name[self.player]]

    def extend_hint_information(self, hint_data: typing.Dict[int, typing.Dict[int, str]]):
        if self.topology_present:
            world_names = [
                LocationName.yoshis_island_region,
                LocationName.donut_plains_region,
                LocationName.vanilla_dome_region,
                LocationName.twin_bridges_region,
                LocationName.forest_of_illusion_region,
                LocationName.chocolate_island_region,
                LocationName.valley_of_bowser_region,
                LocationName.star_road_region,
                LocationName.special_zone_region,
            ]
            world_cutoffs = [
                0x07,
                0x13,
                0x1F,
                0x26,
                0x30,
                0x39,
                0x44,
                0x4F,
                0x59
            ]
            er_hint_data = {}
            for loc_name, level_data in location_id_to_level_id.items():
                level_id = level_data[0]

                if level_id not in self.active_level_dict:
                    continue

                keys_list = list(self.active_level_dict.keys())
                level_index = keys_list.index(level_id)
                for i in range(len(world_cutoffs)):
                    if level_index >= world_cutoffs[i]:
                        continue

                    if not self.options.dragon_coin_checks and "Dragon Coins" in loc_name:
                        continue
                    if not self.options.moon_checks and "3-Up Moon" in loc_name:
                        continue
                    if not self.options.hidden_1up_checks and "Hidden 1-Up" in loc_name:
                        continue
                    if not self.options.bonus_block_checks and "1-Up from Bonus Block" in loc_name:
                        continue
                    if not self.options.blocksanity and "Block #" in loc_name:
                        continue

                    location = self.multiworld.get_location(loc_name, self.player)
                    er_hint_data[location.address] = world_names[i]
                    break

            hint_data[self.player] = er_hint_data

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif name == ItemName.yoshi_egg:
            classification = ItemClassification.progression_skip_balancing
        elif data.progression:
            classification = ItemClassification.progression
        elif data.trap:
            classification = ItemClassification.trap
        else:
            classification = ItemClassification.filler

        created_item = SMWItem(name, classification, data.code, self.player)

        return created_item

    def get_filler_item_name(self) -> str:
        return self.random.choice(list(junk_table.keys()))

    def set_rules(self):
        set_rules(self)
