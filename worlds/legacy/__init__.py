import random
import typing

from BaseClasses import Region, MultiWorld, Entrance, Item
from .Items import LegacyItem, item_table, item_frequencies, base_item_table, extra_item_table, equipment_item_table, rune_item_table
from .Locations import LegacyLocation, location_table, base_location_table
from .Options import legacy_options
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World


class LegacyWorld(World):
    """
    Rogue Legacy is a genealogical rogue-"LITE" where anyone can be a hero. Each time you die, your child will succeed
    you. Every child is unique. One child might be colorblind, another might have vertigo-- they could even be a dwarf.
    But that's OK, because no one is perfect, and you don't have to be to succeed.
    """
    game: str = "Rogue Legacy"
    options = legacy_options
    topology_present = False
    data_version = 0

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    def _get_slot_data(self):
        return {
            "starting_gender": self.world.starting_gender[self.player],
            "new_game_plus": self.world.new_game_plus[self.player],
            "fairy_chests_per_zone": self.world.fairy_chests_per_zone[self.player],
            "chests_per_zone": self.world.chests_per_zone[self.player],
            "items_every_nth_chests": self.world.items_every_nth_chests[self.player],
            "vendors": self.world.vendors[self.player],
            "require_purchasing_equipment": self.world.require_purchasing_equipment[self.player],
            "require_purchasing_runes": self.world.require_purchasing_runes[self.player],
            "gold_gain_multiplier": self.world.gold_gain_multiplier[self.player],
            "death_link": self.world.death_link[self.player],
        }

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in legacy_options:
            option = getattr(self.world, option_name)[self.player]
            slot_data[option_name] = option.value

        return slot_data

    def generate_basic(self):
        itempool: typing.List[LegacyItem] = []
        total_required_locations = 61 + (self.world.chests_per_zone[self.player] * 4) + (self.world.fairy_chests_per_zone[self.player] * 4)

        # Fill item pool with all base items
        for item in base_item_table:
            if item in item_frequencies:
                itempool += [self.create_item(item)] * item_frequencies[item]
            else:
                itempool += [self.create_item(item)]

        for item in equipment_item_table:
            itempool += [self.create_item(item)]

        for item in rune_item_table:
            itempool += [self.create_item(item)]

        # Check if we need to start with these vendors or put them in the pool.
        if self.world.vendors[self.player].value == 0:
            self.world.push_precollected(self.world.create_item("Blacksmith", self.player))
            self.world.push_precollected(self.world.create_item("Enchantress", self.player))
        else:
            itempool += [self.create_item("Blacksmith"), self.create_item("Enchantress")]

        # Fill item pool with the remaining
        for _ in range(len(itempool), total_required_locations):
            item = random.choice(extra_item_table)
            itempool += [self.create_item(item)]

        self.world.itempool += itempool

    def create_regions(self):
        create_regions(self.world, self.player)

    def create_item(self, name: str) -> Item:
        return LegacyItem(name, self.player)

    def set_rules(self):
        set_rules(self.world, self.player)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    # Shamelessly stolen from the ROR2 definition, lol
    ret = Region(name, None, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = LegacyLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret
