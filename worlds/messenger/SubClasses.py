from typing import Set

from BaseClasses import Region, RegionType, Location, Item, ItemClassification, Entrance
from .Constants import SEALS, NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS
from .Regions import REGIONS


class MessengerRegion(Region):
    def __init__(self, name: str, world: "MessengerWorld"):
        super().__init__(name, RegionType.Generic, name, world.player, world.multiworld)
        self.rules = world.rules
        self.locations_lookup = self.multiworld.worlds[self.player].location_name_to_id
        self.add_locations()
        world.multiworld.regions.append(self)

    def create_location(self, name: str) -> "Location":
        loc = MessengerLocation(name, self)
        return loc

    def add_locations(self) -> None:
        for loc in REGIONS[self.name]:
            self.locations.append(self.create_location(loc))
        if self.multiworld.shuffle_seals[self.player]:
            seal_locs = [loc for loc in SEALS if loc.startswith(self.name)]
            for seal_loc in seal_locs:
                self.locations.append(self.create_location(seal_loc))

    def add_exits(self, exits: Set[str]) -> None:
        for exit in exits:
            ret = Entrance(self.player, exit, self)
            if exit in self.rules.region_rules:
                ret.access_rule = self.rules.region_rules[exit]
            self.exits.append(ret)
            ret.connect(self.multiworld.get_region(exit, self.player))


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, name: str, parent: MessengerRegion):
        loc_id = parent.locations_lookup[name] if name in parent.locations_lookup else None
        super().__init__(parent.player, name, loc_id, parent)
        if name in parent.rules.location_rules:
            self.access_rule = parent.rules.location_rules[name]
        if loc_id is None:
            self.place_locked_item(parent.multiworld.worlds[self.player].create_item(name))


class MessengerItem(Item):
    game = "The Messenger"

    def __init__(self, name: str, world: "MessengerWorld"):
        item_class = ItemClassification.filler
        if name in {*NOTES, *PROG_ITEMS, *PHOBEKINS}:
            item_class = ItemClassification.progression
        elif name in USEFUL_ITEMS:
            item_class = ItemClassification.useful
        item_id = world.item_name_to_id[name] if name in world.item_name_to_id else None
        if item_id is None:
            item_class = ItemClassification.progression
        super().__init__(name, item_class, item_id, world.player)

