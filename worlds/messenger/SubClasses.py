from typing import Set, TYPE_CHECKING

from BaseClasses import Region, RegionType, Location, Item, ItemClassification, Entrance
from .Constants import SEALS, NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS
from .Regions import REGIONS

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


class MessengerRegion(Region):
    def __init__(self, name: str, world: MessengerWorld):
        super().__init__(name, RegionType.Generic, name, world.player, world.multiworld)
        self.rules = world.rules
        self.locations_lookup = self.multiworld.worlds[self.player].location_name_to_id
        self.add_locations()
        world.multiworld.regions.append(self)

    def add_locations(self) -> None:
        for loc in REGIONS[self.name]:
            self.locations.append(MessengerLocation(loc, self))
        if self.multiworld.shuffle_seals[self.player]:
            # putting some dumb special case for searing crags and ToT so i can split them into 2 regions
            seal_locs = [loc for loc in SEALS
                         if loc.startswith(self.name.split(" ")[0]) and self.name not in {"Searing Crags", "Tower HQ"}]
            for seal_loc in seal_locs:
                self.locations.append(MessengerLocation(seal_loc, self))

    def add_exits(self, exits: Set[str]) -> None:
        for exit in exits:
            ret = Entrance(self.player, f"{self.name} -> {exit}", self)
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

    def __init__(self, name: str, player: int, item_id: int = None):
        item_class = ItemClassification.filler
        if name in {*NOTES, *PROG_ITEMS, *PHOBEKINS} or item_id is None:
            item_class = ItemClassification.progression
        elif name in USEFUL_ITEMS:
            item_class = ItemClassification.useful
        super().__init__(name, item_class, item_id, player)

