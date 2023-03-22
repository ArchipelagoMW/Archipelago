from typing import Set, TYPE_CHECKING, Optional, Dict

from BaseClasses import Region, Location, Item, ItemClassification, Entrance
from .Constants import SEALS, NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS
from .Options import Goal
from .Regions import REGIONS

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


class MessengerRegion(Region):
    def __init__(self, name: str, world: MessengerWorld) -> None:
        super().__init__(name, world.player, world.multiworld)
        self.add_locations(self.multiworld.worlds[self.player].location_name_to_id)
        world.multiworld.regions.append(self)

    def add_locations(self, name_to_id: Dict[str, int]) -> None:
        for loc in REGIONS[self.name]:
            self.locations.append(MessengerLocation(loc, self, name_to_id.get(loc, None)))
        if self.name == "The Shop" and self.multiworld.goal[self.player] > Goal.option_open_music_box:
            self.locations.append(MessengerLocation("Shop Chest", self, name_to_id.get("Shop Chest", None)))
        # putting some dumb special case for searing crags and ToT so i can split them into 2 regions
        if self.multiworld.shuffle_seals[self.player] and self.name not in {"Searing Crags", "Tower HQ"}:
            for seal_loc in SEALS:
                if seal_loc.startswith(self.name.split(" ")[0]):
                    self.locations.append(MessengerLocation(seal_loc, self, name_to_id.get(seal_loc, None)))

    def add_exits(self, exits: Set[str]) -> None:
        for exit in exits:
            ret = Entrance(self.player, f"{self.name} -> {exit}", self)
            self.exits.append(ret)
            ret.connect(self.multiworld.get_region(exit, self.player))


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, name: str, parent: MessengerRegion, loc_id: Optional[int]) -> None:
        super().__init__(parent.player, name, loc_id, parent)
        if loc_id is None:
            self.place_locked_item(MessengerItem(name, parent.player, None))


class MessengerItem(Item):
    game = "The Messenger"

    def __init__(self, name: str, player: int, item_id: Optional[int] = None, override_progression: bool = False) -> None:
        if name in {*NOTES, *PROG_ITEMS, *PHOBEKINS} or item_id is None or override_progression:
            item_class = ItemClassification.progression
        elif name in USEFUL_ITEMS:
            item_class = ItemClassification.useful
        else:
            item_class = ItemClassification.filler
        super().__init__(name, item_class, item_id, player)

