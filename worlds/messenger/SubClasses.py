from typing import TYPE_CHECKING, Optional

from BaseClasses import Region, Location, Item, ItemClassification
from .Constants import SEALS, NOTES, PROG_ITEMS, PHOBEKINS, USEFUL_ITEMS
from .Options import Goal
from .Regions import REGIONS, MEGA_SHARDS

if TYPE_CHECKING:
    from . import MessengerWorld
else:
    MessengerWorld = object


class MessengerRegion(Region):
    def __init__(self, name: str, world: MessengerWorld) -> None:
        super().__init__(name, world.player, world.multiworld)
        locations = [loc for loc in REGIONS[self.name]]
        if self.name == "The Shop" and self.multiworld.goal[self.player] > Goal.option_open_music_box:
            locations += ["Shop Chest"]
        if self.multiworld.shuffle_seals[self.player] and self.name not in {"Searing Crags", "Tower HQ", "Cloud Ruins"}:
            locations += [loc for loc in SEALS if loc.startswith(self.name.split(" ")[0])]
        if self.multiworld.shuffle_shards[self.player] and self.name in MEGA_SHARDS:
            locations += [loc for loc in MEGA_SHARDS[self.name]]
        loc_dict = {loc: world.location_name_to_id.get(loc, None) for loc in locations}
        self.add_locations(loc_dict, MessengerLocation)
        world.multiworld.regions.append(self)


class MessengerLocation(Location):
    game = "The Messenger"

    def __init__(self, player: int, name: str, loc_id: Optional[int], parent: MessengerRegion) -> None:
        super().__init__(player, name, loc_id, parent)
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

