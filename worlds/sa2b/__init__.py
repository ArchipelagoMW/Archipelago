import os
import typing

from BaseClasses import Item, MultiWorld
from .Items import SA2BItem, ItemData, item_table, upgrades_table
from .Locations import SA2BLocation, all_locations, setup_locations
from .Options import sa2b_options
from .Regions import create_regions
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

    def _get_slot_data(self):
        return {
            "DeathLink":          self.world.DeathLink[self.player],
            "IncludeMission2":    self.world.IncludeMission2[self.player],
            "IncludeMission3":    self.world.IncludeMission3[self.player],
            "IncludeMission4":    self.world.IncludeMission4[self.player],
            "IncludeMission5":    self.world.IncludeMission5[self.player],
            "IncludeChaoEmblems": self.world.IncludeChaoEmblems[self.player],
        }

    def _create_items(self, name: str):
        data = item_table[name]
        return [self.create_item(name)] * data.quantity

    def get_required_client_version(self) -> typing.Tuple[int, int, int]:
        return max((0, 2, 5), super(SA2BWorld, self).get_required_client_version())

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in sa2b_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data
    

    def generate_basic(self):
        itempool: typing.List[SA2BItem] = []

        # First Missions
        total_required_locations = 30

        # Second Missions
        if self.world.IncludeMission2[self.player]:
            total_required_locations += 30

        # Third Missions
        if self.world.IncludeMission3[self.player]:
            total_required_locations += 30

        # Fourth Missions
        if self.world.IncludeMission4[self.player]:
            total_required_locations += 30

        # Fifth Missions
        if self.world.IncludeMission5[self.player]:
            total_required_locations += 30

        # Cannon's Core Missions
        if self.world.IncludeCannonsCore[self.player]:
            total_required_locations += 5

        # Fill item pool with all required items
        for item in {**upgrades_table}:
            itempool += self._create_items(item)

        itempool += [self.create_item(ItemName.emblem)] * (total_required_locations - len(itempool))

        self.world.itempool += itempool


    def create_regions(self):
        location_table = setup_locations(self.world, self.player)
        create_regions(self.world, self.player, location_table)

    def create_item(self, name: str) -> Item:
        data = item_table[name]
        return SA2BItem(name, data.progression, data.code, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)
