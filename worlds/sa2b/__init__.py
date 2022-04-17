import os
import typing
import math

from BaseClasses import Item, MultiWorld
from .Items import SA2BItem, ItemData, item_table, upgrades_table
from .Locations import SA2BLocation, all_locations, setup_locations
from .Options import sa2b_options
from .Regions import create_regions, shuffleable_regions, connect_regions
from .Rules import set_rules
from .Names import ItemName
from ..AutoWorld import World
import Patch


class SA2BWorld(World):
    """
    J.R.R. Tolkien's The Lord of the Rings, Vol. 1 is an SNES Action-RPG brought to you by the minds that would
    eventually bring you the original Fallout. Embark on Frodo's legendary journey to destroy the One Ring and 
    rid Middle-Earth of the shadow of the Dark Lord Sauron forever.
    """
    game: str = "Sonic Adventure 2 Battle"
    options = sa2b_options
    topology_present = False
    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = all_locations

    music_map: typing.Dict[int, int]
    emblems_for_cannons_core: int
    region_emblem_map: typing.Dict[int, int]

    def _get_slot_data(self):
        return {
            "MusicMap":                             self.music_map,
            "MusicShuffle":                         self.world.MusicShuffle[self.player],
            "DeathLink":                            self.world.DeathLink[self.player],
            "IncludeMissions":                      self.world.IncludeMissions[self.player],
            "EmblemPercentageForCannonsCore":       self.world.EmblemPercentageForCannonsCore[self.player],
            "NumberOfLevelGates":                   self.world.NumberOfLevelGates[self.player],
            "LevelGateDistribution":                self.world.LevelGateDistribution[self.player],
            "EmblemsForCannonsCore":                self.emblems_for_cannons_core,
            "RegionEmblemMap":                      self.region_emblem_map,
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def get_required_client_version(self) -> typing.Tuple[int, int, int]:
        return max((0, 2, 5), super(SA2BWorld, self).get_required_client_version())

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        slot_data["MusicMap"] = self.music_map
        for option_name in sa2b_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = 31

        # Mission Locations
        total_required_locations *= self.world.IncludeMissions[self.player]

        # Upgrades
        total_required_locations += 28

        # Fill item pool with all required items
        for item in {**upgrades_table}:
            itempool += self._create_items(item)

        itempool += [self.create_item(ItemName.emblem)] * (total_required_locations - len(itempool))

        self.world.itempool += itempool

        self.emblems_for_cannons_core = math.floor((total_required_locations - len(itempool)) * (self.world.EmblemPercentageForCannonsCore[self.player] / 100.0))

        shuffled_region_list = list(range(30))
        emblem_requirement_list = list()
        self.world.random.shuffle(shuffled_region_list)
        levels_per_gate = 30 / (self.world.NumberOfLevelGates[self.player] + 1)
        levels_added = 0
        current_gate = 0
        for i in range(30):
            emblem_requirement_list.append(current_gate)
            levels_added += 1
            if levels_added >= levels_per_gate:
                current_gate += 1
                levels_added = 0

        self.region_emblem_map = dict(zip(shuffled_region_list, emblem_requirement_list))

        connect_regions(self.world, self.player)

        if self.world.MusicShuffle[self.player] == "levels":
            musiclist_o = list(range(0, 46))
            musiclist_s = musiclist_o.copy()
            self.world.random.shuffle(musiclist_s)
            self.music_map = dict(zip(musiclist_o, musiclist_s))
        elif self.world.MusicShuffle[self.player] == "full":
            musiclist_o = list(range(0, 77))
            musiclist_s = musiclist_o.copy()
            self.world.random.shuffle(musiclist_s)
            self.music_map = dict(zip(musiclist_o, musiclist_s))
        else:
            self.music_map = dict()

    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return SA2BItem(name, data.progression, data.code, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)
