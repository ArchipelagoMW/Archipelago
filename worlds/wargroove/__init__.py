import os
import string
import json

from BaseClasses import Item, MultiWorld, Region, Location, Entrance, Tutorial, ItemClassification, RegionType
from .Items import item_table, item_pool
from .Locations import location_table
from .Regions import create_regions
from .Rules import set_rules
from ..AutoWorld import World, WebWorld
from .Options import wargroove_options


class WargrooveWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up Slay the Spire for Archipelago. "
        "This guide covers single-player, multiworld, and related software.",
        "English",
        "wargroove_en.md",
        "wargroove/en",
        ["Fly Sniper"]
    )]


class WargrooveWorld(World):
    """
    Command an army, customize battlefields, and challenge your friends,
    in this richly detailed return to retro turn-based combat!
    """

    option_definitions = wargroove_options
    game = "Wargroove"
    topology_present = True
    data_version = 1
    web = WargrooveWeb()

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = location_table

    forced_auto_forfeit = True

    def _get_slot_data(self):
        return {
            'seed': "".join(self.multiworld.slot_seeds[self.player].choice(string.ascii_letters) for i in range(16)),
            'income_boost': self.multiworld.income_boost[self.player],
            'co_defense_boost': self.multiworld.co_defense_boost[self.player]
        }

    def generate_basic(self):
        # Fill out our pool with our items from item_pool, assuming 1 item if not present in item_pool
        pool = []
        for name, data in item_table.items():
            if not data.event:
                for amount in range(item_pool.get(name, 1)):
                    item = WargrooveItem(name, self.player)
                    pool.append(item)

        self.multiworld.itempool += pool

        victory = WargrooveItem("Wargroove Victory", self.player)
        self.multiworld.get_location("Wargroove Finale: Victory", self.player).place_locked_item(victory)

        if self.multiworld.logic[self.player] != 'no logic':
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Wargroove Victory", self.player)

    def set_rules(self):
        set_rules(self.multiworld, self.player)

    def create_item(self, name: str) -> Item:
        return WargrooveItem(name, self.player)

    def create_regions(self):
        create_regions(self.multiworld, self.player)

    def fill_slot_data(self) -> dict:
        slot_data = self._get_slot_data()
        for option_name in wargroove_options:
            option = getattr(self.multiworld, option_name)[self.player]
            slot_data[option_name] = int(option.value)
        return slot_data

    def get_filler_item_name(self) -> str:
        return self.multiworld.random.choice(["Card Draw", "Card Draw", "Card Draw", "Relic", "Relic"])

    def fill_slot_data(self):
        return {
            "player_id": self.player,
            "players": {player_id : self.multiworld.player_name[player_id] for player_id in self.multiworld.player_name},
            'income_boost': self.multiworld.income_boost[self.player].value,
            'co_defense_boost': self.multiworld.co_defense_boost[self.player].value
        }


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.multiworld = world
    if locations:
        for location in locations:
            loc_id = location_table.get(location, 0)
            location = WargrooveLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class WargrooveLocation(Location):
    game: str = "Wargroove"

    def __init__(self, player: int, name: str, address=None, parent=None):
        super(WargrooveLocation, self).__init__(player, name, address, parent)
        if address is None:
            self.event = True
            self.locked = True


class WargrooveItem(Item):
    game = "Wargroove"

    def __init__(self, name, player: int = None):
        item_data = item_table[name]
        super(WargrooveItem, self).__init__(
            name,
            ItemClassification.progression if item_data.progression else ItemClassification.filler,
            item_data.code, player
        )
