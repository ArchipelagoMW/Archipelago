import os
import typing
import math
import threading

from BaseClasses import Item, MultiWorld, Tutorial, ItemClassification
from .Items import SMWItem, ItemData, item_table
from .Locations import SMWLocation, all_locations, setup_locations
from .Options import smw_options
from .Regions import create_regions, connect_regions
from .Levels import full_level_list, generate_level_list
from .Rules import set_rules
from ..generic.Rules import add_rule
from .Names import ItemName, LocationName
from ..AutoWorld import WebWorld, World
from .Rom import LocalRom, patch_rom, get_base_rom_path, SMWDeltaPatch
import Patch


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
    options = smw_options
    topology_present = False
    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    active_level_dict: typing.Dict[int,int]
    web = SMWWeb()
    
    def __init__(self, world: MultiWorld, player: int):
        self.rom_name_available_event = threading.Event()
        super().__init__(world, player)

    @classmethod
    def stage_assert_generate(cls, world):
        rom_file = get_base_rom_path()
        if not os.path.exists(rom_file):
            raise FileNotFoundError(rom_file)

    def _get_slot_data(self):
        return {
            #"death_link": self.world.death_link[self.player].value,
            "active_levels": self.active_level_dict,
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in smw_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[SMWItem] = []

        if self.world.level_shuffle[self.player]:
            self.active_level_dict = dict(zip(generate_level_list(self.world), full_level_list))
            self.topology_present = True
        else:
            # SMW_TODO: Make Back Door -> Front 
            self.active_level_dict = dict(zip(full_level_list, full_level_list))

        connect_regions(self.world, self.player, self.active_level_dict)
        
        # Add Boss Token amount requirements for Worlds
        add_rule(self.world.get_region(LocationName.donut_plains_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 1))
        add_rule(self.world.get_region(LocationName.vanilla_dome_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 2))
        add_rule(self.world.get_region(LocationName.forest_of_illusion_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 4))
        add_rule(self.world.get_region(LocationName.chocolate_island_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 5))
        add_rule(self.world.get_region(LocationName.valley_of_bowser_1_tile, self.player).entrances[0], lambda state: state.has(ItemName.koopaling, self.player, 6))

        total_required_locations = 96
        if self.world.dragon_coin_checks[self.player]:
            total_required_locations += 49

        itempool += [self.create_item(ItemName.mario_run)]
        itempool += [self.create_item(ItemName.mario_carry)]
        itempool += [self.create_item(ItemName.mario_swim)]
        itempool += [self.create_item(ItemName.mario_spin_jump)]
        itempool += [self.create_item(ItemName.mario_climb)]
        itempool += [self.create_item(ItemName.yoshi_activate)]
        itempool += [self.create_item(ItemName.p_switch)]
        itempool += [self.create_item(ItemName.p_balloon)]
        itempool += [self.create_item(ItemName.super_star_active)]
        itempool += [self.create_item(ItemName.progressive_powerup)] * 3
        itempool += [self.create_item(ItemName.yellow_switch_palace)]
        itempool += [self.create_item(ItemName.green_switch_palace)]
        itempool += [self.create_item(ItemName.red_switch_palace)]
        itempool += [self.create_item(ItemName.blue_switch_palace)]
        
        if self.world.goal[self.player] == "yoshi_egg_hunt":
            itempool += [self.create_item(ItemName.yoshi_egg)] * self.world.number_of_yoshi_eggs[self.player]
            self.world.get_location(LocationName.yoshis_house, self.player).place_locked_item(self.create_item(ItemName.victory))
        else:
            self.world.get_location(LocationName.bowser, self.player).place_locked_item(self.create_item(ItemName.victory))

        junk_count = total_required_locations - len(itempool)
        trap_weights = []
        trap_weights += ([ItemName.ice_trap] * self.world.ice_trap_weight[self.player].value)
        trap_weights += ([ItemName.stun_trap] * self.world.stun_trap_weight[self.player].value)
        trap_weights += ([ItemName.literature_trap] * self.world.literature_trap_weight[self.player].value)
        trap_count = 0 if (len(trap_weights) == 0) else math.ceil(junk_count * (self.world.trap_fill_percentage[self.player].value / 100.0))
        junk_count -= trap_count

        trap_pool = []
        for i in range(trap_count):
            trap_item = self.world.random.choice(trap_weights)
            trap_pool += [self.create_item(trap_item)]

        itempool += trap_pool

        itempool += [self.create_item(ItemName.one_up_mushroom)] * junk_count

        self.world.get_location(LocationName.yoshis_island_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.donut_plains_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.vanilla_dome_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.twin_bridges_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.forest_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.chocolate_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.valley_koopaling, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.vanilla_reznor, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.forest_reznor, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.chocolate_reznor, self.player).place_locked_item(self.create_item(ItemName.koopaling))
        self.world.get_location(LocationName.valley_reznor, self.player).place_locked_item(self.create_item(ItemName.koopaling))

        self.world.itempool += itempool


    def generate_output(self, output_directory: str):
        try:
            world = self.world
            player = self.player

            rom = LocalRom(get_base_rom_path())
            patch_rom(self.world, rom, self.player, self.active_level_dict)

            outfilepname = f'_P{player}'
            outfilepname += f"_{world.player_name[player].replace(' ', '_')}" \
                if world.player_name[player] != 'Player%d' % player else ''

            rompath = os.path.join(output_directory, f'AP_{world.seed_name}{outfilepname}.sfc')
            rom.write_to_file(rompath)
            self.rom_name = rom.name

            patch = SMWDeltaPatch(os.path.splitext(rompath)[0]+SMWDeltaPatch.patch_file_ending, player=player,
                                  player_name=world.player_name[player], patched_path=rompath)
            patch.write()
        except:
            raise
        finally:
            if os.path.exists(rompath):
                os.unlink(rompath)
            self.rom_name_available_event.set() # make sure threading continues and errors are collected

    def modify_multidata(self, multidata: dict):
        return

        import base64
        # wait for self.rom_name to be available.
        self.rom_name_available_event.wait()
        rom_name = getattr(self, "rom_name", None)
        # we skip in case of error, so that the original error in the output thread is the one that gets raised
        if rom_name:
            new_name = base64.b64encode(bytes(self.rom_name)).decode()
            multidata["connect_names"][new_name] = multidata["connect_names"][self.world.player_name[self.player]]

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
            er_hint_data = {}
            for world_index in range(len(world_names)):
                for level_index in range(5):
                    level_region = self.world.get_region(self.active_level_dict[world_index * 5 + level_index], self.player)
                    for location in level_region.locations:
                        er_hint_data[location.address] = world_names[world_index]
            multidata['er_hint_data'][self.player] = er_hint_data

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str, force_non_progression=False) -> Item:
        data = item_table[name]

        if force_non_progression:
            classification = ItemClassification.filler
        elif data.progression:
            classification = ItemClassification.progression
        else:
            classification = ItemClassification.filler

        created_item = SMWItem(name, classification, data.code, self.player)

        return created_item

    def set_rules(self):
        set_rules(self.world, self.player)
