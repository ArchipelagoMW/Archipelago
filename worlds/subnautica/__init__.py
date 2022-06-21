import logging
import typing

logger = logging.getLogger("Subnautica")

from .Locations import lookup_name_to_id as locations_lookup_name_to_id
from .Items import item_table, lookup_name_to_item, advancement_item_names
from .Items import lookup_name_to_id as items_lookup_name_to_id

from .Regions import create_regions
from .Rules import set_rules
from .Options import options

from BaseClasses import Region, Entrance, Location, MultiWorld, Item, Tutorial, ItemClassification, RegionType
from ..AutoWorld import World, WebWorld


class SubnaticaWeb(WebWorld):
    tutorials = [Tutorial(
        "Multiworld Setup Guide",
        "A guide to setting up the Subnautica randomizer connected to an Archipelago Multiworld",
        "English",
        "setup_en.md",
        "setup/en",
        ["Berserker"]
    )]


class SubnauticaWorld(World):
    """
    Subnautica is an undersea exploration game. Stranded on an alien world, you become infected by
    an unknown bacteria. The planet's automatic quarantine will shoot you down if you try to leave.
    You must find a cure for yourself, build an escape rocket, and leave the planet.
    """
    game: str = "Subnautica"
    web = SubnaticaWeb()

    item_name_to_id = items_lookup_name_to_id
    location_name_to_id = locations_lookup_name_to_id
    options = options

    data_version = 2
    required_client_version = (0, 1, 9)

    def generate_basic(self):
        # Link regions
        self.world.get_entrance('Lifepod 5', self.player).connect(self.world.get_region('Planet 4546B', self.player))

        # Generate item pool
        pool = []
        neptune_launch_platform = None
        extras = 0
        valuable = self.world.item_pool[self.player] == "valuable"
        for item in item_table:
            for i in range(item["count"]):
                subnautica_item = self.create_item(item["name"])
                if item["name"] == "Neptune Launch Platform":
                    neptune_launch_platform = subnautica_item
                elif valuable and not item["progression"]:
                    self.world.push_precollected(subnautica_item)
                    extras += 1
                else:
                    pool.append(subnautica_item)

        for item_name in self.world.random.choices(sorted(advancement_item_names - {"Neptune Launch Platform"}),
                                                   k=extras):
            item = self.create_item(item_name)
            item.advancement = False  # as it's an extra, just fast-fill it somewhere
            pool.append(item)

        self.world.itempool += pool

        # Victory item
        self.world.get_location("Aurora - Captain Data Terminal", self.player).place_locked_item(
            neptune_launch_platform)
        self.world.get_location("Neptune Launch", self.player).place_locked_item(
            SubnauticaItem("Victory", ItemClassification.progression, None, player=self.player))

    def set_rules(self):
        set_rules(self.world, self.player)

    def create_regions(self):
        create_regions(self.world, self.player)

    def fill_slot_data(self):
        slot_data = {}
        return slot_data

    def create_item(self, name: str) -> Item:
        item = lookup_name_to_item[name]
        return SubnauticaItem(name,
                              ItemClassification.progression if item["progression"] else ItemClassification.filler,
                              item["id"], player=self.player)


def create_region(world: MultiWorld, player: int, name: str, locations=None, exits=None):
    ret = Region(name, RegionType.Generic, name, player)
    ret.world = world
    if locations:
        for location in locations:
            loc_id = locations_lookup_name_to_id.get(location, 0)
            location = SubnauticaLocation(player, location, loc_id, ret)
            ret.locations.append(location)
    if exits:
        for exit in exits:
            ret.exits.append(Entrance(player, exit, ret))

    return ret


class SubnauticaLocation(Location):
    game: str = "Subnautica"


class SubnauticaItem(Item):
    game = "Subnautica"
