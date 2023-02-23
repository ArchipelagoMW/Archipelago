import os

import BaseClasses
from .Items import FFPSItem, item_table
from .Locations import FFPSLocations, location_table, exclusion_table
from .Regions import FFPS_regions, link_FFPS_structures
from .Rules import set_rules, set_completion_rules

from BaseClasses import Region, Entrance, Item, Tutorial
from .Options import FFPS_options
from ..AutoWorld import World, WebWorld

client_version = 7


def data_path(*args):
    return os.path.join(os.path.dirname(__file__), 'data', *args)


class FFPSWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Tutorial",
        "A guide to setting up the Archipelago FFPS software on your computer. This guide covers "
        "single-player, multiworld, and related software.",
        "English",
        "ffps_en.md",
        "ffps/en",
        ["Mewlif"]
    )]


class FFPSWorld(World):
    """
    Freddy Fazbear's Pizzeria Simulator is a horror game where animatronics come through vents into your office
    to kill you. You win if you complete night 5 with all 4 animatronics obtained in your world to get the true ending.
    """
    game = "FFPS"
    web = FFPSWeb()
    option_definitions = FFPS_options
    topology_present = True

    item_name_to_id = {name: data.code for name, data in item_table.items()}
    location_name_to_id = {name: data.id for name, data in location_table.items()}

    data_version = 4

    def _get_FFPS_data(self):
        return {
            'world_seed': self.multiworld.per_slot_randoms[self.player].getrandbits(32),
            'seed_name': self.multiworld.seed_name,
            'player_name': self.multiworld.get_player_name(self.player),
            'player_id': self.player,
            'client_version': client_version,
            'race': self.multiworld.is_race,
            'max_anim_appears': int(self.multiworld.max_animatronics_appearing[self.player]),
            'catalogue_rando': bool(self.multiworld.catalogue_rando[self.player]),
            'night_difficulty': int(self.multiworld.night_difficulty[self.player]),
            'upgrade_rando': bool(self.multiworld.upgrade_rando[self.player]),
        }

    def generate_basic(self):
        # Generate item pool
        itempool = []

        # Add all required progression items
        for name, item in self.item_name_to_id.items():
            itempool += [name]
        itempool += ["Stage Upgrade"] * 4
        itempool += ["Cup Upgrade"] * 3
        itempool += ["Speaker Upgrade"] * 1

        self.multiworld.random.shuffle(itempool)

        # Convert itempool into real items
        if not getattr(self.multiworld, f"catalogue_rando")[self.player]:
            self.multiworld.get_location("Unlocked Catalogue 2", self.player).place_locked_item(
                self.create_item("Catalogue 2 Unlock"))
            self.multiworld.get_location("Unlocked Catalogue 3", self.player).place_locked_item(
                self.create_item("Catalogue 3 Unlock"))
            self.multiworld.get_location("Unlocked Catalogue 4", self.player).place_locked_item(
                self.create_item("Catalogue 4 Unlock"))
            itempool.remove("Catalogue 2 Unlock")
            itempool.remove("Catalogue 3 Unlock")
            itempool.remove("Catalogue 4 Unlock")

        if not getattr(self.multiworld, f"upgrade_rando")[self.player]:
            self.multiworld.get_location("Bought Printer Upgrade", self.player).place_locked_item(
                self.create_item("Printer Upgrade"))
            self.multiworld.get_location("Bought Handyman Upgrade", self.player).place_locked_item(
                self.create_item("Handyman Upgrade"))
            self.multiworld.get_location("Bought Internet Upgrade", self.player).place_locked_item(
                self.create_item("Internet Upgrade"))
            itempool.remove("Printer Upgrade")
            itempool.remove("Handyman Upgrade")
            itempool.remove("Internet Upgrade")

        itempool = [item for item in map(lambda name: self.create_item(name), itempool)]
        self.multiworld.itempool += itempool

    def set_rules(self):
        set_rules(self.multiworld, self.player)
        set_completion_rules(self.multiworld, self.player)

    def create_regions(self):
        def FFPSRegion(region_name: str, exits=[]):
            ret = Region(region_name, self.player, self.multiworld)
            ret.locations = [FFPSLocations(self.player, loc_name, loc_data.id, ret)
                             for loc_name, loc_data in location_table.items()
                             if loc_data.region == region_name]
            for exit in exits:
                ret.exits.append(Entrance(self.player, exit, ret))
            return ret

        self.multiworld.regions += [FFPSRegion(*r) for r in FFPS_regions]
        link_FFPS_structures(self.multiworld, self.player)

    def fill_slot_data(self):
        slot_data = self._get_FFPS_data()
        for option_name in FFPS_options:
            option = getattr(self.multiworld, option_name)[self.player]
            if slot_data.get(option_name, None) is None and type(option.value) in {str, int}:
                slot_data[option_name] = int(option.value)
        return slot_data

    def create_item(self, name: str) -> Item:
        item_data = item_table[name]
        item = FFPSItem(name, item_data.classification, item_data.code, self.player)
        return item
